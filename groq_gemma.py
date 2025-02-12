import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from dotenv import load_dotenv

from langchain_community.vectorstores import FAISS # DB for vectorstore
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings # vector embedding model

from dotenv import load_dotenv


load_dotenv()

# Load required API keys from .env file

api_key_groq = os.getenv('GROQ_API_KEY')
api_key_google = os.getenv('GOOGLE_API_KEY')


# Streamlit app configuration

st.title("Gemma Model Usage Through Groq - Document Q&A")

llm = ChatGroq(groq_api_key=api_key_groq, model="gemma2-9b-it")

# Setup prompt template

prompt = ChatPromptTemplate.from_template(
    """
    Use only the provided context while answering the question
    Please make sure the response is as accurate as possible based on the question.
    <context>
    {context}
    <context>
    Question: {input}
    """
)

# Function to read pdfs, chunk them and store to vectorstore

def vector_embedding():
    if "vectors" not in st.session_state:
        st.session_state.embeddings = GoogleGenerativeAIEmbeddings(
            google_api_key=api_key_google,
            model="models/embedding-001",
            temperature=0.0,
            max_output_tokens=512
        )
        st.session_state.loader = PyPDFDirectoryLoader("./us_census_data") # Data ingestion
        st.session_state.docs = st.session_state.loader.load() # Document loading
        st.session_state.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.docs)
        
        st.session_state.vectors = FAISS.from_documents(st.session_state.final_documents, st.session_state.embeddings)



if st.button("Creating vector store"):
    vector_embedding()
    st.success("Vector store created successfully")

import time


prompt1 = st.text_input("Enter your question here")

if prompt1:
    document_chain=create_stuff_documents_chain(llm, prompt)
    retriever = st.session_state.vectors.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    start=time.process_time()
    response = retrieval_chain.invoke({"input": prompt1})
    print("Response time :",time.process_time()-start)
    st.write(response['answer'])
    #Use expander of streamlit
    with st.expander("Document Similarity Search"):
        # Find relevant chunks
        for i, doc in enumerate(response['context']):
            st.write(doc.page_content)
            st.write("----------")