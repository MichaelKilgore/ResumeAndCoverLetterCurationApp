# ResumeAndCoverLetterCurationApp


1. make google docs
2. sql database

    1. Table 1: Company
        - uuid
        - Company Name
        - Item Type (WORK_EXPERIENCE, RELEVANT_PROJECT)

    2. Table 2: Job
        - uuid
        - Job Title
        - date range
        - company uuid

    3. Table 3: Bullet Point
        - uuid
        - bullet point description
        - job uuid

    4. Table 4: Keywords
        - uuid
        - keyword
        - bullet point uuid

    5. Table 5: Skills
        - skill_type (LANGUAGE, SYSTEMS & DATA, TOOLS)
        - skill (Javascript, S3)

    Company -> Job Title (1 - many)
    Job -> Bullet Point (1 - many)
    Bullet Point -> Keyword (1 - many)

    Static Data:
        - Name
        - email
        - phone number
        - linkedIn
        - github
        - Education

3. Resume Maker Workflow:
    - Extract keywords from job description
    - Pull top 4 bullet points for selected jobs
    - construct google doc
    - create google doc

4. Cover Letter Workflow:
    - View instructions
    - View Resume
    - View Promo Doc
