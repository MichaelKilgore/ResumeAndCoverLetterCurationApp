#!/bin/bash

DB_NAME="resume_app"
DB_USER="postgres"

# sudo -u postgres psql

echo "Dropping database $DB_NAME if it exists..."
sudo -u "$DB_USER" psql -c "DROP DATABASE IF EXISTS $DB_NAME;"

echo "Creating database $DB_NAME..."
sudo -u "$DB_USER" psql -c "CREATE DATABASE $DB_NAME;"

echo "Creating tables..."
sudo -u "$DB_USER" psql -d "$DB_NAME" <<EOF

-- Drop tables in reverse dependency order
DROP TABLE IF EXISTS keywords;
DROP TABLE IF EXISTS bullet_point;
DROP TABLE IF EXISTS skills;
DROP TABLE IF EXISTS job;
DROP TABLE IF EXISTS company;
DROP TABLE IF EXISTS project;

-- Drop enum types
DROP TYPE IF EXISTS item_type_enum;
DROP TYPE IF EXISTS skill_type_enum;

-- Create enum types
CREATE TYPE skill_type_enum AS ENUM ('LANGUAGE', 'SYSTEMS_AND_DATA', 'TOOLS');

-- Table 1: Company
CREATE TABLE company (
    uuid        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_name TEXT NOT NULL
);

-- Table 2: Job
CREATE TABLE job (
    uuid         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_title    TEXT NOT NULL,
    start_date   DATE,
    end_date     DATE,
    company_uuid UUID NOT NULL REFERENCES company(uuid) ON DELETE CASCADE
);

-- Table 3: Personal Project
CREATE TABLE project (
    uuid                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_name              TEXT NOT NULL,
    project_type              TEXT NOT NULL
);

-- Table 4: Bullet Point
CREATE TABLE bullet_point (
    uuid                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sentence                  TEXT NOT NULL,
    value                     INT NOT NULL,
    job_uuid                  UUID REFERENCES job(uuid) ON DELETE CASCADE,
    project_uuid              UUID REFERENCES project(uuid) ON DELETE CASCADE,
    CONSTRAINT bullet_point_owner_check CHECK (
        (job_uuid IS NOT NULL AND project_uuid IS NULL) OR
        (job_uuid IS NULL AND project_uuid IS NOT NULL)
    )
);

-- Table 5: Skills
CREATE TABLE skill (
    uuid        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    skill_type  skill_type_enum NOT NULL,
    skill       TEXT NOT NULL
);


EOF

echo "Done."
