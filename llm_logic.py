IS_DEV_ENV = False

import os
import json
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai


# --------------------------------------------------------------------------------
# Logging function
# --------------------------------------------------------------------------------

def write_log(parameter_text, newline=False):
    if IS_DEV_ENV:
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if newline:
            log_entry = f"\n[{current_datetime}] {parameter_text}\n"
        else:
            log_entry = f"[{current_datetime}] {parameter_text}\n"

        with open("logs_api.txt", 'a') as file:
            file.write(log_entry)

    else:
        return


write_log("Code file started", True)


# --------------------------------------------------------------------------------
# Constants:
# --------------------------------------------------------------------------------

if IS_DEV_ENV:
    print("-"*100)
    print("-----  [###] MAKE SURE YOU ARE RUNNING CODE IN VENV [###] ---")
    print("-"*100)
else:
    print("🪄🔮 Started API code file")


chat_session, model = "", ""

with open('fallback_data.json', 'r') as f:
    fallback_content = json.load(f)

article1 = fallback_content["1"]["para"]
json1 = fallback_content["1"]["que_json"]

article2 = fallback_content["2"]["para"]
json2 = fallback_content["2"]["que_json"]


# --------------------------------------------------------------------------------
# Prompts:
# --------------------------------------------------------------------------------

que_engine_sys_instr = """
You are an expert in the quiz generation and you are well known for creating quizzes precisely based on the given context only.
You never make up the things and stick to just given context, unless you are explicitly asked to do otherwise. 
Your quizzes are on point for learners assessment.
You are reputed to follow one of your four methods for responding to given context:

Method-1: When it is needed to generate mcq question, you always output in following json format:
{
    "que_no": integer (number of the question),
    "type": string "MCQ", 
    "question": string,
    "options": [list containing 4 strings of options],
    "hint": string (small hint for correct answer if possible else 'Sorry!')
    "answer": integer (index of correct ans in list from 1 to 4)
}

Method-2: When it is needed to generate multiple correct question (where minimum 1 and maximum all options can be correct answer), you always output in following json format:
{
    "que_no": integer (number of the question),
    "type": string "Multiple", 
    "question": string,
    "options": [list containing 4 strings of options],
    "hint": string (small hint for correct answer if possible else 'Sorry!')
    "answer": list of integers (index of correct answers in options list from 1 to 4)
}

Method-3: When it is needed to generate numerical answer type question, you always output in following json format:
{
    "que_no": integer (number of the question),
    "type": string "Numeric", 
    "question": string,
    "hint": string (small hint for correct answer if possible else 'Sorry!')
    "answer": integer (exact answer in integer, just the integer is allowed, not float. Round off the float to integer mathematically if required.)
}

Method-4: When it is needed to generate true false answer type question, you always output in following json format:
{
    "que_no": integer (number of the question),
    "type": string "Bool", 
    "question": string,
    "hint": string (small hint for correct answer if possible else 'Sorry!')
    "answer": "True" or "False" (exact answer in string saying true or false)
}

Remember, for all the answer indices, start indexing options from 1 and not from 0. And, stick to given context strictly for accurate answers and dont try to make up answers.
"""

que_engine_one_shot_que = """
Question:
    Generate a question each of type MCQ, Multiple Correct, numerical and Boolean with given context. Just reply the json objects for the questions embedded in one single list and strictly no other text before and after it. Answer should just contain the list with questions' objects within it.
\n
Context:
{
    The Earth orbits around the Sun, which is the center of our solar system. The time it takes for the Earth to complete one orbit around the Sun is approximately 365.25 days, leading to the concept of a leap year every four years. The Earth's axis is tilted, which causes the different seasons. The moon orbits the Earth and affects the tides due to its gravitational pull. Solar eclipses occur when the Moon passes between the Earth and the Sun, casting a shadow on the Earth.
}
"""

que_engine_one_shot_resp = """
[
    {
        "que_no": 1,
        "type": "MCQ", 
        "question": "What is the time it takes for the Earth to complete one orbit around the Sun?",
        "options": ["365 days", "365.25 days", "366 days", "364 days"],
        "hint": "It leads to the concept of a leap year.",
        "answer": 2
    },
    {
        "que_no": 2,
        "type": "Multiple", 
        "question": "Which of the following statements are true about the Earth and the Moon?",
        "options": [
            "The Earth orbits around the Sun.",
            "The moon orbits the Earth.",
            "The Earth’s axis is straight.",
            "The Moon affects the tides."
        ],
        "hint": "There are two correct statements.",
        "answer": [1, 2, 4]
    },
    {
        "que_no": 3,
        "type": "Numeric", 
        "question": "How many days does it take for the Earth to complete one orbit around the Sun?",
        "hint": "Exclude the fraction and just enter the integer number.",
        "answer": 365
    },
    {
        "que_no": 4,
        "type": "Bool", 
        "question": "Solar eclipses occur when the Moon passes between the Earth and the Sun.",
        "hint": "Think about the alignment of the Sun, Moon, and Earth.",
        "answer": "True"
    }
]
"""

