# Approach: PDF->Image->LLM->Response

import base64
import io
from dotenv import load_dotenv

load_dotenv() # loads environment variables

import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

#Function to get response from Gemini model from the question, prompt and the resume as pdf content
def get_gemini_response(prompt, pdf_content, context):
    model = genai.GenerativeModel("gemini-1.5-flash") #gemini-1.5-flash
    response = model.generate_content([prompt, pdf_content[0], context])
    return response.text

# PDF processing
def pdf_processing(uploaded_pdf):
    if uploaded_pdf is not None:
        #Convert PDF to Image
        images = pdf2image.convert_from_bytes(uploaded_pdf.read())

        first_page = images[0]

        #Convert Image to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode() # Encode to base64 format
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded.")
    

## Streamlit app

st.set_page_config(page_title="Resume Screener")
st.header("Application Tracking System [ATS]")
job_description = st.text_area("Enpetr the Job Description : ", key="input")
uploaded_pdf = st.file_uploader("Upload the resume in PDF format ...", type=["pdf"])

if uploaded_pdf is not None:
    st.write("Resume uploaded successfully.")

action1 = st.button("Summarize the resume")

prompt_for_action1 = """
You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
Please share your professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements. 
"""
action2 = st.button("How can you improve skills?")

prompt_for_action2 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. 
Please highlight what the candidate can do to improve on the key skills listed as per the job description.
Please consider the current skills highlighted in the resume while providing your feedback.
"""

action3 = st.button("What are the keywords that are missing?")

prompt_for_action3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. Give me the list ok keywords missing in the resume, compared to the job description.
"""

action4 = st.button("Percentage match")
prompt_for_action4 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

if action1:
    if uploaded_pdf is not None:
        pdf_content = pdf_processing(uploaded_pdf)
        response = get_gemini_response(prompt_for_action1, pdf_content, job_description)
        st.subheader("Response:")
        st.write(response)
    else:
        st.error("Please upload the resume first.")

if action2: 
    if uploaded_pdf is not None:
        pdf_content = pdf_processing(uploaded_pdf)
        response = get_gemini_response(prompt_for_action2, pdf_content, job_description)
        st.subheader("Response:")
        st.write(response)
    else:
        st.error("Please upload the resume first.")

if action3:
    if uploaded_pdf is not None:
        pdf_content = pdf_processing(uploaded_pdf)
        response = get_gemini_response(prompt_for_action3, pdf_content, job_description)
        st.subheader("Response:")
        st.write(response)
    else:
        st.error("Please upload the resume first.")

if action4:
    if uploaded_pdf is not None:
        pdf_content = pdf_processing(uploaded_pdf)
        response = get_gemini_response(prompt_for_action4, pdf_content, job_description)
        st.subheader("Response:")
        st.write(response)
    else:
        st.error("Please upload the resume first.")