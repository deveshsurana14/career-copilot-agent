"""
Day 3 - Tool: JD Matcher
Takes parsed resume dict + raw JD text.
Returns match score (0-100), matched skills, missing skills, and recommendations.
"""

import json



def match_resume_to_jd(parsed_resume: dict, jd_text: str, model) -> dict:
    """
    Compares parsed resume against a job description.
    Returns dict with: score, matched_skills, missing_skills, recommendations, verdict.
    """
    resume_summary = json.dumps(parsed_resume, indent=2)

    prompt = f"""
You are a hiring analyst. Compare the candidate's resume against the job description below.

Return ONLY valid JSON — no markdown, no explanation, no code fences.

Fields to return:
- score (integer 0-100, overall match percentage)
- matched_skills (list of strings — skills in resume that match JD requirements)
- missing_skills (list of strings — skills in JD that are NOT in resume)
- recommendations (list of 2-4 actionable strings the candidate should do to improve their fit)
- verdict (one of: "Strong Match", "Moderate Match", "Weak Match")
- jd_key_requirements (list of the top 5 must-have skills/qualities extracted from the JD)

Candidate Resume:
{resume_summary}

Job Description:
{jd_text}

Return ONLY the JSON object.
"""
    response = model.generate_content(prompt)
    raw = response.text.strip()

    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"error": raw}


def get_score_color(score: int) -> str:
    """Returns a hex color based on match score for UI display."""
    if score >= 75:
        return "#00C851"   # green
    elif score >= 50:
        return "#FF8800"   # orange
    else:
        return "#FF4444"   # red