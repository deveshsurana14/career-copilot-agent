"""
Day 2 - Tool: Resume Parser
Extracts raw text from uploaded PDF, then uses Gemini to return
structured JSON: name, email, skills, experience, education, summary.
"""

import json
import pypdf
import google.generativeai as genai


def extract_text_from_pdf(uploaded_file) -> str:
    """Extract raw text from a Streamlit uploaded PDF file."""
    reader = pypdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.strip()


def parse_resume_with_gemini(raw_text: str, model) -> dict:
    """
    Send raw resume text to Gemini and get back structured JSON.
    Returns a dict with keys: name, email, phone, skills, experience, education, summary.
    """
    prompt = f"""
You are a resume parser. Extract the following fields from the resume text below and return ONLY valid JSON — no markdown, no explanation, no code fences.

Fields to extract:
- name (string)
- email (string)
- phone (string)
- skills (list of strings)
- experience (list of objects: each with "title", "company", "duration", "description")
- education (list of objects: each with "degree", "institution", "year")
- summary (2-3 sentence professional summary of the candidate)

Resume Text:
{raw_text}

Return ONLY the JSON object.
"""
    response = model.generate_content(prompt)
    
    if not response.text:
        return {"parse_error": "Gemini returned empty response"}
  
    raw = response.text.strip()

    # Strip markdown code fences if Gemini returns them anyway
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # Fallback: return raw text under a key so the UI can still show something
        return {"raw_text": raw_text, "parse_error": raw}


def get_resume_text_and_parsed(uploaded_file, model) -> tuple[str, dict]:
    """
    Convenience wrapper: returns (raw_text, parsed_dict).
    Call this from app.py.
    """
    raw_text = extract_text_from_pdf(uploaded_file)
    parsed = parse_resume_with_gemini(raw_text, model)
    return raw_text, parsed