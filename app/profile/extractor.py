from app.llm.provider import get_llm
from app.profile.models import CanonicalProfile


class ProfileExtractor:

    def __init__(self):
        llm = get_llm()

        self.structured_llm = llm.with_structured_output(CanonicalProfile)

    def extract(self, resume_text: str) -> CanonicalProfile:

        prompt = f"""
You are a professional resume information extraction system.

Your job is to carefully read the ENTIRE resume and extract ALL relevant
professional information into the provided structured schema.

IMPORTANT:
Do not stop after extracting basic personal information or education.
Read and process every section of the resume.

Extract the following:

1. name
2. professional headline/title, if available
3. professional summary, if available
4. location, if available
5. email

6. skills
   - Extract ALL technical and professional skills explicitly mentioned.
   - Include programming languages, frameworks, databases, AI technologies,
     cloud technologies, tools, and platforms.
   - Do not return an empty skills list if skills are clearly present.

7. experience
   For EVERY work experience extract:
   - company
   - role
   - start date
   - end date
   - concise description

   Do not omit previous or current work experience.

8. projects
   For EVERY project extract:
   - project name
   - description
   - technologies
   - URL if explicitly available

9. education
   For EVERY education entry extract:
   - institution
   - degree
   - field of study
   - dates when available

RULES:

- Read the complete resume before producing the result.
- Extract all relevant entries, not only the first one.
- Never invent information.
- Unknown optional values should be null.
- Missing sections should use empty lists.
- Preserve important technical keywords exactly when practical.
- Current employment should have end_date = null.
- If only a year is provided and an exact date cannot be determined,
  do not invent a month or day.
- Information appearing in bullet points is important and must not be ignored.

RESUME START
----------------

{resume_text}

----------------
RESUME END
"""

        return self.structured_llm.invoke(prompt)
