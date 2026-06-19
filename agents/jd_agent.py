"""
Day 3 - Agent: JD Agent

Responsible for:
- Extracting structured requirements from a job description
- Scoring how well a candidate fits against those requirements
"""

import json


JD_AGENT_SYSTEM = """
You are a technical recruiter who deeply understands job descriptions.

You extract structured requirements and evaluate candidate fit objectively.

Always return valid JSON only.
"""


def extract_jd_requirements(jd_text: str, model) -> dict:
    """
    Parses a raw JD into structured requirements.

    Returns dict with:
    - role_title
    - company_type
    - must_have_skills
    - nice_to_have_skills
    - experience_required
    - responsibilities
    - red_flags
    """

    prompt = f"""
{JD_AGENT_SYSTEM}

Parse this job description and return ONLY valid JSON.


Job Description:

{jd_text}


Return JSON with exactly these fields:


role_title


company_type


must_have_skills


nice_to_have_skills


experience_required


responsibilities


red_flags



company_type must be one of:

startup

MNC

product company

service company

unknown


Return ONLY JSON.

"""


    response = model.generate_content(

        prompt

    )


    raw = response.text.strip()


    if raw.startswith("```"):

        raw = raw.split("```")[1]

        if raw.startswith("json"):

            raw = raw[4:]


    raw = raw.strip()


    try:


        return json.loads(

            raw

        )


    except json.JSONDecodeError:


        return {

            "error": "Failed to parse JD",


            "raw": raw

        }



def score_candidate_for_jd(

        parsed_resume: dict,

        jd_requirements: dict,

        model,

        vector_store=None

):


    context_note = ""


    prompt = f"""

{JD_AGENT_SYSTEM}


Score this candidate against the job requirements below.


Return ONLY valid JSON.



Candidate Resume:


{json.dumps(parsed_resume, indent=2)}



Job Requirements:


{json.dumps(jd_requirements, indent=2)}



Return JSON with EXACTLY these fields:



fit_score


must_have_coverage


skill_gap_severity


interview_readiness


one_liner


apply_recommendation




Example:



{{


"fit_score":78,


"must_have_coverage":0.75,


"skill_gap_severity":"medium",


"interview_readiness":[

"SQL joins",

"Power BI",

"Statistics"

],


"one_liner":"Candidate meets most requirements but lacks dashboard experience.",


"apply_recommendation":"Apply with a strong cover letter"


}}



Return ONLY JSON.


"""


    response = model.generate_content(

        prompt

    )


    raw = response.text.strip()


    if raw.startswith("```"):


        raw = raw.split("```")[1]


        if raw.startswith("json"):


            raw = raw[4:]


    raw = raw.strip()


    try:


        return json.loads(

            raw

        )


    except json.JSONDecodeError:


        return {


            "error": "Failed to score candidate",


            "raw": raw

        }