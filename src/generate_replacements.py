from typing import LiteralString
import psycopg2
import anthropic
from pydantic import BaseModel

JOB_TITLE_TO_PREFIX = { 'Software Development Engineer II': 'AMAZON_SDE_2_BULLET_', 'Software Development Engineer I': 'AMAZON_SDE_1_BULLET_', 'Software Engineer Intern': 'WKIT_SDE_INTERN_BULLET_' }

class JobSelection(BaseModel):
    title: str
    bps: list[str]

class SkillGroup(BaseModel):
    skill_type: str
    skills: list[str]

class Project(BaseModel):
    project_name: str
    project_type: str
    project_date_range: str
    bps: list[str]

class SelectionResponse(BaseModel):
    jobs: list[JobSelection]
    skill_groups: list[SkillGroup]
    project: Project
    missing_keywords: list[str]

def _call_claude(job_description, data) -> SelectionResponse:
    client = anthropic.Anthropic()

    tool = {
        "name": "submit_selections",
        "description": "Submit the selected bullet points for each job title",
        "input_schema": SelectionResponse.model_json_schema()
    }

    with open('const/bullet_point_selection_prompt.txt', 'r') as f:
        prompt_template = f.read()

    prompt = prompt_template.format(data=data, job_description=job_description)

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        tools=[tool],
        tool_choice={"type": "tool", "name": "submit_selections"},
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    tool_use_block = next(b for b in message.content if b.type == "tool_use")
    return SelectionResponse.model_validate(tool_use_block.input)

def _get_replacements(res: SelectionResponse) -> dict:
    replacements = {}

    ''' set jobs replacements '''
    for job in res.jobs:
        prefix = '{{' + JOB_TITLE_TO_PREFIX[job.title]
        for i, bp in enumerate(job.bps):
            if i == 0:
                replacements[prefix+'ONE'+'}}'] = bp
            elif i == 1:
                replacements[prefix+'TWO'+'}}'] = bp
            elif i == 2:
                replacements[prefix+'THREE'+'}}'] = bp
            elif i == 3:
                replacements[prefix+'FOUR'+'}}'] = bp

    ''' set skills replacements '''
    for skill_group in res.skill_groups:
        if skill_group.skill_type == 'LANGUAGE':
            replacements['{{LANGUAGES}}'] = ', '.join(skill_group.skills)
        if skill_group.skill_type == 'SYSTEMS_AND_DATA':
            replacements['{{SYSTEMS_AND_DATA}}'] = ', '.join(skill_group.skills)
        if skill_group.skill_type == 'TOOLS':
            replacements['{{TOOLS}}'] = ', '.join(skill_group.skills)

    ''' set project replacements '''
    project = res.project
    replacements['{{PROJECT_CHOICE}}'] = project.project_name
    replacements['{{PROJECT_DATE_RANGE}}'] = project.project_date_range
    replacements['{{PROJECT_TYPE}}'] = project.project_type
    prefix = '{{' + 'PROJECT_BULLET_'
    for i, bp in enumerate(project.bps):
        if i == 0:
            replacements[prefix+'ONE'+'}}'] = bp
        elif i == 1:
            replacements[prefix+'TWO'+'}}'] = bp
        elif i == 2:
            replacements[prefix+'THREE'+'}}'] = bp
        elif i == 3:
            replacements[prefix+'FOUR'+'}}'] = bp

    return replacements



def generate_replacements(job_description: str) -> dict:
    with open('const/data.json', 'r') as f:
        data = f.read()

    res = _call_claude(job_description, data)

    replacements = _get_replacements(res)

    if res.missing_keywords:
        answer = input(f"\nThe following keywords are missing: {res.missing_keywords}. Do you still want to generate the resume google doc? (y/n): ").strip().lower()

        if answer != 'y':
            raise Exception("Aborting process due to missing keywords")

    return replacements



if __name__ == '__main__':
    resp = generate_replacements()

    print(resp)

