from app.profile.models import CanonicalProfile, Experience, Project


profile = CanonicalProfile(
    name="Test User",
    headline="AI Engineer",
    skills=[
        "Python",
        "FastAPI",
        "LangGraph",
    ],
    experience=[
        Experience(
            company="Example Corp",
            role="AI Engineer",
        )
    ],
    projects=[
        Project(
            name="Profile Sync Agent",
            description="Synchronizes professional profiles.",
            technologies=[
                "Python",
                "FastAPI",
                "LangGraph",
            ],
        )
    ],
)


print(profile.model_dump_json(indent=2))
