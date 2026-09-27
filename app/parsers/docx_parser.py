from pathlib import Path

from docx import Document

from app.parsers.base import ResumeParser


class DOCXParser(ResumeParser):

    def parse(self, file_path: Path) -> str:
        document = Document(file_path)

        paragraphs = [
            paragraph.text.strip()
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        ]

        return "\n".join(paragraphs)
