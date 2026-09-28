import shutil
from pathlib import Path
from uuid import uuid4

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
)  # pyright: ignore[reportMissingImports]
from app.parsers.factory import get_resume_parser
from app.profile.extractor import ProfileExtractor
from sqlalchemy.orm import Session  # pyright: ignore[reportMissingImports]
from app.db.database import get_db
from app.profile.repository import ProfileRepository
from app.profile.models import CanonicalProfile
from app.profile.diff import ProfileDiffService


router = APIRouter()

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def save_upload(file: UploadFile) -> Path:
    extension = Path(file.filename or "").suffix.lower()

    if extension not in {".pdf", ".docx"}:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX resumes are supported.",
        )

    file_path = UPLOAD_DIR / f"{uuid4()}{extension}"

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return file_path


@router.post("/resume/parse")
async def parse_resume(file: UploadFile = File(...)):
    file_path = save_upload(file)

    try:
        parser = get_resume_parser(file_path)
        text = parser.parse(file_path)

        if not text.strip():
            raise HTTPException(
                status_code=422,
                detail="No readable text found in resume.",
            )

        return {
            "filename": file.filename,
            "characters": len(text),
            "text": text,
        }

    finally:
        file.file.close()

        if file_path.exists():
            file_path.unlink()


@router.post("/resume/extract")
async def extract_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    file_path = save_upload(file)

    try:
        parser = get_resume_parser(file_path)
        text = parser.parse(file_path)

        if not text.strip():
            raise HTTPException(
                status_code=422,
                detail="No readable text found in resume.",
            )

        extractor = ProfileExtractor()
        profile = extractor.extract(text)

        repository = ProfileRepository()

        saved_version = repository.save(
            db=db,
            profile=profile,
        )

        return {
            "version": saved_version.version,
            "profile": profile,
        }

    finally:
        file.file.close()

        if file_path.exists():
            file_path.unlink()


# Endpoint to get the latest data for resume
@router.get("/profiles/latest")
def get_latest_profile(
    db: Session = Depends(get_db),
):
    repository = ProfileRepository()

    version = repository.get_latest(db)

    if version is None:
        raise HTTPException(
            status_code=404,
            detail="No profile versions found.",
        )

    return {
        "version": version.version,
        "created_at": version.created_at,
        "profile": CanonicalProfile.model_validate_json(version.profile_json),
    }


@router.get("/profiles/diff")
def compare_profiles(
    old_version: int,
    new_version: int,
    db: Session = Depends(get_db),
):
    repository = ProfileRepository()

    old_record = repository.get_by_version(
        db,
        old_version,
    )

    new_record = repository.get_by_version(
        db,
        new_version,
    )

    if old_record is None or new_record is None:
        raise HTTPException(
            status_code=404,
            detail="One or both profile versions were not found.",
        )

    old_profile = CanonicalProfile.model_validate_json(old_record.profile_json)

    new_profile = CanonicalProfile.model_validate_json(new_record.profile_json)

    diff_service = ProfileDiffService()

    diff = diff_service.compare(
        old=old_profile,
        new=new_profile,
    )

    return {
        "old_version": old_version,
        "new_version": new_version,
        "total_changes": diff.total_changes,
        "changes": diff.changes,
    }
