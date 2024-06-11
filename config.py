########  GENERAL APP INFORMATION  ##############

APP_TITLE = "Guided Critical Analysis"
APP_INTRO = """In this guided case study, we\'ll both read the same case study. Then, you\'ll be guided through an analysis of the paper. Let\'s begin by reading the paper!

This is a **DEMO**, so sample answers are pre-filled and the article is one that is highly familiar to people.
"""

APP_HOW_IT_WORKS = """
 This is an **AI-Tutored Rubric exercise** that acts as a tutor guiding a student through a shared asset, like an article. It uses the OpenAI Assistants API with GPT-4. The **questions and rubric** are defined by a **faculty**. The **feedback and the score** are generarated by the **AI**. 

It can:

1. provide feedback on a student's answers to questions about an asset
2. roughly "score" a student to determine if they can move on to the next section.  

Scoring is based on a faculty-defined rubric on the backend. These rubrics can be simple (i.e. "full points if the student gives a thoughtful answer") or specific with different criteria and point thresholds. The faculty also defines a minimum pass threshold for each question. The threshold could be as low as zero points to pass any answer, or it could be higher. 

Using AI to provide feedback and score like this is a very experimental process. Some things to note: 

 - AIs make mistakes. Users are encourage to skip a question if the AI is not understanding them or giving good feedback. 
 - The AI might say things that it can't do, like "Ask me anything about the article". I presume further refinement can reduce these kinds of responses. 
 - Scoring is highly experimental. At this point, it should mainly be used to gauge if a user gave an approximately close answer to what the rubric suggests. It is not recommended to show the user the numeric score. 
 - Initial testing indicates that the AI is a very easy grader. This is probably good in this experiment, and it may be refined with different prompting. 
 """

SHARED_ASSET = {
}

HTML_BUTTON = {
    "url":"http://up.csail.mit.edu/other-pubs/las2014-pguo-engagement.pdf",
    "button_text":"Read PDF"
}

COMPLETION_MESSAGE = "You've reached the end! I hope you learned something!"
COMPLETION_CELEBRATION = False

SCORING_DEBUG_MODE = True

 ####### PHASES INFORMATION #########

