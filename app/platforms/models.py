from typing import Any

from pydantic import BaseModel, Field


class PlatformChange(BaseModel):
    target: str
    field: str

    old_value: Any | None = None
    new_value: Any | None = None


class PlatformChangeSet(BaseModel):
    platform: str

    changes: list[PlatformChange] = Field(default_factory=list)

    @property
    def total_changes(self) -> int:
        return len(self.changes)


class SyncResult(BaseModel):
    platform: str
    success: bool
    message: str
