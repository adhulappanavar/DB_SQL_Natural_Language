import sqlite3
import os

def create_database():
    """Create SQLite database with customers table and sample data."""
    
    # Remove existing database if it exists
    if os.path.exists('mydb.sqlite'):
        os.remove('mydb.sqlite')
    
    # Connect to database
    conn = sqlite3.connect('mydb.sqlite')
    cursor = conn.cursor()
    
    # Create customers table
    cursor.execute('''
        CREATE TABLE customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            age INTEGER,
            city TEXT,
            country TEXT,
            registration_date DATE,
            total_orders INTEGER DEFAULT 0,
            total_spent REAL DEFAULT 0.0
        )
    ''')
    
    # Insert sample data
    sample_customers = [
        ('John Smith', 'john.smith@email.com', 28, 'New York', 'USA', '2023-01-15', 5, 1250.50),
        ('Sarah Johnson', 'sarah.j@email.com', 34, 'Los Angeles', 'USA', '2023-02-20', 8, 2100.75),
        ('Mike Wilson', 'mike.wilson@email.com', 45, 'Chicago', 'USA', '2023-01-30', 3, 850.25),
        ('Emma Davis', 'emma.davis@email.com', 29, 'London', 'UK', '2023-03-10', 12, 3200.00),
        ('David Brown', 'david.brown@email.com', 52, 'Toronto', 'Canada', '2023-02-05', 6, 1800.50),
        ('Lisa Garcia', 'lisa.garcia@email.com', 31, 'Madrid', 'Spain', '2023-03-25', 4, 950.75),
        ('Tom Anderson', 'tom.anderson@email.com', 38, 'Sydney', 'Australia', '2023-01-20', 7, 1650.00),
        ('Anna Mueller', 'anna.mueller@email.com', 26, 'Berlin', 'Germany', '2023-04-01', 2, 450.25),
        ('James Taylor', 'james.taylor@email.com', 41, 'Manchester', 'UK', '2023-02-15', 9, 2400.50),
        ('Maria Rodriguez', 'maria.rodriguez@email.com', 33, 'Barcelona', 'Spain', '2023-03-05', 6, 1750.00)
    ]
    
    cursor.executemany('''
        INSERT INTO customers (name, email, age, city, country, registration_date, total_orders, total_spent)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', sample_customers)
    
    # Commit and close
    conn.commit()
    conn.close()
    
    print("Database created successfully with customers table and sample data!")
    print("Sample queries you can try:")
    print("- Show me all customers from the USA")
    print("- Find customers who spent more than $1000")
    print("- List customers by age, youngest first")
    print("- Show customers registered in March 2023")

if __name__ == "__main__":
    create_database()
