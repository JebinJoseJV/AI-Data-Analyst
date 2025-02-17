# AI-Data-Analyst

This is a Streamlit-based AI-powered data analyst that allows users to upload CSV or Excel files, ask natural language questions about the data, and receive SQL query responses with results.

You can access the live version of the app on Streamlit Cloud:
[**AI Data Analyst App**](https://your-streamlit-app-link)

## Features
- Upload and store CSV or Excel files in a SQLite database.
- Convert natural language questions into SQL queries using Groq's AI model.
- Execute the SQL query on the stored dataset and display the results.
- User-friendly Streamlit interface with a sidebar for entering the Groq API key.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/JebinJoseJV/AI-Data-Analyst.git
   
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Usage

1. Enter your Groq API key in the sidebar.
2. Upload a CSV or Excel file.
3. Enter a natural language query about the data.
4. Click the **Submit** button to generate and execute the SQL query.
5. View the SQL query and query results.


## Requirements
- Python 3.8+
- Streamlit
- Pandas
- SQLite3
- Langchain
- Groq API key

## License
This project is licensed under the MIT License.



