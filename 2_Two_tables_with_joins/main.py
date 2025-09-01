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

def get_database_schema():
    """Get the schema of both tables with sample data."""
    conn = sqlite3.connect('mydb.sqlite')
    cursor = conn.cursor()
    
    schema = "Database Schema:\n\n"
    
    # Get customers table schema
    cursor.execute("PRAGMA table_info(customers)")
    customers_columns = cursor.fetchall()
    
    cursor.execute("SELECT * FROM customers LIMIT 3")
    customers_sample = cursor.fetchall()
    
    schema += "Table: customers\n"
    schema += "Columns:\n"
    for col in customers_columns:
        schema += f"  - {col[1]} ({col[2]})\n"
    
    schema += "\nSample customers data:\n"
    for row in customers_sample:
        schema += f"  {row}\n"
    
    # Get orders table schema
    cursor.execute("PRAGMA table_info(orders)")
    orders_columns = cursor.fetchall()
    
    cursor.execute("SELECT * FROM orders LIMIT 3")
    orders_sample = cursor.fetchall()
    
    schema += "\nTable: orders\n"
    schema += "Columns:\n"
    for col in orders_columns:
        schema += f"  - {col[1]} ({col[2]})\n"
    
    schema += "\nSample orders data:\n"
    for row in orders_sample:
        schema += f"  {row}\n"
    
    # Show relationship
    schema += "\nRelationships:\n"
    schema += "- customers.customer_id = orders.customer_id (One-to-Many)\n"
    schema += "- Each customer can have multiple orders\n"
    
    conn.close()
    return schema

def nl2sql(nl_query):
    """Convert natural language to SQL using OpenAI."""
    
    schema = get_database_schema()
    
    prompt = f"""
You are a SQL expert. Convert the following natural language query to SQL.

{schema}

Natural Language Query: {nl_query}

Rules:
1. Use both 'customers' and 'orders' tables when needed
2. Use proper JOIN syntax (INNER JOIN, LEFT JOIN) as appropriate
3. Return ONLY the SQL query, no explanations
4. Use proper SQL syntax for SQLite
5. Be precise with column names and data types
6. Use meaningful aliases when joining tables
7. Consider aggregation functions (COUNT, SUM, AVG) when asking for totals or averages

SQL Query:
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
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
        placeholder="e.g., Show me all customers with their total order amounts",
        lines=2
    ),
    outputs=gr.Textbox(
        label="SQL Query and Results",
        lines=20
    ),
    title="Natural Language to SQL Query Tool (Two Tables)",
    description="Ask questions about customers and orders database in plain English",
    examples=[
        "Show me all customers with their total order amounts",
        "Find customers who have placed more than 2 orders",
        "List orders with customer names and product details",
        "Show the total revenue by country",
        "Find VIP customers who haven't ordered recently",
        "Show average order value by membership level",
        "Which customers have pending orders?",
        "Show top 5 customers by total spending",
        "List all orders from customers in the USA",
        "Show customers and their order counts"
    ]
)

if __name__ == "__main__":
    iface.launch()