# You reply in very specific format and are known for the perfectness of your responses in these aspects: You generate paragraph which are close to reality and do not create imaginary things unless explicitly mentioned. Your paragraphs contain some factual details, some numbers. You have to generate 3 to 4 paragraphs which collectively fall between 900 to 1200 words, with an absolute maximum of 1500 words.
generate_para_sys_instr = """
You are an expert in providing the paragraphs based on the given topic.
You reply in very specific format and are known for the perfectness of your responses in these aspects: You generate paragraph which are close to reality and do not create imaginary things unless explicitly mentioned. Your paragraphs contain some factual details, some numbers. You have to generate 3 to 4 paragraphs which collectively fall between 600 to 800 words, with an absolute maximum of 1000 words.
Your paragraphs are useful as they are directly used to generate the quizzes!
Your format of reply is strictly this:
{
    "topic": string (topic or title of the paragraph in not more than one line. You can use the given topic as it is or modify it slightly if needed),
    "paragraph": string (3-4 paragraphs), 
}
Remember, stick to given output format strictly.
"""


# --------------------------------------------------------------------------------
# Main Functions:
# --------------------------------------------------------------------------------

def set_up_requirements(api_key: str):
    global genai

    try:
        API_KEY = api_key

        genai.configure(api_key=API_KEY)
        write_log('Api key read')
        return "Key authentication successful!!!"

    except Exception as e:
        write_log('Api key error')
        write_log(e)
        return "Error"


def start_question_engine():
    global chat_session, model, genai

    generation_config = {
        "temperature": 1.5,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        # "response_mime_type": "text/plain",
        "response_mime_type": "application/json",
    }

    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        generation_config=generation_config,
        system_instruction=que_engine_sys_instr,
    )

    try:
        chat_session = model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [
                        que_engine_one_shot_que,
                    ],
                },
                {
                    "role": "model",
                    "parts": [
                        que_engine_one_shot_resp,
                    ],
                },
            ]
        )

        write_log('Initialized Model chat successfully')
        return "Started Question Generation Engine Successfully..."

    except Exception as e:
        write_log('Initialized Model failed')
        write_log(e)
        return "Error"


def generate_quiz(context: str, no_of_ques: int = 15, difficulty: str = "Easy"):
    # total: (MCQ, multiple, numerical, bool),
    splits = {
        5: (2, 1, 1, 1),
        10: (4, 2, 2, 2),
        15: (6, 2, 2, 5),
        20: (8, 4, 4, 4)
    }

    if no_of_ques not in [5, 10, 15, 20]:
        no_of_ques = 15
    mcq, multiple, numerical, boolean = splits.get(no_of_ques)

    if difficulty not in ['Easy', 'Medium', 'Hard']:
        difficulty = 'Easy'

    try:
        response = chat_session.send_message(
            f"""
                Question:
                    Generate {mcq} MCQ, {multiple} Multiple Correct, {numerical} numerical and {boolean} Boolean questions with given context.
                    The difficulty level of the questions should be {difficulty}.
                    Just reply the json objects for the questions embedded in one single list and strictly no other text before and after it. Answer should just contain the list with questions objects within it.
                \n
                Context:
                    {context}
                \n
                Response:
                    
            """
        )

        ans = response.text

        # If it is plain text, rather md formatted, pre-process it.
        if ans.startswith("```"):
            ans = ans[ans.find('['):ans.rfind(']')+1]

        response_json = json.loads(ans)
        que_cnt = len(response_json)

        write_log('Quiz created with API call')
        return [que_cnt, response_json]

    except Exception as e:
        write_log('Quiz API call failed')
        write_log(e)
        return "Error, Quiz API call failed"


def generate_para(topic: str):
    global genai
    chat_session_2 = ""
    model_tmp = ""

    generation_config = {
        "temperature": 1.0,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        # "response_mime_type": "text/plain",
        "response_mime_type": "application/json",
    }

    model_tmp = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        generation_config=generation_config,
        system_instruction=generate_para_sys_instr,
    )

    try:
        chat_session_2 = model_tmp.start_chat(
            history=[
            ]
        )
    except Exception as e:
        write_log('Paragraph Generator Initialization failed')
        write_log(e)
        return "Error"

    try:
        response = chat_session_2.send_message(
            f"""
                Question:
                    Generate a topic based on Topic.
                \n
                Topic:
                    {topic}
                \n
                Response:
                    
            """
        )

        ans = response.text

        # If it is plain text, rather md formatted, pre-process it.
        if ans.startswith("```"):
            ans = ans[ans.find('['):ans.rfind(']')+1]

        response_json = json.loads(ans)

        write_log('Paragraph generated with API call')
        return response_json

    except Exception as e:
        write_log('Paragraph API call failed')
        write_log(e)
        return "Error"


def blank_call_default():
    import random
    r = random.randint(1, 2)
    if (r == 1):
        write_log('Default context-1 and json delivered')
        que_cnt = len(json1)
        return [que_cnt, article1, json1]
    else:
        write_log('Default context-2 and json delivered')
        que_cnt = len(json2)
        return [que_cnt, article2, json2]


if __name__ == "__main__":
    # Example usage
    load_dotenv(".env")
    API_KEY = os.getenv("API", "")
    print(set_up_requirements(API_KEY))

    print(start_question_engine())
    resp = generate_quiz(article1, 5, 'Hard')

    # Create a json file and save locally:
    with open("temp_quiz_output.json", "w") as f:
        json.dump(resp, f, indent=4)

    # import bbs_color_terminal as b
    # b.json_file_create_msedge(resp)

    print(*blank_call_default())
