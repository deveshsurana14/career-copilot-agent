"""
Day 3 - Agent: Resume Agent

Responsible for:
- Critiquing resumes
- ATS scoring
- Section level feedback
- Rewrite suggestions
- Missing keywords detection
"""

import json


RESUME_AGENT_SYSTEM = """
You are an expert resume reviewer with 10+ years of experience in tech hiring.

Your job is to give honest, actionable feedback on resumes.

Be specific.

Reference actual content from the resume.

Always return valid JSON only.
"""


def critique_resume(parsed_resume: dict, model, vector_store=None) -> dict:
    """
    Analyze resume and return structured feedback.

    Returns:

    - section_scores
    - overall_score
    - strengths
    - weaknesses
    - rewrite_suggestions
    - ats_keywords_missing
    """

    context_note = ""

    prompt = f"""
{RESUME_AGENT_SYSTEM}

Analyze this resume.

Return ONLY valid JSON.


Resume Data:

{json.dumps(parsed_resume, indent=2)}


Return JSON with EXACTLY these fields:


section_scores

overall_score

strengths

weaknesses

rewrite_suggestions

ats_keywords_missing



Example format


{{
"section_scores":{{

"summary":8,

"experience":7,

"skills":9,

"education":8

}},

"overall_score":81,


"strengths":[

"...",

"..."

],


"weaknesses":[

"...",

"..."

],


"rewrite_suggestions":[

{{

"section":"experience",

"issue":"Weak bullet point",

"suggestion":"Use metrics"

}}

],


"ats_keywords_missing":[

"Power BI",

"Docker"

]

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

            "error": "Failed to parse critique",


            "raw": raw

        }



def get_resume_improvement_chat(


        user_question: str,

        parsed_resume: dict,

        model

):


    prompt = f"""

You are an expert career coach.


Resume:


{json.dumps(parsed_resume,indent=2)}



Question:


{user_question}



Answer clearly.

Give practical advice.


"""


    response = model.generate_content(

        prompt

    )


    return response.text.strip()