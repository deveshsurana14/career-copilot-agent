"""
Day 3 - Agent: Orchestrator

Routes user queries to the appropriate agent.

Intent categories:

resume_critique
jd_analysis
match
resume_question
general
"""

import json


from agents.resume_agent import (
    critique_resume,
    get_resume_improvement_chat
)


from agents.jd_agent import (
    extract_jd_requirements,
    score_candidate_for_jd
)


from tools.jd_matcher import (
    match_resume_to_jd
)



INTENT_KEYWORDS = {


    "resume_critique": [

        "review my resume",

        "critique my resume",

        "score my resume",

        "what's wrong with my resume",

        "improve my resume",

        "resume feedback",

        "check my resume",

        "analyze my resume"

    ],



    "jd_analysis": [

        "analyze this job",

        "analyze the jd",

        "what does this job require",

        "parse this job description",

        "extract requirements",

        "job description"

    ],



    "match": [

        "how do i match",

        "match score",

        "do i fit",

        "am i a good fit",

        "compare my resume",

        "match my resume",

        "fit for this role"

    ],


}



def detect_intent(


        user_message: str,

        model

) -> str:



    lower = user_message.lower()



    for intent, keywords in INTENT_KEYWORDS.items():



        if any(

                kw in lower

                for kw in keywords

        ):


            return intent



    prompt = f"""

Classify this message into EXACTLY one category


resume_critique


jd_analysis


match


resume_question


general



User message:


{user_message}



Return ONLY category name.


"""



    response = model.generate_content(

        prompt

    )



    detected = (

        response.text

        .strip()

        .lower()

        .replace('"', '')

        .replace("'", "")

    )



    valid = {


        "resume_critique",

        "jd_analysis",

        "match",

        "resume_question",

        "general"

    }



    if detected in valid:


        return detected



    return "general"




def route(


        user_message: str,


        model,


        session_memory,


        parsed_resume=None,


        jd_text=None

):



    intent = detect_intent(

        user_message,

        model

    )



    #####################################################
    # Resume Critique
    #####################################################


    if intent == "resume_critique":



        if not parsed_resume:



            return {


                "intent": intent,


                "response_type": "text",


                "data":

                "Please upload a resume first.",


                "agent_used":

                "orchestrator"

            }



        result = critique_resume(

            parsed_resume,

            model

        )



        session_memory.update(

            "last_resume_critique",

            result

        )



        return {


            "intent": intent,


            "response_type": "structured",


            "data": result,


            "agent_used":

            "resume_agent"

        }




    #####################################################
    # JD Analysis
    #####################################################


    elif intent == "jd_analysis":



        text_to_analyze = (

            jd_text

            or

            user_message

        )



        result = extract_jd_requirements(

            text_to_analyze,

            model

        )



        session_memory.update(

            "last_jd_analysis",

            result

        )



        return {


            "intent": intent,


            "response_type": "structured",


            "data": result,


            "agent_used":

            "jd_agent"

        }




    #####################################################
    # Resume Match
    #####################################################


    elif intent == "match":



        if not parsed_resume:



            return {


                "intent": intent,


                "response_type": "text",


                "data":

                "Please upload a resume first.",


                "agent_used":

                "orchestrator"

            }



        if not jd_text:



            return {


                "intent": intent,


                "response_type": "text",


                "data":

                "Paste a Job Description first.",


                "agent_used":

                "orchestrator"

            }



        result = match_resume_to_jd(

            parsed_resume,

            jd_text,

            model

        )



        session_memory.update(

            "last_match_result",

            result

        )



        return {


            "intent": intent,


            "response_type": "structured",


            "data": result,


            "agent_used":

            "jd_matcher"

        }




    #####################################################
    # Resume Question
    #####################################################


    elif intent == "resume_question":



        if not parsed_resume:



            return {


                "intent": intent,


                "response_type": "text",


                "data":

                "Upload your resume first.",


                "agent_used":

                "orchestrator"

            }



        answer = get_resume_improvement_chat(


            user_message,


            parsed_resume,


            model

        )



        return {


            "intent": intent,


            "response_type": "text",


            "data": answer,


            "agent_used":

            "resume_agent"

        }




    #####################################################
    # General Career Chat
    #####################################################


    else:



        history = session_memory.get_all()



        context = ""


        if history:



            context = (

                f"User context from session:\n"

                f"{json.dumps(history)}\n\n"

            )



        prompt = f"""

You are Career Copilot.


{context}


User:


{user_message}



Provide practical,

specific,

career advice.


"""



        response = model.generate_content(

            prompt

        )



        return {


            "intent": "general",


            "response_type": "text",


            "data":

            response.text.strip(),


            "agent_used":

            "gemini_direct"

        }