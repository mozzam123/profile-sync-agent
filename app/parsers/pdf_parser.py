from pathlib import Path

import fitz

from app.parsers.base import ResumeParser


class PDFParser(ResumeParser):

    def parse(self, file_path: Path) -> str:
        document = fitz.open(file_path)

        pages = []

        try:
            for page in document:
                text = page.get_text("text")
                pages.append(text)
        finally:
            document.close()

        return "\n".join(pages).strip()
