# 🤖 TalentScout Chatbot

TalentScout is an AI-powered Hiring Assistant chatbot designed to automate the technical screening process for candidates. It collects essential candidate information, dynamically generates role-specific technical questions using OpenRouter models, and evaluates responses — all within a conversational UI powered by Streamlit.

---

## 🧠 Project Overview

TalentScout simplifies the initial screening process by:

- Collecting basic candidate details via chat (name, email, tech stack, experience, etc.)
- Automatically generating 3–4 technical interview questions per technology using free OpenRouter models
- Validating the relevance of candidate responses
- Saving candidate responses in both CSV and JSON format
- Providing an engaging and structured conversational experience

---

## ⚙️ Installation Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/talentscout_chatbot.git
cd talentscout_chatbot
```

### 2. (Optional) Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> If `requirements.txt` is not present, here's a sample:

```txt
streamlit
requests
pandas
```

### 4. Run the Streamlit app

```bash
streamlit run app.py
```

---

## 🚀 Usage Guide

1. Launch the app using `streamlit run app.py`
2. Select a **free model** from OpenRouter (e.g., deepseek, gemma, llama).
3. Enter your **OpenRouter API key** (get one from [https://openrouter.ai](https://openrouter.ai))
4. Answer the chatbot's questions to provide your:
   - Name
   - Email
   - Phone
   - Experience
   - Position
   - Location
   - Tech Stack (comma-separated)
5. Confirm to start the technical interview.
6. Respond to technical questions generated per your tech stack.
7. Type `exit` anytime to end the chat and save your data.

---

## 🛠️ Technical Details

### 💻 Libraries Used

- **Streamlit** – Interactive chat UI
- **Requests** – API integration with OpenRouter
- **Pandas** – Storing data in `.csv` format
- **OS, JSON, Datetime** – File handling and timestamping

### 🤖 Model Integration

- Uses **free models** via [OpenRouter](https://openrouter.ai) API
- Supported models:  
  - `deepseek/deepseek-chat-v3-0324:free`  
  - `google/gemma-3-27b-it:free`  
  - `meta-llama/llama-4-maverick:free`  
  - `mistralai/devstral-small:free`

### 🧱 Architecture Overview

```
Streamlit App (app.py)
│
├── prompts.py         → All LLM prompt templates
├── utils.py           → API calls, response handling, question generation, data saving
└── candidates.csv     → Appended with each interview session
```

---

## ✨ Prompt Design

### 🟢 Candidate Info Collection

Prompted one-by-one using:

```python
("Name", "Please share your full name.")
("Email", "What is your email address?")
...
```

Each prompt is sequentially displayed until all key information is collected.

### 🧠 Technical Question Generation

Dynamic prompt crafted as:

```
Based on the candidate's profile:
- Technology: Python
- Experience: 2 years
- Role: Backend Developer

Generate exactly 4 technical interview questions for Python...
```

The model responds with questions formatted as a numbered list.

### ✅ Relevance Check Prompt

After each answer, the model checks whether the response is on-topic:

```
Is this response attempting to answer the technical question?
...
Reply with only "YES" or "NO".
```

---

## ⚔️ Challenges & Solutions

### 1. **Prompt Formatting Issues**
   - **Challenge**: Some models responded with explanations or non-list content.
   - **Solution**: Prompts were explicitly formatted to request numbered questions only, and responses were post-processed using regex to extract valid questions.

### 2. **Response Relevance Check**
   - **Challenge**: Candidates might go off-topic or provide irrelevant answers.
   - **Solution**: A lightweight relevance-checking prompt was created to ensure the answer fits the question context before proceeding.

### 3. **File Handling & Storage**
   - **Challenge**: Persisting user responses and multiple session data.
   - **Solution**: Both `.csv` and `.json` file formats are used to store structured data per session using pandas and the `json` module.

---

## 📂 Deliverables

- ✅ Fully documented codebase (`app.py`, `utils.py`, `prompts.py`)
- ✅ Chat-based UI for the interview process
- ✅ Candidate data saved as `.csv` and `.json`
- ✅ README file with installation, usage, and design notes

---

## 📬 Contact

If you'd like to contribute or collaborate, feel free to reach out or fork the project.  
Happy Hiring! 🚀
