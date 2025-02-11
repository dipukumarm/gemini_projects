from dotenv import load_dotenv
load_dotenv()

import streamlit as st

import os

import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## function to load Gemini pro model and get response

model=genai.GenerativeModel("gemini-pro")
chat=model.start_chat(history=[])

def get_gemini_response(question):
    response=chat.send_message(question, stream=True)
    return response

st.set_page_config(page_title="Q&A Demo")

st.header("Gemini LLM Application")

# session state initialization
if 'history' not in st.session_state:
    st.session_state['history']=[]

input = st.text_input("Input : ", key="input")

submit = st.button("Ask the question - ")

if submit and input:
    response = get_gemini_response(input)
    ## Add query and response to history
    st.session_state['history'].append(('You:', input))
    st.subheader("Response :")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['history'].append(('Gemini:', chunk.text))

st.subheader("Chat History :")
for role, text in st.session_state['history']:
    st.write(f"{role}:{text}")