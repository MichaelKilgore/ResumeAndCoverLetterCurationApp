import os
from typing import Optional
import psycopg2
import argparse

def get_connection():
    return psycopg2.connect(
        dbname='resume_app',
    )


def insert_skill(skill: str, skill_type: str) -> None:

    with get_connection() as conn:
        with conn.cursor() as cur:
            job_uuid = None
            project_uuid = None


            cur.execute(
                """
                INSERT INTO skill (skill_type, skill)
                VALUES (%s, %s)
                RETURNING uuid
                """,
                (skill_type, skill),
            )
            _ = cur.fetchone()[0]



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Insert a bullet point into the resume database.')

    parser.add_argument('--skill_type', type=str, help='skill type')
    parser.add_argument('--skill', type=str, help='skill')

    args = parser.parse_args()

    insert_skill(
        skill=args.skill,
        skill_type=args.skill_type,
    )

