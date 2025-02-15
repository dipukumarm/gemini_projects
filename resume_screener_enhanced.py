
# Approach: PDF->Text->LLM->Response

import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv('GENAI_API_KEY'))

# Gemeni pro response

def get_llm_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text


# PDF to Text
def convert_pdf_to_text(pdf_file):
    pdf_reader = pdf.PdfReader(pdf_file)
    text = ''
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text


# Prompt Template

input_prompt="""
Hey Act Like a skilled ATS(Application Tracking System)
with a deep understanding of tech field, software engineering,data science,data analytics
and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving the resume. Assign the percentage Matching based 
on job description and the missing keywords with high accuracy
resume:{text}
description:{jd}

I want the response in one single string having the structure
{{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}}
"""

st.title("Resume Screener")
st.text("Analyze PDF Resume")
jd = st.text_area("Paste the Job Description here")
uploaded_file = st.file_uploader("Upload your resume", type="pdf", help="Upload in  PDF format")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text = convert_pdf_to_text(uploaded_file)
        response = get_llm_response(input_prompt)
        st.subheader("Response")
        st.write(response)
    else:
        st.write("Please upload a file")