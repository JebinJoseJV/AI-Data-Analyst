import os
import sqlite3
import pandas as pd
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

def initialize_database():
    return sqlite3.connect("data.db", check_same_thread=False)

def upload_and_store_data(uploaded_file, conn):
    if uploaded_file is not None:
        file_extension = uploaded_file.name.split(".")[-1].lower()
        if file_extension == "csv":
            df = pd.read_csv(uploaded_file)
        elif file_extension in ["xls", "xlsx"]:
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Unsupported file format. Please upload a CSV or Excel file.")
            return None
        
        st.subheader("Preview of Uploaded Data")
        st.dataframe(df.head())
        
        df.to_sql("data", conn, if_exists="replace", index=False)
        st.success("File uploaded and data stored in the database successfully!")
        return df
    return None

def get_sql_query(user_query, api_key):
    groq_sys_prompt = ChatPromptTemplate.from_template("""
                    You are an expert in converting English questions to SQL query!
                    The SQL database has the name data and has dynamic columns.
                    Generate SQL queries dynamically based on the available columns.
                    Now convert the following question in English to a valid SQL Query: {user_query}.
                    No preamble, only valid SQL please.
                                                       """)
    model="llama3-8b-8192"
    llm = ChatGroq(
        groq_api_key=api_key,
        model_name=model
    )
    chain = groq_sys_prompt | llm | StrOutputParser()
    response = chain.invoke({"user_query": user_query})
    return response

def return_sql_response(sql_query, conn):
    try:
        return conn.execute(sql_query).fetchall()
    except Exception as e:
        st.error(f"SQL Execution Error: {e}")
        return []

def main():
    st.set_page_config(page_title="AI Data Analyst", layout="wide")
    
    with st.sidebar:
        st.header("Settings")
        api_key = st.text_input("Enter Groq API Key", type="password",help="Enter your GROQ API key to access the service")

        if not api_key:
            st.warning("⚠️ Please enter your Groq API Key to proceed")
            return

        st.success("API Key accepted!")
        
    
    st.markdown("""
        <style>
            .main {
                background-color: #f5f5f5;
            }
            .title-text {
                text-align: center;
                font-size: 36px;
                font-weight: bold;
                color: #333;
            }
            .stTextInput, .stButton, .stFileUploader {
                margin-bottom: 20px;
            }
            .stDataFrame {
                border-radius: 10px;
                overflow: hidden;
            }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<h1 class='title-text'>AI Data Analyst</h1>", unsafe_allow_html=True)
    
    conn = initialize_database()
    uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xls", "xlsx"], help="Upload your dataset here")
    
    if uploaded_file is not None:
        upload_and_store_data(uploaded_file, conn)
    
    st.subheader("Ask Your Data a Question")
    user_query = st.text_input("Enter your question:", placeholder="e.g., Show all records where sales > 1000")
    submit = st.button("Submit", help="Click to generate SQL query and fetch results")
    
    if submit:
        if not api_key:
            st.error("Please enter your Groq API key in the sidebar.")
        else:
            sql_query = get_sql_query(user_query, api_key)
            retrieved_data = return_sql_response(sql_query, conn)
            
            st.subheader("Generated SQL Query")
            st.code(sql_query, language="sql")
            
            if retrieved_data:
                st.subheader("Query Results")
                st.dataframe(pd.DataFrame(retrieved_data))
            else:
                st.write("No results found.")
    
    conn.close()

if __name__ == '__main__':
    main()
