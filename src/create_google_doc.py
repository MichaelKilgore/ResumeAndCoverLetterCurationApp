TEMPLATE_DOC_ID = '13p9Gh0NtuCkAFIfWjdl3yhSB_kDBjJFGiHsLo9uuxAQ'

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os
import pickle

from generate_replacements import generate_replacements

SCOPES = [
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/drive"
]

def get_services():
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as f:
            creds = pickle.load(f)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.pickle", "wb") as f:
            pickle.dump(creds, f)

    docs_service = build("docs", "v1", credentials=creds)
    drive_service = build("drive", "v3", credentials=creds)
    return docs_service, drive_service


def copy_template(drive_service, template_doc_id, new_title):
    copied_file = drive_service.files().copy(
        fileId=template_doc_id,
        body={"name": new_title}
    ).execute()
    return copied_file["id"]


def replace_placeholders(docs_service, doc_id, replacements):
    requests = []

    for placeholder, value in replacements.items():
        requests.append({
            "replaceAllText": {
                "containsText": {
                    "text": placeholder,
                    "matchCase": True
                },
                "replaceText": value
            }
        })

    docs_service.documents().batchUpdate(
        documentId=doc_id,
        body={"requests": requests}
    ).execute()


def main():
    company = 'Drillbit'

    raw_hard_skills: str = 'Computer Science, postgresql, typescript, tailwind, node.js, docker, Jest, LLMs, CSS, NPM'
    raw_soft_skills: str = 'Collaboration'

    jd_key_words = raw_hard_skills.split(', ') + raw_soft_skills.split(', ')

    replacements = generate_replacements(jd_key_words)

    docs_service, drive_service = get_services()

    new_doc_id = copy_template(
        drive_service,
        TEMPLATE_DOC_ID,
        f"{company} Resume"
    )

    replace_placeholders(docs_service, new_doc_id, replacements)

    print(f"Created doc: https://docs.google.com/document/d/{new_doc_id}/edit")


if __name__ == "__main__":
    main()

