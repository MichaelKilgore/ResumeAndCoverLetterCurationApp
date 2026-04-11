from typing import LiteralString
import psycopg2
import anthropic
from pydantic import BaseModel

def _get_doc_text(docs_service, doc_id: str) -> str:
    doc = docs_service.documents().get(documentId=doc_id).execute()
    text_parts = []
    for element in doc.get("body", {}).get("content", []):
        paragraph = element.get("paragraph")
        if paragraph:
            for run in paragraph.get("elements", []):
                text_run = run.get("textRun")
                if text_run:
                    text_parts.append(text_run.get("content", ""))
    return "".join(text_parts)

def _call_claude(prompt: str) -> str:
    client = anthropic.Anthropic()

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return message.content[0].text

def create_cover_letter(docs_service, resume_doc_id: str):
    resume = _get_doc_text(docs_service, resume_doc_id)

    # get cover letter instructions
    with open('const/COVER_LETTER_CONSTRUCTION_INSTRUCTIONS.txt', 'r') as f:
        cover_letter_construction_instructions = f.read()

    # get promo_doc
    with open('const/promo_doc.txt', 'r') as f:
        promo_doc = f.read()

    # get job description
    with open('job_description.txt', 'r') as f:
        job_description = f.read()

    # model instructions
    with open('const/cover_letter_writing_prompt.txt', 'r') as f:
        prompt_template = f.read()

    with open('const/promo_doc.txt', 'r') as f:
        promo_doc = f.read()

    prompt = prompt_template.format(cover_letter_instructions=cover_letter_construction_instructions, resume=resume, promo_doc=promo_doc, job_description=job_description)


    return _call_claude(prompt)



