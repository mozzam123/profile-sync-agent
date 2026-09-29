from app.platforms.base import PlatformAdapter
from app.platforms.models import (
    PlatformChangeSet,
    SyncResult,
)
from app.profile.models import CanonicalProfile


class GitHubAdapter(PlatformAdapter):

    @property
    def platform_name(self) -> str:
        return "github"

    def prepare_changes(
        self,
        profile: CanonicalProfile,
    ) -> PlatformChangeSet:

        raise NotImplementedError

    def sync(
        self,
        changes: PlatformChangeSet,
    ) -> SyncResult:

        raise NotImplementedError
