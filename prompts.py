def get_greeting():
    return (
        "🤖 **Welcome to TalentScout - Your AI Interview Assistant!**\n\n"
        "I'll help conduct a comprehensive technical interview by:\n"
        "- Collecting your basic information\n"
        "- Generating targeted questions based on your tech stack, experience, and role\n"
        "- Asking 3-4 questions per technology you mention\n\n"
        "Let's get started! Please enter your OpenRouter API key to begin."
    )


def get_candidate_prompt(candidate_info):
    
    questions = [
        ("Name", "Please share your full name."),
        ("Email", "What is your email address?"),
        ("Phone", "What is your phone number?"),
        ("Experience", "How many years of experience do you have?"),
        ("Position", "What position are you applying for?"),
        ("Location", "Where are you currently located?"),
        ("Tech Stack", "What is your tech stack? (e.g., Python, React, Node.js - separate with commas)")
    ]
    
    for key, prompt in questions:
        if key not in candidate_info:
            return key, prompt
    
    return None, None

def get_tech_question_generation_prompt(tech, experience, role):
    return f"""Based on the candidate's profile:
- Technology: {tech}
- Experience: {experience} years
- Role: {role}

Generate exactly 4 technical interview questions for {tech}.
Make questions appropriate for {experience} years of experience and {role} role.

Requirements:
- Questions should test practical knowledge and problem-solving
- Mix of conceptual and hands-on questions
- Appropriate difficulty level for the experience mentioned
- Clear and specific questions

Format your response as a simple numbered list:
1. [Question 1]
2. [Question 2]  
3. [Question 3]
4. [Question 4]

Do not include any explanations, just the questions."""

def get_relevance_check_prompt(question, user_response):
    return f"""Technical Question: {question}

Candidate Response: {user_response}

Is this response attempting to answer the technical question? 

Guidelines:
- If the candidate is asking about celebrities, movies, general knowledge, or completely unrelated topics, respond "NO"
- If they're attempting to answer the technical question (even if incorrectly or partially), respond "YES"
- If they're asking for clarification about the technical question, respond "YES"
- If they say "I don't know" or "I'm not sure", respond "YES"

Reply with only "YES" or "NO"."""

def get_interview_completion_message():
    return """🎉 **Congratulations! You have completed the technical interview.**

✅ All your responses have been recorded and saved
📊 Your answers will be reviewed by our team
📧 We'll get back to you soon with the results

Thank you for your time and effort!

Type 'exit' to end the session."""

def get_off_topic_warning():
    return """⚠️ **Please stay focused on the technical interview.**

I'm here to assess your technical skills. Let's get back to the interview question.

If you need clarification about the question, feel free to ask!"""

def get_error_message(error_type="general"):
    error_messages = {
        "api_key": "❌ Invalid API key. Please check your OpenRouter API key and try again.",
        "network": "🌐 Network error. Please check your connection and try again.",
        "generation": "⚠️ Unable to generate questions. Please try again or contact support.",
        "general": "❌ Something went wrong. Please try again."
    }
    
    return error_messages.get(error_type, error_messages["general"])

def get_progress_message(current, total):
    return f"📊 **Progress: {current}/{total} questions completed**"

def get_tech_stack_confirmation(tech_stack):
    technologies = [tech.strip() for tech in tech_stack.split(',')]
    tech_list = ", ".join(technologies)
    
    return f"""✅ **Tech Stack Confirmed:** {tech_list}

I'll generate 3-4 questions for each technology, totaling approximately {len(technologies) * 4} questions.

Ready to begin the technical assessment?"""