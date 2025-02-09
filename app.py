from dotenv import load_dotenv
load_dotenv() # loading all environment variables from .env file

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

gemini_pro_model = genai.GenerativeModel('gemini-pro')

## Function to load Gemini model pro and get responses
def get_gemini_response(query):
    return gemini_pro_model.generate_content(query).text


## Initialize the streamlit app

st.set_page_config(page_title="Q&A Demo")

st.header("Gemini LLM Application")

input=st.text_input("Input: ", key="input")

submit = st.button("Ask the question")

## When submit is clicked

if submit:
    response = get_gemini_response(input)
    st.subheader("The response is:")
    st.write(response)

#print(get_gemini_response("List some exo planets"))
