import sqlite3

def test_customer_query():
    """Test the correct SQL query for customers with total spending and order count."""
    conn = sqlite3.connect('mydb.sqlite')
    cursor = conn.cursor()
    
    print("=== Correct Query ===")
    print("SELECT customer_id, first_name, last_name, total_spent, total_orders")
    print("FROM customers;")
    print()
    
    # Execute the correct query
    cursor.execute("""
        SELECT customer_id, first_name, last_name, total_spent, total_orders
        FROM customers
        ORDER BY total_spent DESC
    """)
    
    results = cursor.fetchall()
    
    print("Query Results:")
    print("customer_id | first_name | last_name | total_spent | total_orders")
    print("-" * 70)
    for row in results:
        print(f"{row[0]:11} | {row[1]:10} | {row[2]:9} | {row[3]:11.2f} | {row[4]:12}")
    
    print("\n=== Alternative Query (if you want to calculate from orders) ===")
    print("SELECT c.customer_id, c.first_name, c.last_name,")
    print("       COALESCE(SUM(o.total_amount), 0) as total_spent,")
    print("       COUNT(o.order_id) as total_orders")
    print("FROM customers c")
    print("LEFT JOIN orders o ON c.customer_id = o.customer_id")
    print("GROUP BY c.customer_id, c.first_name, c.last_name")
    print("ORDER BY total_spent DESC;")
    print()
    
    # Execute the alternative query
    cursor.execute("""
        SELECT c.customer_id, c.first_name, c.last_name,
               COALESCE(SUM(o.total_amount), 0) as total_spent,
               COUNT(o.order_id) as total_orders
        FROM customers c
        LEFT JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY c.customer_id, c.first_name, c.last_name
        ORDER BY total_spent DESC
    """)
    
    results2 = cursor.fetchall()
    
    print("Alternative Query Results:")
    print("customer_id | first_name | last_name | total_spent | total_orders")
    print("-" * 70)
    for row in results2:
        print(f"{row[0]:11} | {row[1]:10} | {row[2]:9} | {row[3]:11.2f} | {row[4]:12}")
    
    conn.close()

if __name__ == "__main__":
    test_customer_query()
