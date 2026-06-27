"""
Day 4 - Evaluation: Test Cases

Defines ground-truth test cases for each agent intent.
Each case has an input and the expected fields in the response.
"""

RESUME_CRITIQUE_TEST_CASES = [
    {
        "id": "rc_01",
        "description": "Basic resume with Python skills",
        "parsed_resume": {
            "name": "Jane Doe",
            "email": "jane@example.com",
            "phone": "9999999999",
            "skills": ["Python", "SQL", "Excel"],
            "experience": [
                {
                    "title": "Data Analyst Intern",
                    "company": "Acme Corp",
                    "duration": "6 months",
                    "description": "Analyzed data using Excel and SQL."
                }
            ],
            "education": [
                {
                    "degree": "B.E. Computer Science",
                    "institution": "Example University",
                    "year": "2024"
                }
            ],
            "summary": "Aspiring data analyst with internship experience."
        },
        "expected_fields": [
            "section_scores",
            "overall_score",
            "strengths",
            "weaknesses",
            "rewrite_suggestions",
            "ats_keywords_missing"
        ],
        "score_range": (0, 100),
    }
]

JD_ANALYSIS_TEST_CASES = [
    {
        "id": "jd_01",
        "description": "Data Analyst JD",
        "jd_text": """
We are looking for a Data Analyst to join our team.
Requirements:
- 2+ years of experience with SQL and Python
- Experience with Power BI or Tableau
- Strong communication skills
- Nice to have: knowledge of machine learning basics
Responsibilities:
- Build dashboards and reports
- Analyze business data to find insights
- Work closely with stakeholders
""",
        "expected_fields": [
            "role_title",
            "company_type",
            "must_have_skills",
            "nice_to_have_skills",
            "experience_required",
            "responsibilities",
            "red_flags"
        ],
    }
]

JD_MATCH_TEST_CASES = [
    {
        "id": "match_01",
        "description": "Strong match — candidate has all required skills",
        "parsed_resume": {
            "name": "Strong Candidate",
            "email": "strong@example.com",
            "skills": ["Python", "SQL", "Power BI", "Statistics", "Excel"],
            "experience": [
                {
                    "title": "Data Analyst",
                    "company": "BigCo",
                    "duration": "2 years",
                    "description": "Built dashboards in Power BI and analyzed data with Python."
                }
            ],
            "education": [{"degree": "B.Sc. Statistics", "institution": "Top University", "year": "2022"}],
            "summary": "Experienced data analyst."
        },
        "jd_text": """
Data Analyst role requiring Python, SQL, Power BI.
2 years experience required.
Nice to have: Tableau, ML knowledge.
""",
        "expected_fields": ["score", "matched_skills", "missing_skills", "recommendations", "verdict"],
        "expected_verdict_options": ["Strong Match", "Moderate Match", "Weak Match"],
        "min_score": 60,
    },
    {
        "id": "match_02",
        "description": "Weak match — candidate missing most required skills",
        "parsed_resume": {
            "name": "Weak Candidate",
            "email": "weak@example.com",
            "skills": ["MS Word", "PowerPoint"],
            "experience": [],
            "education": [{"degree": "B.A. History", "institution": "College", "year": "2023"}],
            "summary": "Recent graduate."
        },
        "jd_text": """
Senior Data Engineer requiring PySpark, Kafka, Airflow, AWS, Docker, Kubernetes.
5 years experience required.
""",
        "expected_fields": ["score", "matched_skills", "missing_skills", "recommendations", "verdict"],
        "expected_verdict_options": ["Strong Match", "Moderate Match", "Weak Match"],
        "max_score": 40,
    }
]

INTENT_DETECTION_TEST_CASES = [
    {"message": "Can you review my resume?", "expected_intent": "resume_critique"},
    {"message": "Critique my resume please", "expected_intent": "resume_critique"},
    {"message": "analyze this job description", "expected_intent": "jd_analysis"},
    {"message": "How do I match this job?", "expected_intent": "match"},
    {"message": "Am I a good fit for this role?", "expected_intent": "match"},
    {"message": "What skills should I add to my resume?", "expected_intent": "resume_question"},
    {"message": "How do I get into data science?", "expected_intent": "general"},
]
