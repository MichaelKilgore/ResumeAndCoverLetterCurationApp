#!/bin/bash

DB_NAME="resume_app"
DB_USER="michael"

echo "Inserting companies, jobs, and projects..."

sudo -u "$DB_USER" psql -d "$DB_NAME" <<EOF

-- Amazon
WITH ins_amazon AS (
    INSERT INTO company (company_name)
    VALUES ('Amazon')
    RETURNING uuid
)
INSERT INTO job (job_title, start_date, end_date, company_uuid)
SELECT * FROM (VALUES
    ('Software Development Engineer II', '2025-07-01'::DATE, '2026-01-31'::DATE),
    ('Software Development Engineer I',  '2022-08-15'::DATE, '2025-06-30'::DATE)
) AS jobs(job_title, start_date, end_date)
CROSS JOIN ins_amazon;

-- Washington Kids In Transition
WITH ins_wkit AS (
    INSERT INTO company (company_name)
    VALUES ('Washington Kids In Transition')
    RETURNING uuid
)
INSERT INTO job (job_title, start_date, end_date, company_uuid)
SELECT 'Software Engineer Intern', '2021-10-01'::DATE, '2022-02-01'::DATE, uuid
FROM ins_wkit;

-- Projects
INSERT INTO project (project_name, project_type) VALUES
    ('AI Stock Forecasts',             'Personal Project'),
    ('Deep Swing Institutional System', 'Upwork Contract');

EOF

echo "Done."
