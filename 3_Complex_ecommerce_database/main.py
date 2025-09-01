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
    """Get the schema of all tables with sample data and relationships."""
    conn = sqlite3.connect('mydb.sqlite')
    cursor = conn.cursor()
    
    schema = "Complex E-commerce Database Schema:\n\n"
    
    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = cursor.fetchall()
    
    # Define table relationships
    relationships = {
        'categories': 'Self-referencing (parent_category_id → category_id)',
        'suppliers': 'Referenced by products',
        'products': 'References categories, suppliers. Referenced by order_items, inventory, reviews, product_tags',
        'customers': 'Referenced by shipping_addresses, payment_methods, orders, reviews',
        'shipping_addresses': 'References customers. Referenced by orders',
        'payment_methods': 'References customers. Referenced by orders',
        'orders': 'References customers, shipping_addresses, payment_methods. Referenced by order_items, reviews',
        'order_items': 'References orders, products',
        'inventory': 'References products',
        'reviews': 'References products, customers, orders',
        'product_tags': 'Many-to-many relationship with products'
    }
    
    # Get schema for each table
    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 2")
        sample_data = cursor.fetchall()
        
        schema += f"Table: {table_name}\n"
        schema += "Columns:\n"
        for col in columns:
            schema += f"  - {col[1]} ({col[2]})"
            if col[5] == 1:  # Primary key
                schema += " [PRIMARY KEY]"
            schema += "\n"
        
        schema += f"Relationships: {relationships.get(table_name, 'None')}\n"
        
        if sample_data:
            schema += f"Sample {table_name} data:\n"
            for row in sample_data:
                schema += f"  {row}\n"
        
        schema += "\n"
    
    # Add complex relationship examples
    schema += "Complex Relationship Examples:\n"
    schema += "- customers → orders → order_items → products → categories\n"
    schema += "- customers → shipping_addresses → orders\n"
    schema += "- customers → payment_methods → orders\n"
    schema += "- products → inventory (stock levels)\n"
    schema += "- products → reviews (customer feedback)\n"
    schema += "- products → product_tags (many-to-many)\n"
    schema += "- categories → categories (hierarchical)\n"
    schema += "- suppliers → products → order_items → orders\n"
    
    # Add pre-calculated fields information
    schema += "\nPRE-CALCULATED FIELDS (Use these instead of complex joins when possible):\n"
    schema += "- customers.total_spent: Sum of all order amounts for the customer\n"
    schema += "- customers.total_orders: Count of orders for the customer\n"
    schema += "- orders.total_amount: Total amount including tax and shipping\n"
    schema += "- order_items.total_price: Quantity * unit_price\n"
    
    conn.close()
    return schema

def nl2sql(nl_query):
    """Convert natural language to SQL using OpenAI."""
    
    schema = get_database_schema()
    
    prompt = f"""
You are a SQL expert. Convert the following natural language query to SQL for a complex e-commerce database.

{schema}

Natural Language Query: {nl_query}

CRITICAL RULES:
1. ALWAYS check if the requested data is already available in a single table before using joins
2. Use pre-calculated fields when available (e.g., customers.total_spent, customers.total_orders)
3. Only use JOINs when you need data from multiple tables
4. Prefer simple queries over complex ones when they achieve the same result
5. Use appropriate JOIN types (INNER JOIN, LEFT JOIN) based on the query needs
6. Use proper aggregation functions (COUNT, SUM, AVG, MAX, MIN) when needed
7. Apply appropriate filtering with WHERE clauses
8. Use GROUP BY and HAVING for grouped aggregations
9. Use ORDER BY and LIMIT for sorting and limiting results
10. Use meaningful table aliases for readability
11. Return ONLY the SQL query, no explanations

EXAMPLES:
- "Show customers with total spending" → SELECT customer_id, first_name, last_name, total_spent FROM customers
- "Show customers with order count" → SELECT customer_id, first_name, last_name, total_orders FROM customers
- "Show customers with both spending and orders" → SELECT customer_id, first_name, last_name, total_spent, total_orders FROM customers

SQL Query:
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
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
        placeholder="e.g., Show me all customers with their total spending and order count",
        lines=2
    ),
    outputs=gr.Textbox(
        label="SQL Query and Results",
        lines=25
    ),
    title="Natural Language to SQL Query Tool (Complex E-commerce)",
    description="Ask complex questions about the e-commerce database with 11+ tables and relationships",
    examples=[
        "Show me all customers with their total spending and order count",
        "Find products with low inventory that need reordering",
        "List top 5 customers by total spending with their preferred payment methods",
        "Show average rating by product category",
        "Find customers who haven't ordered in the last 30 days",
        "Show revenue by supplier and country",
        "List products with their inventory levels and supplier information",
        "Find customers who have reviewed products they purchased",
        "Show order status distribution by customer country",
        "List products with tags and their average ratings",
        "Find the most profitable products by supplier",
        "Show customers and their shipping addresses by country",
        "List products in Electronics category with their reviews",
        "Find orders with multiple items and their total values",
        "Show inventory levels by warehouse location"
    ]
)

if __name__ == "__main__":
    iface.launch()
