from pathlib import Path

from app.parsers.base import ResumeParser
from app.parsers.docx_parser import DOCXParser
from app.parsers.pdf_parser import PDFParser


def get_resume_parser(file_path: Path) -> ResumeParser:
    extension = file_path.suffix.lower()

    if extension == ".pdf":
        return PDFParser()

    if extension == ".docx":
        return DOCXParser()

    raise ValueError(f"Unsupported resume format: {extension}")
