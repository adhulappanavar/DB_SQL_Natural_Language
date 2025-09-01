import gradio as gr
import sqlite3
import os
from openai import OpenAI
import json
from dotenv import load_dotenv

# Load .env from the root directory
load_dotenv('/Users/anidhula/learn/agno/promptengineer48/.env')

# Initialize OpenAI client (you can replace with any LLM API)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "your-api-key-here"))

def get_table_schema():
    """Get the schema of the customers table."""
    conn = sqlite3.connect('mydb.sqlite')
    cursor = conn.cursor()
    
    # Get table schema
    cursor.execute("PRAGMA table_info(customers)")
    columns = cursor.fetchall()
    
    # Get sample data
    cursor.execute("SELECT * FROM customers LIMIT 3")
    sample_data = cursor.fetchall()
    
    conn.close()
    
    schema = "Table: customers\n"
    schema += "Columns:\n"
    for col in columns:
        schema += f"  - {col[1]} ({col[2]})\n"
    
    schema += "\nSample data:\n"
    for row in sample_data:
        schema += f"  {row}\n"
    
    return schema

def nl2sql(nl_query):
    """Convert natural language to SQL using OpenAI."""
    
    schema = get_table_schema()
    
    prompt = f"""
You are a SQL expert. Convert the following natural language query to SQL.

Database Schema:
{schema}

Natural Language Query: {nl_query}

Rules:
1. Only use the 'customers' table
2. Return ONLY the SQL query, no explanations
3. Use proper SQL syntax for SQLite
4. Be precise with column names and data types

SQL Query:
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0
        )
        
        sql_query = response.choices[0].message.content.strip()
        return sql_query
        
    except Exception as e:
        return f"Error generating SQL: {str(e)}"

def execute_sql(sql_query):
    """Execute SQL query and return results."""
    try:
        conn = sqlite3.connect('mydb.sqlite')
        cursor = conn.cursor()
        
        cursor.execute(sql_query)
        results = cursor.fetchall()
        
        # Get column names
        column_names = [description[0] for description in cursor.description] if cursor.description else []
        
        conn.close()
        
        if not results:
            return "Query executed successfully. No results returned."
        
        # Format results
        output = "Query Results:\n"
        output += " | ".join(column_names) + "\n"
        output += "-" * (len(" | ".join(column_names)) + 10) + "\n"
        
        for row in results:
            output += " | ".join(str(cell) for cell in row) + "\n"
        
        return output
        
    except Exception as e:
        return f"Error executing SQL: {str(e)}"

def query_db_with_nl(nl_query):
    """Converts natural language to SQL and executes the query."""
    if not nl_query.strip():
        return "Please enter a natural language query."
    
    # Convert NL to SQL
    sql_query = nl2sql(nl_query)
    
    # Execute SQL
    results = execute_sql(sql_query)
    
    # Format output
    output = f"Natural Language Query: {nl_query}\n\n"
    output += f"Generated SQL: {sql_query}\n\n"
    output += results
    
    return output

# Check if database exists, if not create it
if not os.path.exists('mydb.sqlite'):
    print("Database not found. Please run 'python setup_database.py' first to create the database.")
    exit(1)

iface = gr.Interface(
    fn=query_db_with_nl,
    inputs=gr.Textbox(
        label="Natural Language Query",
        placeholder="e.g., Show me all customers from the USA",
        lines=2
    ),
    outputs=gr.Textbox(
        label="SQL Query and Results",
        lines=20
    ),
    title="Natural Language to SQL Query Tool",
    description="Ask questions about the customers database in plain English",
    examples=[
        "Show me all customers from the USA",
        "Find customers who spent more than $1000",
        "List customers by age, youngest first",
        "Show customers registered in March 2023",
        "How many customers are from each country?",
        "What's the average age of customers?"
    ]
)

if __name__ == "__main__":
    iface.launch()
