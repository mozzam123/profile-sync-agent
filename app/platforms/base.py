from abc import ABC, abstractmethod

from app.platforms.models import (
    PlatformChangeSet,
    SyncResult,
)
from app.profile.models import CanonicalProfile


class PlatformAdapter(ABC):

    @property
    @abstractmethod
    def platform_name(self) -> str:
        pass

    @abstractmethod
    def prepare_changes(
        self,
        profile: CanonicalProfile,
    ) -> PlatformChangeSet:
        """
        Compare the canonical profile with the
        current platform state and prepare proposed changes.
        """
        pass

    @abstractmethod
    def sync(
        self,
        changes: PlatformChangeSet,
    ) -> SyncResult:
        """
        Apply previously approved changes.
        """
        pass
