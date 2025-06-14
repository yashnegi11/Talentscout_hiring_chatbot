import streamlit as st
from prompts import get_greeting, get_candidate_prompt
from utils import (
    validate_openrouter_key, 
    generate_all_tech_questions, 
    check_response_relevance,
    save_candidate_data,
    initialize_session_state
)

st.set_page_config(page_title="TalentScout Chatbot")
st.title(':blue[Chatbot] :material/robot_2:')

initialize_session_state()

if st.session_state.stage == 'greeting':
    st.info(get_greeting())
    with st.form("api_form"):
        model = st.selectbox('Select a free OpenRouter model', (
            "deepseek/deepseek-chat-v3-0324:free",
            "google/gemma-3-27b-it:free",
            "meta-llama/llama-4-maverick:free",
            "mistralai/devstral-small:free"
        ))
        api_key = st.text_input('Enter your OpenRouter API key', type='password',
                                help='Generate your API key from https://openrouter.ai')
        submitted = st.form_submit_button("Connect")

        if submitted:
            if validate_openrouter_key(api_key, model):
                st.success("API key validated successfully.")
                st.session_state.api_key = api_key
                st.session_state.model = model
                st.session_state.stage = 'collect_info'

                key, prompt = get_candidate_prompt(st.session_state.candidate_info)
                if prompt:
                    st.session_state.current_question_key = key
                    st.session_state.chat_history.append({"role": "assistant", "content": prompt})
                st.rerun()
            else:
                st.warning("⚠️ Invalid API key. Please try again.")
                st.stop()

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Type your response here...")
if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    if 'exit' in user_input.lower():
        save_candidate_data(st.session_state.candidate_info, st.session_state.tech_answers)
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": "Thank you for your time. Ending the chat. 🙏"
        })
        st.session_state.stage = "done"
        st.success("Candidate data saved.")
        st.rerun()

    if st.session_state.stage == "collect_info":
        if st.session_state.current_question_key:
            st.session_state.candidate_info[st.session_state.current_question_key] = user_input
            st.session_state.current_question_key = None

        key, prompt = get_candidate_prompt(st.session_state.candidate_info)
        if prompt:
            st.session_state.current_question_key = key
            st.session_state.chat_history.append({"role": "assistant", "content": prompt})
        else:
            st.session_state.stage = "generating_questions"
            st.session_state.chat_history.append({
                "role": "assistant", 
                "content": (
                    "You may type \"exit\" at any time to leave the chat.\n"
                    "If you are unsure about any question, feel free to respond with \"I don't know\" or \"IDK.\"\n"
                    "Your responses will be recorded and reviewed by our team.\n\n"
                    "Please type \"OK\" to begin the technical stack questions."
                )
            })
        st.rerun()

    elif st.session_state.stage == "generating_questions":
        tech_stack = st.session_state.candidate_info.get("Tech Stack", "")
        experience = st.session_state.candidate_info.get("Experience", "0")
        role = st.session_state.candidate_info.get("Position", "")
        
        st.session_state.tech_questions = generate_all_tech_questions(
            tech_stack, experience, role, st.session_state.model, st.session_state.api_key
        )
        
        if st.session_state.tech_questions:
            st.session_state.stage = "tech_questions"
            st.session_state.current_question_index = 0
            
            first_question = st.session_state.tech_questions[0]
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": f"Let's begin the technical interview! 🚀\n\n**Question 1/{len(st.session_state.tech_questions)}:**\n{first_question}"
            })
        else:
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": "❌ Sorry, I couldn't generate questions. Please try again."
            })
        st.rerun()

    elif st.session_state.stage == "tech_questions":
        current_question = st.session_state.tech_questions[st.session_state.current_question_index]
        
        is_relevant = check_response_relevance(
            current_question, user_input, st.session_state.model, st.session_state.api_key
        )
        
        if not is_relevant:
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": "I'm here to conduct a technical interview. Please focus on answering the technical question. Let me repeat the question:\n\n" + current_question
            })
        else:
            question_key = f"Q{st.session_state.current_question_index + 1}_{current_question.split(':')[0]}"
            st.session_state.tech_answers[question_key] = user_input
            
            st.session_state.current_question_index += 1
            
            if st.session_state.current_question_index < len(st.session_state.tech_questions):
                next_question = st.session_state.tech_questions[st.session_state.current_question_index]
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": f"Great! Moving to the next question.\n\n**Question {st.session_state.current_question_index + 1}/{len(st.session_state.tech_questions)}:**\n{next_question}"
                })
            else:
                st.session_state.stage = "completed"
                save_candidate_data(st.session_state.candidate_info, st.session_state.tech_answers)
                
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": "🎉 Congratulations! You have completed the technical interview.\n\nAll your responses have been recorded. Thank you for your time!\n\nType 'exit' to end the session."
                })
        st.rerun()

    elif st.session_state.stage == "completed":
        if 'exit' in user_input.lower():
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": "Thank you for participating in the interview. Have a great day! 👋"
            })
        else:
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": "The interview has been completed. Type 'exit' to end the session."
            })
        st.rerun()