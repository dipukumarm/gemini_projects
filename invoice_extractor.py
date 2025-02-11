# App to extract information from invoices in different languages

from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

load_dotenv() #load all environment variables from .env file
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## function to load Gemini flash model for dealing with image and text and get response

model=genai.GenerativeModel("gemini-1.5-flash")


def get_gemini_response(input, image, prompt):
    response=model.generate_content([input, image[0], prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        #Extract bytes from the file
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded.")

st.set_page_config(page_title="Extractor")
st.header("Invoice Extractor")
input=st.text_input("Prompt : ", key="input")
uploaded_file = st.file_uploader("Select the image of invoice ...", type=["jpg", "jpeg", "png"])

image=""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Image under consideration: ", use_column_width=True)

submit=st.button("Extract Information")

input_prompt="""
I'm working with invoices in different languages. I need your help to extract required information form the uploaded invoice.
"""

# If submit button is clicked.

if submit:
    image_data = input_image_details(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)
    st.subheader("Extracted Information:")
    st.write(response)

