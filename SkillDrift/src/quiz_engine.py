import json
import os
import random

try:
    from google import genai
    client = genai.Client(api_key="AIzaSyDT6JrTvPFFeqXoDvB9bFPOQdiEbXWbJG8")
    API_AVAILABLE = True
except:
    API_AVAILABLE = False

LOCAL_QUESTIONS_PATH = "data/local_questions"

def get_subjects(domain):
    return {
        "Programming Languages": ["C", "C++", "Java", "Python"],
        "Web Development": ["HTML", "React", "Node.js"],
        "CSE Core": ["DBMS", "DSA", "OS"],
        "Data Science & AI": ["ML", "DL", "Statistics"]
    }.get(domain, [])

def get_questions(subject, count=20):
    questions = []

    if API_AVAILABLE:
        try:
            prompt = f"""
            Generate EXACTLY {count} high-quality MCQs from {subject}.
            RULES:
            - All questions must be DIFFERENT
            - Include conceptual + practical questions
            - Each question must have 4 meaningful options
            - Provide correct answer EXACTLY matching one option
            FORMAT STRICTLY:
            [
              {{"q": "Question text?", "o": ["Option A","Option B","Option C","Option D"], "a": "Correct Option"}}
            ]
            """
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )
            text = response.text
            start = text.find("[")
            end = text.rfind("]") + 1
            data = json.loads(text[start:end])
            questions = data
        except Exception as e:
            print("API failed, using local questions:", e)

    if not questions:
        filename = os.path.join(LOCAL_QUESTIONS_PATH, f"{subject}.json")
        if os.path.exists(filename):
            with open(filename, "r") as f:
                all_qs = json.load(f)
                if len(all_qs) >= count:
                    questions = random.sample(all_qs, count)
                else:
                    questions = all_qs
        else:
            raise FileNotFoundError(f"Local question file {filename} not found!")

    for q in questions:
        options = q["o"]
        random.shuffle(options)
        q["o"] = options

    return questions
