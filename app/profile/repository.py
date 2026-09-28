from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.models import ProfileVersion
from app.profile.models import CanonicalProfile


class ProfileRepository:

    def save(
        self,
        db: Session,
        profile: CanonicalProfile,
    ) -> ProfileVersion:

        latest_version = db.scalar(select(func.max(ProfileVersion.version)))

        next_version = (latest_version or 0) + 1

        profile_version = ProfileVersion(
            version=next_version,
            profile_json=profile.model_dump_json(),
        )

        db.add(profile_version)
        db.commit()
        db.refresh(profile_version)

        return profile_version

    def get_latest(
        self,
        db: Session,
    ) -> ProfileVersion | None:

        return db.scalar(
            select(ProfileVersion).order_by(ProfileVersion.version.desc()).limit(1)
        )

    def get_previous(
        self,
        db: Session,
    ) -> ProfileVersion | None:

        return db.scalar(
            select(ProfileVersion)
            .order_by(ProfileVersion.version.desc())
            .offset(1)
            .limit(1)
        )
