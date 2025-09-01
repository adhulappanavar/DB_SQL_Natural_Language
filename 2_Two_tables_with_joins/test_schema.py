import sqlite3

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

if __name__ == "__main__":
    print(get_database_schema())
