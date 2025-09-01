import sqlite3
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load .env from the root directory
load_dotenv('/Users/anidhula/learn/agno/promptengineer48/.env')

# Initialize OpenAI client
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

def test_query():
    """Test the improved AI with the problematic query."""
    query = "Show me all customers with their total spending and order count"
    
    print(f"Testing query: {query}")
    print("=" * 60)
    
    sql_query = nl2sql(query)
    print(f"Generated SQL:\n{sql_query}")
    print("\n" + "=" * 60)
    
    # Test if the SQL executes correctly
    try:
        conn = sqlite3.connect('mydb.sqlite')
        cursor = conn.cursor()
        
        cursor.execute(sql_query)
        results = cursor.fetchall()
        
        # Get column names
        column_names = [description[0] for description in cursor.description] if cursor.description else []
        
        print("Query Results:")
        print(" | ".join(column_names))
        print("-" * 50)
        
        for row in results:
            print(" | ".join(str(cell) for cell in row))
        
        conn.close()
        
    except Exception as e:
        print(f"Error executing SQL: {str(e)}")

if __name__ == "__main__":
    test_query()
