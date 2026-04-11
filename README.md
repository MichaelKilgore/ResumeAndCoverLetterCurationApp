# ResumeAndCoverLetterCurationApp

### How it Works

The purpose of this script is to automate the process of keyword matching via Job Scan. I found that a lot of times you are just rewording bullet points so this script automates that process. When you apply for a new job, look at the keywords you are missing and add them to your bullet points, and over time your database will grow and you won't have to add new bullet points all the time.

### Set Up Instructions

To use this tool go into the db_queries/init_base_stuff.sh file and and db_queries/create_sql_stuff.sh and update it to use your bullet points and jobs and skills then create a template like this:

![Resume Template Screenshot](img/resume_template_screenshot.png)

copy paste the TEMPLATE ID into global variable at top of src/create_google_doc.py

Then update:

```
    company = 'Drillbit'

    raw_hard_skills: str = 'Computer Science, postgresql, typescript, tailwind, node.js, docker, Jest, LLMs, CSS, NPM'
    raw_soft_skills: str = 'Collaboration'
```

the variables in the create_google_doc file. (I'm pulling these keywords from jobscan).

Finally make sure to set up authentication for google doc. (I won't go into details just ask chatgpt)

After you've done that you can just run src/create_google_doc.py and it should work.

### Hindsights 20/20

1. When I created this script I only aimed to make what I was currently do to 


