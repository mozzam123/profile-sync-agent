from datetime import date

from pydantic import BaseModel, Field


class Experience(BaseModel):
    company: str
    role: str
    start_date: date | None = None
    end_date: date | None = None
    description: str | None = None


class Project(BaseModel):
    name: str
    description: str | None = None
    technologies: list[str] = Field(default_factory=list)
    url: str | None = None


class Education(BaseModel):
    institution: str
    degree: str | None = None
    field_of_study: str | None = None
    start_date: date | None = None
    end_date: date | None = None


class CanonicalProfile(BaseModel):
    name: str

    headline: str | None = None
    summary: str | None = None
    location: str | None = None

    email: str | None = None

    skills: list[str] = Field(default_factory=list)

    experience: list[Experience] = Field(default_factory=list)
    projects: list[Project] = Field(default_factory=list)
    education: list[Education] = Field(default_factory=list)
