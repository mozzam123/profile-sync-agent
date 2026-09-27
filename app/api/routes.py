import shutil
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.parsers.factory import get_resume_parser
from app.profile.extractor import ProfileExtractor


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
async def extract_resume(file: UploadFile = File(...)):
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

        return profile

    finally:
        file.file.close()

        if file_path.exists():
            file_path.unlink()
