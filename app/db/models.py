from datetime import datetime

from sqlalchemy import DateTime, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class ProfileVersion(Base):
    __tablename__ = "profile_versions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    version: Mapped[int] = mapped_column(
        Integer,
        unique=True,
        nullable=False,
    )

    profile_json: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
