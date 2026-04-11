#!/bin/bash

./db_queries/create_sql_stuff.sh

./db_queries/create_company_and_jobs.sh

# ''' JOBS '''

# Amazon Software Development Engineer II

python3 src/insert_bullet_point.py --job 'Software Development Engineer II' --sentence 'Led the launch of promotion depth awareness features using AWS S3, Glue, Step Functions, EMR, and CDK, improving forecast accuracy by 10% during peak promotional periods.' --value 10



python3 src/insert_bullet_point.py --job 'Software Development Engineer II' --sentence 'Served as a technical point of contact for multiple forecasting initiatives, coordinating design reviews and driving delivery across ML and infrastructure teams.' --value 9
python3 src/insert_bullet_point.py --job 'Software Development Engineer II' --sentence 'Served as a technical point of contact for multiple forecasting initiatives, leading cross-functional collaboration across ML and infrastructure teams to coordinate design reviews and drive delivery.' --value 9


python3 src/insert_bullet_point.py --job 'Software Development Engineer II' --sentence 'Designed and implemented components of distributed forecasting services spanning data processing, training, inference, and analysis, partnering with ML scientists and platform teams to support multiple production pipelines processing millions of records.' --value 8

python3 src/insert_bullet_point.py --job 'Software Development Engineer II' --sentence 'Owned delivery of a demand anomaly detection system using AWS Lambda and Athena, reducing time-to-detection of upstream data issues across multiple production forecasting pipelines.' --value 7


# Amazon Software Development Engineer I

python3 src/insert_bullet_point.py --job 'Software Development Engineer I' --sentence 'Top performing contributor on a 10-engineer team for two consecutive years (~150 PRs/year), driving six internal launches.' --value 10

python3 src/insert_bullet_point.py --job 'Software Development Engineer I' --sentence 'Launched a Deals Optimization Tool, a React internal application used by teams in emerging markets, resulting in 36 Full-Time Engineer Weeks saved per year.' --value 9

python3 src/insert_bullet_point.py --job 'Software Development Engineer I' --sentence 'Wrote optimization logic in TypeScript for an internal authentication library used across multiple CI pipelines, reducing average integration test runtime by over 2x.' --value 8

python3 src/insert_bullet_point.py --job 'Software Development Engineer I' --sentence 'Mentored new engineers, helping to accelerate onboarding and improve their code quality' --value 7


# Washington Kids In Transition
python3 src/insert_bullet_point.py --job 'Software Engineer Intern' --sentence 'Built a full stack Django application that allows WKIT to better keep track of the ways in which they have helped kids, as well as pair kids with programs and scholarships.' --value 10
python3 src/insert_bullet_point.py --job 'Software Engineer Intern' --sentence "Leveraged 2-factor authentication and HTTPS to strengthen security of users' information." --value 9



# ''' PROJECTS '''


# AI Stock Forecasts
python3 src/insert_bullet_point.py --project 'AI Stock Forecasts' --sentence 'Built an end-to-end stock forecasting and trading system using PyTorch, including feature generation, model training, inference, and automated trade execution based on forecasted signals.' --value 10
python3 src/insert_bullet_point.py --project 'AI Stock Forecasts' --sentence 'Implemented daily trading execution on EC2 with data stored in S3, enabling automated backtesting and live strategy evaluation.' --value 9
python3 src/insert_bullet_point.py --project 'AI Stock Forecasts' --sentence 'Implemented evaluation logic for backtesting forecast-driven strategies, enabling comparison of trading performance across model versions.' --value 8


# Deep Swing Institutional System
python3 src/insert_bullet_point.py --project 'Deep Swing Institutional System' --sentence 'Architected an automated options decision making system that detects unusually large institutional trades, then assembles multi-source financial context, and uses an LLM to produce structured trading recommendations with confidence and pricing guidance.' --value 10
python3 src/insert_bullet_point.py --project 'Deep Swing Institutional System' --sentence 'Engineered integrations with Massive and FMP APIs to support real-time signal ingestion and contextual analysis across price action, earnings, insider activity, and corporate events.' --value 9
python3 src/insert_bullet_point.py --project 'Deep Swing Institutional System' --sentence 'Improved reliability of LLM-based decision workflows by enforcing typed outputs with Pydantic and persisting recommendation history in PostgreSQL for downstream retrieval and analysis.' --value 8
python3 src/insert_bullet_point.py --project 'Deep Swing Institutional System' --sentence 'Delivered real-time Telegram alerting for actionable buy recommendations, enabling fast user response to high-premium trade opportunities.' --value 7



# ''' SKILLS '''

python3 src/insert_skill.py --skill_type 'LANGUAGE' --skill 'Python'
python3 src/insert_skill.py --skill_type 'LANGUAGE' --skill 'Python3'
python3 src/insert_skill.py --skill_type 'LANGUAGE' --skill 'Java'
python3 src/insert_skill.py --skill_type 'LANGUAGE' --skill 'Scala'
python3 src/insert_skill.py --skill_type 'LANGUAGE' --skill 'SQL'
python3 src/insert_skill.py --skill_type 'LANGUAGE' --skill 'TypeScript'
python3 src/insert_skill.py --skill_type 'LANGUAGE' --skill 'CSS'
python3 src/insert_skill.py --skill_type 'LANGUAGE' --skill 'HTML'
python3 src/insert_skill.py --skill_type 'LANGUAGE' --skill 'PostgreSQL'

python3 src/insert_skill.py --skill_type 'SYSTEMS_AND_DATA' --skill 'Distributed Systems'
python3 src/insert_skill.py --skill_type 'SYSTEMS_AND_DATA' --skill 'Data Pipelines'
python3 src/insert_skill.py --skill_type 'SYSTEMS_AND_DATA' --skill 'ML Infrastructure'
python3 src/insert_skill.py --skill_type 'SYSTEMS_AND_DATA' --skill 'Forecasting Systems'
python3 src/insert_skill.py --skill_type 'SYSTEMS_AND_DATA' --skill 'S3'
python3 src/insert_skill.py --skill_type 'SYSTEMS_AND_DATA' --skill 'EMR'
python3 src/insert_skill.py --skill_type 'SYSTEMS_AND_DATA' --skill 'Glue'
python3 src/insert_skill.py --skill_type 'SYSTEMS_AND_DATA' --skill 'Step Functions'
python3 src/insert_skill.py --skill_type 'SYSTEMS_AND_DATA' --skill 'Lambda'
python3 src/insert_skill.py --skill_type 'SYSTEMS_AND_DATA' --skill 'Apache Airflow'
python3 src/insert_skill.py --skill_type 'SYSTEMS_AND_DATA' --skill 'Athena'
python3 src/insert_skill.py --skill_type 'SYSTEMS_AND_DATA' --skill 'ECR'
python3 src/insert_skill.py --skill_type 'SYSTEMS_AND_DATA' --skill 'Spark'
python3 src/insert_skill.py --skill_type 'SYSTEMS_AND_DATA' --skill 'Terraform'

python3 src/insert_skill.py --skill_type 'TOOLS' --skill 'CI/CD'
python3 src/insert_skill.py --skill_type 'TOOLS' --skill 'Git'
python3 src/insert_skill.py --skill_type 'TOOLS' --skill 'AI Tools'
python3 src/insert_skill.py --skill_type 'TOOLS' --skill 'React'
python3 src/insert_skill.py --skill_type 'TOOLS' --skill 'Docker'


