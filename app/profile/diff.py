from app.profile.models import (
    CanonicalProfile,
    ProfileChange,
    ProfileDiff,
)


class ProfileDiffService:

    def compare(
        self,
        old: CanonicalProfile,
        new: CanonicalProfile,
    ) -> ProfileDiff:

        changes: list[ProfileChange] = []

        changes.extend(self._compare_simple_fields(old, new))

        changes.extend(self._compare_skills(old, new))

        changes.extend(self._compare_experience(old, new))

        changes.extend(self._compare_projects(old, new))

        changes.extend(self._compare_education(old, new))

        return ProfileDiff(changes=changes)

    def _compare_simple_fields(
        self,
        old: CanonicalProfile,
        new: CanonicalProfile,
    ) -> list[ProfileChange]:

        changes = []

        fields = [
            "name",
            "headline",
            "summary",
            "location",
            "email",
        ]

        for field in fields:
            old_value = getattr(old, field)
            new_value = getattr(new, field)

            if old_value != new_value:
                changes.append(
                    ProfileChange(
                        change_type="updated",
                        section="profile",
                        identifier=field,
                        old_value=old_value,
                        new_value=new_value,
                    )
                )

        return changes

    def _compare_skills(
        self,
        old: CanonicalProfile,
        new: CanonicalProfile,
    ) -> list[ProfileChange]:

        changes = []

        old_skills = {skill.lower(): skill for skill in old.skills}

        new_skills = {skill.lower(): skill for skill in new.skills}

        added = new_skills.keys() - old_skills.keys()
        removed = old_skills.keys() - new_skills.keys()

        for key in sorted(added):
            changes.append(
                ProfileChange(
                    change_type="added",
                    section="skills",
                    identifier=new_skills[key],
                    new_value=new_skills[key],
                )
            )

        for key in sorted(removed):
            changes.append(
                ProfileChange(
                    change_type="removed",
                    section="skills",
                    identifier=old_skills[key],
                    old_value=old_skills[key],
                )
            )

        return changes

    def _compare_experience(
        self,
        old: CanonicalProfile,
        new: CanonicalProfile,
    ) -> list[ProfileChange]:

        old_items = {self._experience_key(item): item for item in old.experience}

        new_items = {self._experience_key(item): item for item in new.experience}

        return self._compare_items(
            section="experience",
            old_items=old_items,
            new_items=new_items,
        )

    def _compare_projects(
        self,
        old: CanonicalProfile,
        new: CanonicalProfile,
    ) -> list[ProfileChange]:

        old_items = {project.name.lower(): project for project in old.projects}

        new_items = {project.name.lower(): project for project in new.projects}

        return self._compare_items(
            section="projects",
            old_items=old_items,
            new_items=new_items,
        )

    def _compare_education(
        self,
        old: CanonicalProfile,
        new: CanonicalProfile,
    ) -> list[ProfileChange]:

        old_items = {item.institution.lower(): item for item in old.education}

        new_items = {item.institution.lower(): item for item in new.education}

        return self._compare_items(
            section="education",
            old_items=old_items,
            new_items=new_items,
        )

    def _compare_items(
        self,
        section: str,
        old_items: dict,
        new_items: dict,
    ) -> list[ProfileChange]:

        changes = []

        old_keys = old_items.keys()
        new_keys = new_items.keys()

        for key in sorted(new_keys - old_keys):
            item = new_items[key]

            changes.append(
                ProfileChange(
                    change_type="added",
                    section=section,
                    identifier=key,
                    new_value=item.model_dump(mode="json"),
                )
            )

        for key in sorted(old_keys - new_keys):
            item = old_items[key]

            changes.append(
                ProfileChange(
                    change_type="removed",
                    section=section,
                    identifier=key,
                    old_value=item.model_dump(mode="json"),
                )
            )

        for key in sorted(old_keys & new_keys):
            old_item = old_items[key]
            new_item = new_items[key]

            if old_item != new_item:
                changes.append(
                    ProfileChange(
                        change_type="updated",
                        section=section,
                        identifier=key,
                        old_value=old_item.model_dump(mode="json"),
                        new_value=new_item.model_dump(mode="json"),
                    )
                )

        return changes

    def _experience_key(self, experience) -> str:
        return f"{experience.role.lower()}" f"@{experience.company.lower()}"
