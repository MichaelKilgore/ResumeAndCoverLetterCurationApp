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

class SelectionResponse(BaseModel):
    jobs: list[JobSelection]
    skill_groups: list[SkillGroup]

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

def _get_skills() -> dict:
    conn = psycopg2.connect(dbname="resume_app")
    cur = conn.cursor()
    cur.execute("""
        SELECT sk.skill, sk.skill_type
        FROM skill sk;
    """, ())
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [ { 'skill': row[0], 'skill_type': row[1] } for row in rows ]

def _get_skipped_keywords() -> list[str]:
    res = []
    with open('skipped_keywords.txt', 'r') as f:
        lines = f.readlines()
        for l in lines:
            res.append(l.strip())

    return res

def generate_replacements(jd_key_words: list[str]) -> dict:
    s = set(jd_key_words)


    l = []
    for title in ('Software Development Engineer II', 'Software Development Engineer I', 'Software Engineer Intern'):
        l.append({ 'job title': title, 'bps': [] })
        bullet_points = _get_bullet_points(title)


        for bp in bullet_points:

            key_word_matches = [key_word for key_word in jd_key_words if key_word.lower() in bp.lower()]

            l[-1]['bps'].append({ 'bullet_point': bp, 'jd_key_word_matches': key_word_matches })

    # get skills
    skills = _get_skills()

    for i,skill in enumerate(skills):
        if skill['skill'] in jd_key_words:
            skills[i]['is_keyword'] = True
        else:
            skills[i]['is_keyword'] = False

    matched_keywords = set()
    for job_entry in l:
        for bp_entry in job_entry['bps']:
            matched_keywords.update(bp_entry['jd_key_word_matches'])

    skipped_matches = _get_skipped_keywords()

    unmatched_keywords = s - matched_keywords - set(skipped_matches) - set([skill['skill'] for skill in skills])
    if unmatched_keywords:
        print(f"\nWarning: The following JD keywords had no matches in any bullet point:")
        for kw in sorted(unmatched_keywords):
            print(f"  - {kw}")
        answer = input("\nDo you want to continue and call Claude? (y/n): ").strip().lower()
        if answer != 'y':
            raise RuntimeError("Aborted: unmatched JD keywords with no bullet point coverage.")


    client = anthropic.Anthropic()

    tool = {
        "name": "submit_selections",
        "description": "Submit the selected bullet points for each job title",
        "input_schema": SelectionResponse.model_json_schema()
    }

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        tools=[tool],
        tool_choice={"type": "tool", "name": "submit_selections"},
        messages=[
            {
                "role": "user",
                "content": f"For each of these job titles there is a list of bullet points, I need you to select 4 bullet points based on 3 criteria. \n\n1. The number of key words that the bullet point covers. Remember its import that the key word is an exact match so SQL is not the same as postgreSQL for example.\n2. Additionally the variety of bullet points, across all 4 bullet points we want to cover as many key words as possible.\n3. Finally some of these bullet points are reworded versions of other bullet points, make sure not to include duplicates.\nAlso P.S. order the bullets by a combination of how good a bullet point is and how many key words it has. A bullet point is good if it seems complex and makes use of data points such as improved forecasting by 10%.\n\njob data:\n\n{l}\n\nAdditionally for skills return all the skills given but remove duplicates. Like for example Python and Python3 are the same, pick which one to display based on whether or not it is a valid key word, if they both either are or are not key words then just pick one.\n\nskills data:\n\n{skills}"
            }
        ]
    )

    tool_use_block = next(b for b in message.content if b.type == "tool_use")
    res = SelectionResponse.model_validate(tool_use_block.input)

    replacements = {}

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

    for skill_group in res.skill_groups:
        if skill_group.skill_type == 'LANGUAGE':
            replacements['{{LANGUAGES}}'] = ', '.join(skill_group.skills)
        if skill_group.skill_type == 'SYSTEMS_AND_DATA':
            replacements['{{SYSTEMS_AND_DATA}}'] = ', '.join(skill_group.skills)
        if skill_group.skill_type == 'TOOLS':
            replacements['{{TOOLS}}'] = ', '.join(skill_group.skills)


    return replacements

if __name__ == '__main__':
    raw_hard_skills = 'Computer Science, postgresql, typescript, tailwind, node.js, docker, Jest, LLMs, CSS, NPM'
    raw_soft_skills = 'Collaboration'

    jd_key_words = raw_hard_skills.split(', ') + raw_soft_skills.split(', ')

    resp = generate_replacements(jd_key_words)

    print(resp)
