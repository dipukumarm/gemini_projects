# Handling multiple pdf documents using Gemini.

from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate

import os

load_dotenv() # Load all environment variables from .env file

# Configure genai module

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))


#For the left side on UI to upload and read pdfs
def read_pdf_docs(pdf_docs):
    text=""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text;

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

def get_conversational_chain():
    prompt_template = """
    From the context provided, please answer the questions as detailed a possible.
    If answer in not present in the context, please say "I don't get it from the context provided", but don;t provide wrong answers\n\n
    Context:\n {context}\n
    Question:\n{question}\n

    Answer:
    """
    # Function to load Gemini pro model for dealing with image and text and get response
    model=ChatGoogleGenerativeAI(model='gemini-pro', temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input=["context", "question"])

    chain=load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

def user_input(question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db = FAISS.local_local("faiss_index", embeddings)
    docs = new_db.similarity_search(question)
    chain = get_conversational_chain()

    response = chain({"input_documents": docs, "question": question}, return_only_outputs=True)

    print (response)
    st.write("Reply: ", response['output_text'])


# For UI
def main():
    st.set_page_config("PDF Analyzer")
    st.header("PDF Analyzer")
    question = st.text_input("What do you want to learn form the PDFs?")

    if question:
        user_input(question)
    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader("Upload pdfs and submit", accept_multiple_files=True)
        if(st.button("Submit")):
            with st.spinner("Processing..."):
                text = read_pdf_docs(pdf_docs)
                chunks = get_text_chunks(text)
                get_vector_store(chunks)
                st.success("PDF's processed successfully.")



if __name__ == "__main__":
    main()