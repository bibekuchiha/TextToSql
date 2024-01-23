from dotenv import load_dotenv
import os
import sqlite3
import streamlit as st
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Genai with API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get response from Google Gemini Model
def get_gemini_response(question, prompt):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content([prompt[0], question])
        return response.text
    except Exception as e:
        print(f"Error generating Gemini response: {e}")
        return None

# Function to execute SQL query and fetch results
def execute_sql_query(sql, db_path):
    try:
        with sqlite3.connect(db_path) as conn:
            cur = conn.cursor()
            cur.execute(sql)
            return cur.fetchall()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    except Exception as e:
        print(f"Error executing query: {e}")
        return []

# Streamlit App Configuration
st.set_page_config(page_title="SQL Query Generator")
st.header("Retrieve SQL Data Using Natural Language")

# Define the prompt for the Gemini model
prompt=[
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, 
    SECTION \n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ;
    \nExample 2 - Tell me all the students studying in Data Science class?, 
    the SQL command will be something like this SELECT * FROM STUDENT 
    where CLASS="Data Science"; 
    also the sql code should not have ``` in beginning or end and sql word in output

    """


]
# Streamlit Input
question = st.text_input("Enter your question:", key="input")
submit = st.button("Submit Query")

# Process the input
if submit and question:
    sql_response = get_gemini_response(question, prompt)
    if sql_response:
        query_results = execute_sql_query(sql_response, "student.db")
        if query_results:
            st.subheader("Query Results:")
            for row in query_results:
                st.write(row)
        else:
            st.error("No results found or error in query.")
    else:
        st.error("Error generating SQL query from the provided question.")
