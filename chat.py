
from dotenv import load_dotenv

load_dotenv() 

import streamlit as st
import os 
import google.generativeai as genai 

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini Pro Model
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response


# Initialize our Streamlit app

st.set_page_config(page_title= "Q&A Demo")

st.header("Gemini LLM QA Chatbot")

# Initialize session state for chat history if it doesnt exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input = st.text_input("Input: ", key="input")
submit = st.button("Ask the quesion")

if submit and input:
    response = get_gemini_response(input)

    # Add user query and response to session chat history
    st.session_state['chat_history'].append(('You', input))
    st.subheader("The Response is: ")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(('Bot', chunk.text))

st.subheader("The Chat History is: ")

for role, text in st.session_state['chat_history']:
    st.write(f"{role}:{text}")
