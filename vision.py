from dotenv import load_dotenv
load_dotenv()

import streamlit as st

import os

import google.generativeai as genai

from PIL import Image


genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))


gemini_pro_model = genai.GenerativeModel('gemini-1.5-flash')

## Function to load Gemini model pro and get responses
def get_gemini_response(input, image):
    response = ''
    if input.strip() !='':
        response =  gemini_pro_model.generate_content([input, image])
    else:
        response =  gemini_pro_model.generate_content(image)
    return response.text


## Initialize streamlit app

st.set_page_config(page_title="Gemini Image Demo")

st.header("Gemini Application")
input = st.text_input("Input Prompt: ", key="input")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me about this image - ")

## When submit is clicked

if submit:
    response = get_gemini_response(input, image)
    st.subheader("The response is:")
    st.write(response)



