import requests
import pandas as pd
import os
import streamlit as st

def initialize_session_state():
    session_vars = {
        'stage': 'greeting',
        'chat_history': [],
        'candidate_info': {},
        'current_question_key': None,
        'tech_questions': [],
        'current_question_index': 0,
        'tech_answers': {}
    }
    
    for var, default_value in session_vars.items():
        if var not in st.session_state:
            st.session_state[var] = default_value
            
def validate_openrouter_key(api_key, model):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://chat.openai.com",  
        "Content-Type": "application/json",
    }
    body = {
        "model": model,
        "messages": [{"role": "user", "content": "Hello"}],
        "stream": False,
    }

    try:
        response = requests.post(url, headers=headers, json=body)
        return response.status_code == 200
    except Exception:
        return False


def get_openrouter_response(model, api_key, chat_history):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://chat.openai.com",
        "Content-Type": "application/json",
    }

    body = {
        "model": model,
        "messages": chat_history,
        "stream": False,
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ Failed to fetch response: {e}"


def generate_all_tech_questions(tech_stack, experience, role, model, api_key):
    technologies = [tech.strip() for tech in tech_stack.split(',')]
    all_questions = []
    
    for tech in technologies:
        questions = generate_questions_for_technology(tech, experience, role, model, api_key)
        all_questions.extend(questions)
    
    return all_questions

def generate_questions_for_technology(tech, experience, role, model, api_key):
    from prompts import get_tech_question_generation_prompt
    
    prompt = get_tech_question_generation_prompt(tech, experience, role)
    temp_chat = [{"role": "user", "content": prompt}]
    
    try:
        response = get_openrouter_response(model, api_key, temp_chat)
        return parse_questions_from_response(response, tech)
    except Exception as e:
        st.error(f"Error generating questions for {tech}: {e}")
        return []

def parse_questions_from_response(response, tech):
    questions = []
    
    for line in response.split('\n'):
        line = line.strip()
        if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
            if '.' in line:
                question = line.split('.', 1)[-1].strip()
            elif '-' in line:
                question = line.split('-', 1)[-1].strip()
            elif '•' in line:
                question = line.split('•', 1)[-1].strip()
            else:
                question = line.strip()
            
            if question and len(question) > 10: 
                questions.append(f"{tech}: {question}")
    
    return questions[:4]  

def check_response_relevance(question, user_response, model, api_key):
    from prompts import get_relevance_check_prompt
    
    prompt = get_relevance_check_prompt(question, user_response)
    temp_chat = [{"role": "user", "content": prompt}]
    
    try:
        response = get_openrouter_response(model, api_key, temp_chat)
        return "YES" in response.strip().upper()
    except Exception:
        return True 
    
import json
from datetime import datetime

def save_candidate_data(candidate_info, tech_answers):
    try:
        candidate_questions = [
            ("What is your full name?", "Name"),
            ("What is your email address?", "Email"),
            ("What is your phone number?", "Phone"),
            ("How many years of experience do you have?", "Experience"),
            ("What position are you applying for?", "Position"),
            ("Where are you currently located?", "Location"),
            ("What is your tech stack?", "Tech Stack"),
        ]

        row = {}
        for q_text, key in candidate_questions:
            row[q_text] = candidate_info.get(key, "")

        for question, answer in tech_answers.items():
            row[question] = answer

        df = pd.DataFrame([row])
        file_exists = os.path.exists("candidates.csv")
        df.to_csv("candidates.csv", mode="a", index=False, header=not file_exists)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_filename = f"candidate_{candidate_info.get('Name','unknown')}_{timestamp}.json"
        with open(json_filename, "w") as f:
            json.dump(row, f, indent=4)

        return True
    except Exception as e:
        st.error(f"❌ Error saving candidate data: {e}")
        return False



def get_candidate_summary(candidate_info):
    summary = []
    summary.append(f"**Name:** {candidate_info.get('Name', 'N/A')}")
    summary.append(f"**Email:** {candidate_info.get('Email', 'N/A')}")
    summary.append(f"**Experience:** {candidate_info.get('Experience', 'N/A')} years")
    summary.append(f"**Position:** {candidate_info.get('Position', 'N/A')}")
    summary.append(f"**Tech Stack:** {candidate_info.get('Tech Stack', 'N/A')}")
    summary.append(f"**Location:** {candidate_info.get('Location', 'N/A')}")
    
    return "\n".join(summary)