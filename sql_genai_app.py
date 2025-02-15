# LLM Application for tqt to sql

#Flow: Query/Prompt -> LLM -> Gemini Pro -> Query -> SQL DB -> Response

#Steps
# SQL Lite as DB and insert few records using python  - refer sql_handler.py
# LLM App -> Gemini Pro -> SQL Lite DB -> Response

from dotenv import load_dotenv
load_dotenv() # loads environment variables

import streamlit as st
import os
import sqlite3

import google.generativeai as genai

## Configure API Key
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

#Get the LLM model
model = genai.GenerativeModel("gemini-pro")

# Load Gemini model and return sql query as response
def get_sql_query_from_gemini(question, prompt):
    response = model.generate_content([prompt[0], question])
    return response.text

# To retrieve query results from the sql db
def retrieve_query_results(query, db):
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    connection.commit()
    connection.close()
    for row in rows:
        print(row)
    return rows

# Define your prompt
prompt =[
"""
Context is to convert questions in English language to sql query.
The sql database name is STUDENT and has following columns - NAME, CLASS, SECTION and MARKS\n\nFor example, \n Example 1 - How many entries of records are present? the SQL command will be somethin glike this - SELECT COUNT(*) FROM STUDENT;
\nExample 2 - Tell me all the students studying in Data Sience class?, the SQL command will be something like this - SELECT * FROM STUDENT where CLASS="Data Sience"; also the sql code should not have ``` in the beginning or end and sql word in the output
"""
]

#Stremlit app

st.set_page_config(page_title="SQL Query Interface")
st.header("Use Gemeny Model to Query SQL DB")
question = st.text_input("Enter your question here: ", key="input")
submit = st.button("Ask the question") 


#If submit is clicked
if submit:
    response = get_sql_query_from_gemini(question, prompt)
    print(response)
    data = retrieve_query_results(response, "student_data.db")
    st.subheader("The response is: ")
    for row in data:
        print(row)
        st.write(row)