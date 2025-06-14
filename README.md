# 🤖 TalentScout - AI Technical Interview Chatbot

TalentScout is a smart, interactive Streamlit-based chatbot designed to simulate a technical interview experience. It leverages free OpenRouter LLMs to dynamically generate role-specific and experience-based questions. All user responses are validated and stored neatly for later review.

---

## 🚀 Features

- Collects candidate details (name, email, phone, experience, position, location, tech stack)
- Generates tailored questions (3–4 per technology)
- Checks response relevance using AI
- Logs all interview questions and answers in structured format
- Fully built with free resources (OpenRouter API & Streamlit)

---

## 🗂️ Project Structure

talentscout_chatbot/
├── app.py              # Streamlit app logic

├── prompts.py          # Prompt templates and helper generators

├── utils.py            # API validation, question generation, data saving

├── candidates.csv      # Saved interview records (questions + responses)

├── venv/               # Virtual environment

├── __pycache__/        # Python cache files

└── README.md           # Project documentation


---

## 🛠️ Installation Guide

1. **Clone this repository**
```
git clone https://github.com/your-username/talentscout_chatbot.git
cd talentscout_chatbot
```
2. **Create a virtual environment**
```
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```
3. **Install required libraries**
```
pip install -r requirements.txt
```
4. **Run the Streamlit app**
```
streamlit run app.py
```
## 🔐 OpenRouter API Key Setup
Visit OpenRouter.ai

Create a free account and get your API key

Paste the key when prompted in the app

Select a free model like deepseek, gemma, or llama-4-maverick

## 🧠 How It Works
Candidate select a model and Enter their API key.

Candidate provides basic information

The app generates 3-4 technical questions per mentioned technology

Each response is validated for relevance

All data is stored in a clean tabular format (candidates.csv)

Sample stored format:

Name	Email	Tech Stack	Q1_Python	Q2_Streamlit	...
Yash	y@gmail.com	Python, Streamlit	your answer	your answer	...

## 📌 Use Cases
HR tech pre-screening tool

Resume + quiz pipeline for hiring

AI-based self-assessment tool for developers

## 🧰 Tech Stack
Python

Streamlit

OpenRouter (LLMs)

Pandas

## 📈 Future Improvements
Resume file upload + parsing

PDF export of interview

Integration with HR systems

Score generation or feedback

## 👨‍💻 Author
Yash Pal Singh Negi
📫 [yashnegiuk02@gmail.com]
🎯 Machine Learning & AI enthusiast

