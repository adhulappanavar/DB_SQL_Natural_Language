import sqlite3
import os

def create_database():
    """Create SQLite database with customers and orders tables and sample data."""
    
    # Remove existing database if it exists
    if os.path.exists('mydb.sqlite'):
        os.remove('mydb.sqlite')
    
    # Connect to database
    conn = sqlite3.connect('mydb.sqlite')
    cursor = conn.cursor()
    
    # Create customers table
    cursor.execute('''
        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            age INTEGER,
            city TEXT,
            country TEXT,
            registration_date DATE,
            membership_level TEXT DEFAULT 'standard'
        )
    ''')
    
    # Create orders table
    cursor.execute('''
        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            order_date DATE NOT NULL,
            product_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            total_amount REAL NOT NULL,
            status TEXT DEFAULT 'pending',
            FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
        )
    ''')
    
    # Insert sample customers
    sample_customers = [
        ('John Smith', 'john.smith@email.com', 28, 'New York', 'USA', '2023-01-15', 'premium'),
        ('Sarah Johnson', 'sarah.j@email.com', 34, 'Los Angeles', 'USA', '2023-02-20', 'standard'),
        ('Mike Wilson', 'mike.wilson@email.com', 45, 'Chicago', 'USA', '2023-01-30', 'premium'),
        ('Emma Davis', 'emma.davis@email.com', 29, 'London', 'UK', '2023-03-10', 'vip'),
        ('David Brown', 'david.brown@email.com', 52, 'Toronto', 'Canada', '2023-02-05', 'standard'),
        ('Lisa Garcia', 'lisa.garcia@email.com', 31, 'Madrid', 'Spain', '2023-03-25', 'premium'),
        ('Tom Anderson', 'tom.anderson@email.com', 38, 'Sydney', 'Australia', '2023-01-20', 'standard'),
        ('Anna Mueller', 'anna.mueller@email.com', 26, 'Berlin', 'Germany', '2023-04-01', 'standard'),
        ('James Taylor', 'james.taylor@email.com', 41, 'Manchester', 'UK', '2023-02-15', 'vip'),
        ('Maria Rodriguez', 'maria.rodriguez@email.com', 33, 'Barcelona', 'Spain', '2023-03-05', 'premium')
    ]
    
    cursor.executemany('''
        INSERT INTO customers (name, email, age, city, country, registration_date, membership_level)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', sample_customers)
    
    # Insert sample orders
    sample_orders = [
        (1, '2023-05-10', 'Laptop', 1, 1200.00, 1200.00, 'completed'),
        (1, '2023-05-15', 'Mouse', 2, 25.00, 50.00, 'completed'),
        (2, '2023-05-12', 'Keyboard', 1, 80.00, 80.00, 'completed'),
        (2, '2023-05-20', 'Monitor', 1, 300.00, 300.00, 'shipped'),
        (3, '2023-05-08', 'Tablet', 1, 500.00, 500.00, 'completed'),
        (3, '2023-05-18', 'Headphones', 1, 150.00, 150.00, 'pending'),
        (4, '2023-05-05', 'Smartphone', 1, 800.00, 800.00, 'completed'),
        (4, '2023-05-22', 'Charger', 3, 15.00, 45.00, 'completed'),
        (4, '2023-05-25', 'Case', 1, 30.00, 30.00, 'shipped'),
        (5, '2023-05-11', 'Printer', 1, 200.00, 200.00, 'completed'),
        (6, '2023-05-14', 'Webcam', 1, 100.00, 100.00, 'completed'),
        (6, '2023-05-28', 'Microphone', 1, 75.00, 75.00, 'pending'),
        (7, '2023-05-09', 'Speakers', 1, 120.00, 120.00, 'completed'),
        (8, '2023-05-16', 'USB Drive', 2, 20.00, 40.00, 'completed'),
        (9, '2023-05-03', 'Gaming Console', 1, 400.00, 400.00, 'completed'),
        (9, '2023-05-19', 'Games', 3, 60.00, 180.00, 'shipped'),
        (10, '2023-05-07', 'Camera', 1, 350.00, 350.00, 'completed'),
        (10, '2023-05-24', 'Tripod', 1, 50.00, 50.00, 'pending')
    ]
    
    cursor.executemany('''
        INSERT INTO orders (customer_id, order_date, product_name, quantity, unit_price, total_amount, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', sample_orders)
    
    # Commit and close
    conn.commit()
    conn.close()
    
    print("Database created successfully with customers and orders tables!")
    print("Sample queries you can try:")
    print("- Show me all customers with their total order amounts")
    print("- Find customers who have placed more than 2 orders")
    print("- List orders with customer names and product details")
    print("- Show the total revenue by country")
    print("- Find VIP customers who haven't ordered recently")
    print("- Show average order value by membership level")

if __name__ == "__main__":
    create_database()
