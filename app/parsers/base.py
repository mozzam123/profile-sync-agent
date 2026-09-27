from abc import ABC, abstractmethod
from pathlib import Path


class ResumeParser(ABC):

    @abstractmethod
    def parse(self, file_path: Path) -> str:
        """Extract text from a resume."""
        pass
