import streamlit as st
import mysql.connector
import os
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load Hugging Face model and tokenizer
model_name = "mrm8488/t5-small-finetuned-wikiSQL"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Function to connect to MySQL database and execute SQL query
def execute_sql_query(sql):
    connection = None  # Initialize connection variable
    try:
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE"),
            port=int(os.getenv("MYSQL_PORT"))  # Convert MYSQL_PORT to integer
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            return rows
    except mysql.connector.Error as e:
        st.error(f"Error connecting to MySQL: {e}")
    finally:
        if connection and connection.is_connected():  # Check if connection is not None before using it
            cursor.close()
            connection.close()

# Function to translate a natural language question to an SQL query using Hugging Face model
def translate_question_to_sql(question):
    inputs = tokenizer.encode("translate English to SQL: " + question, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(inputs, max_length=150, num_beams=4, early_stopping=True)
    sql_query = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Check if the generated query matches known patterns
    if "SELECT * FROM table" in sql_query:
        if "student" in question.lower():
            sql_query = "SELECT * FROM student"
        # Add other table name overrides as necessary

    return sql_query

# Streamlit App
st.set_page_config(page_title="SQL Query Chat App")
st.header("SQL Query Chat App")

question = st.text_input("Input SQL query or question: ", key="input")
submit = st.button("Submit")

if submit:
    if question.strip():  # Check if input is not empty
        sql_query = translate_question_to_sql(question)
        st.write(f"Generated SQL Query: {sql_query}")
        try:
            # Debug: Print the SQL query being executed
            st.write(f"Executing SQL Query: {sql_query}")
            rows = execute_sql_query(sql_query)

            st.subheader("Results:")
            if rows:
                for row in rows:
                    st.write(row)
            else:
                st.write("No results found.")
        except mysql.connector.Error as e:
            st.error(f"Error executing SQL query: {e}")
    else:
        st.warning("Please enter a valid SQL query or question.")
