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

def _get_bullet_points(job_title: str) -> list[str]:
    conn = psycopg2.connect(dbname="resume_app")
    cur = conn.cursor()
    cur.execute("""
        SELECT bp.sentence, bp.value
        FROM bullet_point bp
        JOIN job j ON bp.job_uuid = j.uuid
        WHERE j.job_title = %s
        ORDER BY bp.value DESC
    """, (job_title,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [row[0] for row in rows]

def _get_project_bullet_points(project_name: str) -> list[dict]:
    conn = psycopg2.connect(dbname="resume_app")
    cur = conn.cursor()
    cur.execute("""
        SELECT bp.sentence, bp.value
        FROM bullet_point bp
        JOIN project p ON bp.project_uuid = p.uuid
        WHERE p.project_name = %s
        ORDER BY bp.value DESC
    """, (project_name,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [row[0] for row in rows]


def _get_skills(jd_key_words):
    conn = psycopg2.connect(dbname="resume_app")
    cur = conn.cursor()
    cur.execute("""
        SELECT sk.skill, sk.skill_type
        FROM skill sk;
    """, ())
    rows = cur.fetchall()
    cur.close()
    conn.close()

    skills = [ { 'skill': row[0], 'skill_type': row[1] } for row in rows ]

    for i,skill in enumerate(skills):
        if skill['skill'] in jd_key_words:
            skills[i]['is_keyword'] = True
        else:
            skills[i]['is_keyword'] = False

    return skills

def _get_skipped_keywords() -> list[str]:
    res = []
    with open('const/skipped_keywords.txt', 'r') as f:
        lines = f.readlines()
        for l in lines:
            res.append(l.strip())

    return res

def _get_jobs(jd_key_words):
    l = []
    for title in ('Software Development Engineer II', 'Software Development Engineer I', 'Software Engineer Intern'):
        l.append({ 'job title': title, 'bps': [] })
        bullet_points = _get_bullet_points(title)


        for bp in bullet_points:
            key_word_matches = [key_word for key_word in jd_key_words if key_word.lower() in bp.lower()]

            l[-1]['bps'].append({ 'bullet_point': bp, 'jd_key_word_matches': key_word_matches })

    return l

def _notify_user_of_missing_key_words(jd_key_words, l, skills, projects):
    matched_keywords = set()
    for job_entry in l:
        for bp_entry in job_entry['bps']:
            matched_keywords.update(bp_entry['jd_key_word_matches'])

    skipped_matches = _get_skipped_keywords()

    project_bps = []
    for project in projects:
        project_bps += project['bullet_points']

    unmatched_keywords = set([x.lower() for x in list(jd_key_words)]) - set([x.lower() for x in list(matched_keywords)]) - set([x.lower() for x in skipped_matches]) - set([skill['skill'].lower() for skill in skills]) - set([x.lower() for x in project_bps])
    if unmatched_keywords:
        print(f"\nWarning: The following JD keywords had no matches in any bullet point:")
        for kw in sorted(unmatched_keywords):
            print(f"  - {kw}")
        answer = input("\nDo you want to continue and call Claude? (y/n): ").strip().lower()
        if answer != 'y':
            raise RuntimeError("Aborted: unmatched JD keywords with no bullet point coverage.")

def _get_projects(jd_key_words):
    res = []
    for (p,d_r,p_t) in ( ('AI Stock Forecasts', 'Sept 2025 - Present','Personal Project'), ('Deep Swing Institutional System', 'Feb 2026', 'Upwork Contract') ):
        bps = _get_project_bullet_points(p)

        res.append( { 'project_name': p, 'bullet_points': bps, 'project_date_range': d_r, 'project_type': p_t } )

    return res

def _call_claude(jobs, skills, projects) -> SelectionResponse:
    client = anthropic.Anthropic()

    tool = {
        "name": "submit_selections",
        "description": "Submit the selected bullet points for each job title",
        "input_schema": SelectionResponse.model_json_schema()
    }

    with open('const/bullet_point_selection_prompt.txt', 'r') as f:
        prompt_template = f.read()

    prompt = prompt_template.format(l=jobs, skills=skills, projects=projects)

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



def generate_replacements(jd_key_words: list[str] | list[LiteralString]) -> dict:
    s = set(jd_key_words)

    l = _get_jobs(jd_key_words)

    skills = _get_skills(jd_key_words)

    projects = _get_projects(jd_key_words)

    _notify_user_of_missing_key_words(jd_key_words, l, skills, projects)

    res = _call_claude(l, skills, projects)

    replacements = _get_replacements(res)

    return replacements

if __name__ == '__main__':
    raw_hard_skills = 'Computer Science, postgresql, typescript, tailwind, node.js, docker, Jest, LLMs, CSS, NPM'
    raw_soft_skills = 'Collaboration'

    jd_key_words = raw_hard_skills.split(', ') + raw_soft_skills.split(', ')

    resp = generate_replacements(jd_key_words)

    print(resp)