PHASES =     {
    "org_name": {
        "type": "text_input",
        "label": """What is your name?""",
        "instructions": """The user will give you their name. Then, welcome the user to the exercise, and explain that you'll help them and provide feedback as they go. End your statement with "I will now give you your first question about the article." """,
        "scored_phase": True,
        "rubric": """
            1. Name
                    1 point - The user has provided a response in this thread. 
                    0 points - The user has not provided a response. 
        """,
        "button_label": "GO!",
        "minimum_score": 0
    },
    "about": {
        "type": "text_area",
        "height": 100,
        "label": """What is the article about?""",
        "instructions": "Provide helpful feedback for the following question. If the student has not answered the question accurately, then do not provide the correct answer for the student. Instead, use evidence from the article coach them towards the correct answer. If the student has answered the question correctly, then explain why they were correct and use evidence from the article. Question:",
        "scored_phase": True,
        "value": "This article investigates the impact of various video production decisions on student engagement in online educational videos, utilizing data from 6.9 million video watching sessions on the edX platform. It identifies factors such as video length, presentation style, and speaking speed that influence engagement, and offers recommendations for creating more effective educational content.",
        "rubric": """
                1. Length
                    1 point - Response is greater than or equal to 150 characters.
                    0 points - Response is less than 150 characters. 
                2. Key Points
                    2 points - The response mentions both videos AND student engagement rates
                    1 point - The response mentions either videos OR student engagement rates, but not both
                    0 points - The response does not summarize any important points in the article. 
        """,
        "minimum_score": 2,
        "allow_skip": True
    },
    "methdologies": {
        "type": "text_area",
        "height": 100,
       "label": "Summarize the methodology(s) used.",
       "instructions": "Provide helpful feedback for the following question. If the student has not answered the question accurately, then do not provide the correct answer for the student. Instead, use evidence from the article coach them towards the correct answer. If the student has answered the question correctly, then explain why they were correct and use evidence from the article. Question: Summarize the methodology(s) used.",
       "scored_phase": True,
       "value": "The study gathered data around video watch duration and problem attempts from the edX logs. These metrics served as a proxy for engagement. Then it compared that with video attributes like length, speaking rate, type, and production style, to determine how video production affects engagement.",
       "rubric": """
               1. Correctness
                   1 point - Response is correct and based on facts in the paper
                   0 points - Response is incorrect or not based on facts in the paper
               """,
       "minimum_score": 1,
       "allow_skip": True
    },
    "findings": {
        "type": "text_area",
        "height": 100,
        "label": "What were the main findings in the article?",
        "instructions": "Provide helpful feedback for the following question. If the student has not answered the question accurately, then do not provide the correct answer for the student. Instead, use evidence from the article coach them towards the correct answer. If the student has answered the question correctly, then explain why they were correct and use evidence from the article. Question: What were the main findings in the article?",
        "value": "Shorter videos are more engaging; Faster-speaking instructors hold students' attention better; High production value does not necessarily correlate with higher engagement;",
        "scored_phase": True,
        "rubric": """
            1. Correctness
                    2 points - Response includes two or more findings or recommendations from the study
                    1 point - Response includes only one finding or recommendation form the study
                    0 points - Response includes no findings or recommendations or is not based on facts in the paper
                    """,
        "minimum_score": 1,
        "allow_skip": True
    },
    "limitations": {
        "type": "text_area",
        "height": 100,
        "value": "The study cannot measure true student engagement, and so it must use proxies; The study could not track any offline video viewing; The study only used data from math/science courses;",
        "label": "What are some of the weaknesses of this study?",
        "instructions": "Provide helpful feedback for the following question. If the student has not answered the question accurately, then do not provide the correct answer for the student. Instead, use evidence from the article coach them towards the correct answer. If the student has answered the question correctly, then explain why they were correct and use evidence from the article. Question: What are some of the weaknesses of this study?",
        "scored_phase": True,
        "rubric": """
            1. Correctness
                    2 points - Response includes two or more limitations of the study
                    1 point - Response includes only one limitation in the study
                    0 points - Response includes no limitations or is not based on facts in the paper
                2. Total Score
                    The total sum of their scores. 
            """,
        "minimum_score": 1,
        "allow_skip": True
    }
}


########## AI ASSISTANT CONFIGURATION #######
ASSISTANT_NAME = "Guided Rubric"
ASSISTANT_INSTRUCTIONS = """
You are a helpful tutor that is guiding a university student through a critical appraisal of a scholarly journal article. You want to encourage the students ideas, but you also want those idea to be rooted in evidence from the journal article that you'll fetch via retrieval. 

Generally, you will be asked to provided feedback on the students answer based on the article, and you'll also sometimes be asked to score the submission based on a rubric which will be provided. More specific instructions will be given in the instructions via the API. """

LLM_CONFIGURATION = {
    "gpt-4-turbo":{
        "name":ASSISTANT_NAME,
        "instructions": ASSISTANT_INSTRUCTIONS,
        "tools":[{"type":"file_search"}],
        "model":"gpt-4-turbo",
        "temperature":0,
        "price_per_1k_prompt_tokens":.01,
        "price_per_1k_completion_tokens": .03
    },
    "gpt-4o":{
        "name":ASSISTANT_NAME,
        "instructions": ASSISTANT_INSTRUCTIONS,
        "tools":[{"type":"file_search"}],
        "model":"gpt-4o",
        "temperature":0,
        "price_per_1k_prompt_tokens":.005,
        "price_per_1k_completion_tokens": .015
    },
    "gpt-3.5-turbo":{
        "name":ASSISTANT_NAME,
        "instructions": ASSISTANT_INSTRUCTIONS,
        "tools":[{"type":"file_search"}],
        "model":"gpt-3.5-turbo-0125",
        "temperature":0,
        "price_per_1k_prompt_tokens":0.0005,
        "price_per_1k_completion_tokens": 0.0015
    }
}


ASSISTANT_THREAD = ""
ASSISTANT_ID_FILE = "assistant_id.txt"
