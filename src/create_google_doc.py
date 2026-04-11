TEMPLATE_DOC_ID = '13p9Gh0NtuCkAFIfWjdl3yhSB_kDBjJFGiHsLo9uuxAQ'

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os
import pickle
from create_cover_letter import create_cover_letter

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


def replace_placeholders(docs_service, doc_id, replacements) -> str:
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

    return doc_id

def create_cover_letter_doc(docs_service, drive_service, company: str, cover_letter_text: str) -> str:
    file_metadata = {
        "name": f"{company} Cover Letter",
        "mimeType": "application/vnd.google-apps.document"
    }
    new_file = drive_service.files().create(body=file_metadata, fields="id").execute()
    doc_id = new_file["id"]

    docs_service.documents().batchUpdate(
        documentId=doc_id,
        body={
            "requests": [
                {
                    "insertText": {
                        "location": {"index": 1},
                        "text": cover_letter_text
                    }
                }
            ]
        }
    ).execute()

    return doc_id

def main():
    company = 'Drillbit'

    docs_service, drive_service = get_services()

    answer = input("\nDo you want to generate a resume (y/n): ").strip().lower()

    with open('job_description.txt', 'r') as f:
        job_description = f.read()

    new_doc_id = TEMPLATE_DOC_ID
    if answer == 'y':

        replacements = generate_replacements(job_description)


        new_doc_id = copy_template(
            drive_service,
            TEMPLATE_DOC_ID,
            f"{company} Resume"
        )

        replace_placeholders(docs_service, new_doc_id, replacements)

        print(f"Created resume doc: https://docs.google.com/document/d/{new_doc_id}/edit")

    answer = input("\nDo you want to generate a cover letter (y/n): ").strip().lower()

    if answer == 'y':
        cover_letter_text = create_cover_letter(docs_service, resume_doc_id=new_doc_id)

        cover_letter_doc_id = create_cover_letter_doc(docs_service, drive_service, company, cover_letter_text)

        print(f"Created cover letter doc: https://docs.google.com/document/d/{cover_letter_doc_id}/edit")



if __name__ == "__main__":
    main()




