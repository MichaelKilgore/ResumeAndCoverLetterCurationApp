import os
from typing import Optional
import psycopg2
import argparse

def get_connection():
    return psycopg2.connect(
        dbname='resume_app',
    )


def insert_bullet_point(job_name: Optional[str], project_name: Optional[str],
                        sentence: str, value: int) -> None:
    if not (bool(job_name) ^ bool(project_name)):
        raise ValueError("Exactly one of job_name or project_name must be provided.")

    with get_connection() as conn:
        with conn.cursor() as cur:
            job_uuid = None
            project_uuid = None

            if job_name:
                cur.execute(
                    "SELECT uuid FROM job WHERE job_title = %s LIMIT 1",
                    (job_name,),
                )
                row = cur.fetchone()
                if not row:
                    raise ValueError(f"No job found with title: {job_name!r}")
                job_uuid = row[0]
            else:
                cur.execute(
                    "SELECT uuid FROM project WHERE project_name = %s LIMIT 1",
                    (project_name,),
                )
                row = cur.fetchone()
                if not row:
                    raise ValueError(f"No project found with name: {project_name!r}")
                project_uuid = row[0]

            cur.execute(
                """
                INSERT INTO bullet_point (sentence, value, job_uuid, project_uuid)
                VALUES (%s, %s, %s, %s)
                RETURNING uuid
                """,
                (sentence, value, job_uuid, project_uuid),
            )
            bullet_point_uuid = cur.fetchone()[0]



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Insert a bullet point into the resume database.')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--job', type=str, help='Job title to associate the bullet point with.')
    group.add_argument('--project', type=str, help='Project name to associate the bullet point with.')

    parser.add_argument('--sentence', type=str, required=True, help='The bullet point text.')
    parser.add_argument('--value', type=int, required=True, help='The value of the bullet point allows us to rank the bullet points')

    args = parser.parse_args()

    insert_bullet_point(
        job_name=args.job,
        project_name=args.project,
        sentence=args.sentence,
        value=args.value,
    )

