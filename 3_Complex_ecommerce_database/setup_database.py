import sqlite3
import os
from datetime import datetime, timedelta
import random

def create_database():
    """Create SQLite database with comprehensive e-commerce tables and sample data."""
    
    # Remove existing database if it exists
    if os.path.exists('mydb.sqlite'):
        os.remove('mydb.sqlite')
    
    # Connect to database
    conn = sqlite3.connect('mydb.sqlite')
    cursor = conn.cursor()
    
    # Create tables with proper foreign key relationships
    
    # 1. Categories table
    cursor.execute('''
        CREATE TABLE categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            parent_category_id INTEGER,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (parent_category_id) REFERENCES categories (category_id)
        )
    ''')
    
    # 2. Suppliers table
    cursor.execute('''
        CREATE TABLE suppliers (
            supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            address TEXT,
            country TEXT,
            rating REAL DEFAULT 0.0,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 3. Products table
    cursor.execute('''
        CREATE TABLE products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            category_id INTEGER NOT NULL,
            supplier_id INTEGER NOT NULL,
            sku TEXT UNIQUE NOT NULL,
            price REAL NOT NULL,
            cost_price REAL NOT NULL,
            weight REAL,
            dimensions TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES categories (category_id),
            FOREIGN KEY (supplier_id) REFERENCES suppliers (supplier_id)
        )
    ''')
    
    # 4. Customers table
    cursor.execute('''
        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            date_of_birth DATE,
            registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT 1,
            total_orders INTEGER DEFAULT 0,
            total_spent REAL DEFAULT 0.0
        )
    ''')
    
    # 5. Shipping_addresses table
    cursor.execute('''
        CREATE TABLE shipping_addresses (
            address_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            address_line1 TEXT NOT NULL,
            address_line2 TEXT,
            city TEXT NOT NULL,
            state TEXT,
            country TEXT NOT NULL,
            postal_code TEXT NOT NULL,
            is_default BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
        )
    ''')
    
    # 6. Payment_methods table
    cursor.execute('''
        CREATE TABLE payment_methods (
            payment_method_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            method_type TEXT NOT NULL,
            card_number TEXT,
            expiry_date TEXT,
            card_holder_name TEXT,
            is_default BOOLEAN DEFAULT 0,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
        )
    ''')
    
    # 7. Orders table
    cursor.execute('''
        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            shipping_address_id INTEGER NOT NULL,
            payment_method_id INTEGER NOT NULL,
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'pending',
            subtotal REAL NOT NULL,
            tax_amount REAL DEFAULT 0.0,
            shipping_cost REAL DEFAULT 0.0,
            total_amount REAL NOT NULL,
            notes TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers (customer_id),
            FOREIGN KEY (shipping_address_id) REFERENCES shipping_addresses (address_id),
            FOREIGN KEY (payment_method_id) REFERENCES payment_methods (payment_method_id)
        )
    ''')
    
    # 8. Order_items table
    cursor.execute('''
        CREATE TABLE order_items (
            order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            total_price REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders (order_id),
            FOREIGN KEY (product_id) REFERENCES products (product_id)
        )
    ''')
    
    # 9. Inventory table
    cursor.execute('''
        CREATE TABLE inventory (
            inventory_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            warehouse_location TEXT DEFAULT 'Main',
            quantity_in_stock INTEGER NOT NULL,
            reorder_level INTEGER DEFAULT 10,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products (product_id)
        )
    ''')
    
    # 10. Reviews table
    cursor.execute('''
        CREATE TABLE reviews (
            review_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            customer_id INTEGER NOT NULL,
            order_id INTEGER NOT NULL,
            rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
            title TEXT,
            comment TEXT,
            review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_verified_purchase BOOLEAN DEFAULT 1,
            FOREIGN KEY (product_id) REFERENCES products (product_id),
            FOREIGN KEY (customer_id) REFERENCES customers (customer_id),
            FOREIGN KEY (order_id) REFERENCES orders (order_id)
        )
    ''')
    
    # 11. Product_tags table (Many-to-Many relationship)
    cursor.execute('''
        CREATE TABLE product_tags (
            product_id INTEGER NOT NULL,
            tag_name TEXT NOT NULL,
            PRIMARY KEY (product_id, tag_name),
            FOREIGN KEY (product_id) REFERENCES products (product_id)
        )
    ''')
    
    # Insert sample data
    
    # Categories (with parent-child relationships)
    categories_data = [
        (None, 'Electronics', 'Electronic devices and accessories', 1),
        (None, 'Clothing', 'Fashion and apparel', 1),
        (None, 'Home & Garden', 'Home improvement and garden supplies', 1),
        (1, 'Computers', 'Desktop and laptop computers', 1),
        (1, 'Smartphones', 'Mobile phones and accessories', 1),
        (1, 'Audio', 'Speakers, headphones, and audio equipment', 1),
        (2, 'Men\'s Clothing', 'Clothing for men', 1),
        (2, 'Women\'s Clothing', 'Clothing for women', 1),
        (2, 'Kids Clothing', 'Clothing for children', 1),
        (3, 'Kitchen', 'Kitchen appliances and utensils', 1),
        (3, 'Furniture', 'Home and office furniture', 1),
        (4, 'Laptops', 'Portable computers', 1),
        (4, 'Desktops', 'Desktop computers', 1),
        (5, 'Android Phones', 'Android smartphones', 1),
        (5, 'iPhone', 'Apple smartphones', 1)
    ]
    
    cursor.executemany('''
        INSERT INTO categories (parent_category_id, name, description, is_active)
        VALUES (?, ?, ?, ?)
    ''', categories_data)
    
    # Suppliers
    suppliers_data = [
        ('TechCorp', 'tech@techcorp.com', '+1-555-0101', '123 Tech St, Silicon Valley', 'USA', 4.5),
        ('FashionHub', 'contact@fashionhub.com', '+1-555-0102', '456 Fashion Ave, NYC', 'USA', 4.2),
        ('HomeGoods Inc', 'sales@homegoods.com', '+1-555-0103', '789 Home Rd, Chicago', 'USA', 4.0),
        ('Global Electronics', 'info@globalelec.com', '+44-20-1234-5678', '10 Tech Lane, London', 'UK', 4.3),
        ('Asian Suppliers', 'contact@asiansuppliers.com', '+81-3-1234-5678', '5 Supplier St, Tokyo', 'Japan', 4.1)
    ]
    
    cursor.executemany('''
        INSERT INTO suppliers (name, email, phone, address, country, rating)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', suppliers_data)
    
    # Products
    products_data = [
        ('MacBook Pro 13"', 'Apple MacBook Pro with M2 chip', 13, 1, 'MBP13-001', 1299.99, 800.00, 1.4, '12.3" x 8.6" x 0.6"'),
        ('Dell XPS 15', 'Dell XPS 15 laptop with Intel i7', 13, 1, 'DXP15-001', 1499.99, 900.00, 2.1, '13.6" x 9.1" x 0.7"'),
        ('iPhone 15 Pro', 'Apple iPhone 15 Pro 128GB', 14, 1, 'IP15P-001', 999.99, 600.00, 0.19, '5.8" x 2.8" x 0.3"'),
        ('Samsung Galaxy S24', 'Samsung Galaxy S24 256GB', 14, 1, 'SGS24-001', 899.99, 550.00, 0.17, '5.9" x 2.8" x 0.3"'),
        ('Sony WH-1000XM4', 'Sony wireless noise-canceling headphones', 6, 1, 'SWH4-001', 349.99, 200.00, 0.25, '7.3" x 3.0" x 10.0"'),
        ('Men\'s Casual Shirt', 'Cotton casual shirt for men', 7, 2, 'MCS-001', 29.99, 15.00, 0.3, '12" x 8" x 1"'),
        ('Women\'s Dress', 'Elegant evening dress', 8, 2, 'WD-001', 89.99, 45.00, 0.5, '14" x 10" x 2"'),
        ('Kitchen Mixer', 'Professional stand mixer', 10, 3, 'KM-001', 299.99, 150.00, 5.2, '14" x 8" x 12"'),
        ('Coffee Table', 'Modern wooden coffee table', 11, 3, 'CT-001', 199.99, 100.00, 25.0, '48" x 24" x 18"'),
        ('Gaming Mouse', 'RGB gaming mouse with 16000 DPI', 4, 1, 'GM-001', 79.99, 30.00, 0.12, '5" x 2.5" x 1.5"'),
        ('Wireless Keyboard', 'Mechanical wireless keyboard', 4, 1, 'WK-001', 129.99, 60.00, 0.8, '14" x 5" x 1"'),
        ('Bluetooth Speaker', 'Portable bluetooth speaker', 6, 1, 'BS-001', 89.99, 40.00, 0.5, '6" x 3" x 3"'),
        ('Running Shoes', 'Professional running shoes', 7, 2, 'RS-001', 129.99, 65.00, 0.9, '12" x 4" x 4"'),
        ('Winter Jacket', 'Warm winter jacket', 8, 2, 'WJ-001', 199.99, 100.00, 1.2, '24" x 16" x 3"'),
        ('Garden Tools Set', 'Complete garden maintenance set', 3, 3, 'GTS-001', 149.99, 75.00, 8.5, '36" x 12" x 6"')
    ]
    
    cursor.executemany('''
        INSERT INTO products (name, description, category_id, supplier_id, sku, price, cost_price, weight, dimensions)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', products_data)
    
    # Customers
    customers_data = [
        ('John', 'Smith', 'john.smith@email.com', '+1-555-0001', '1990-05-15', '2023-01-10'),
        ('Sarah', 'Johnson', 'sarah.j@email.com', '+1-555-0002', '1988-12-03', '2023-02-15'),
        ('Mike', 'Wilson', 'mike.wilson@email.com', '+1-555-0003', '1975-08-22', '2023-01-25'),
        ('Emma', 'Davis', 'emma.davis@email.com', '+44-20-0001', '1992-03-10', '2023-03-05'),
        ('David', 'Brown', 'david.brown@email.com', '+1-555-0004', '1985-11-18', '2023-02-08'),
        ('Lisa', 'Garcia', 'lisa.garcia@email.com', '+34-91-0001', '1991-07-25', '2023-03-20'),
        ('Tom', 'Anderson', 'tom.anderson@email.com', '+61-2-0001', '1983-04-12', '2023-01-30'),
        ('Anna', 'Mueller', 'anna.mueller@email.com', '+49-30-0001', '1994-09-08', '2023-04-01'),
        ('James', 'Taylor', 'james.taylor@email.com', '+44-16-0001', '1980-06-30', '2023-02-20'),
        ('Maria', 'Rodriguez', 'maria.rodriguez@email.com', '+34-93-0001', '1987-01-14', '2023-03-12')
    ]
    
    cursor.executemany('''
        INSERT INTO customers (first_name, last_name, email, phone, date_of_birth, registration_date)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', customers_data)
    
    # Shipping addresses
    addresses_data = [
        (1, '123 Main St', 'Apt 4B', 'New York', 'NY', 'USA', '10001', 1),
        (1, '456 Oak Ave', None, 'Brooklyn', 'NY', 'USA', '11201', 0),
        (2, '789 Pine Rd', 'Suite 100', 'Los Angeles', 'CA', 'USA', '90210', 1),
        (3, '321 Elm St', None, 'Chicago', 'IL', 'USA', '60601', 1),
        (4, '10 Baker St', 'Flat 2', 'London', None, 'UK', 'W1U 6TU', 1),
        (5, '555 Queen St', 'Unit 15', 'Toronto', 'ON', 'Canada', 'M5V 2H1', 1),
        (6, 'Calle Mayor 123', 'Piso 3', 'Madrid', None, 'Spain', '28013', 1),
        (7, '123 George St', 'Apt 5', 'Sydney', 'NSW', 'Australia', '2000', 1),
        (8, 'Unter den Linden 1', None, 'Berlin', None, 'Germany', '10117', 1),
        (9, '15 Oxford Rd', 'House 7', 'Manchester', None, 'UK', 'M1 1AA', 1),
        (10, 'Carrer de la Pau 45', 'Piso 2', 'Barcelona', None, 'Spain', '08001', 1)
    ]
    
    cursor.executemany('''
        INSERT INTO shipping_addresses (customer_id, address_line1, address_line2, city, state, country, postal_code, is_default)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', addresses_data)
    
    # Payment methods
    payment_methods_data = [
        (1, 'credit_card', '4111-1111-1111-1111', '12/25', 'John Smith', 1, 1),
        (1, 'paypal', None, None, 'John Smith', 0, 1),
        (2, 'credit_card', '4222-2222-2222-2222', '03/26', 'Sarah Johnson', 1, 1),
        (3, 'debit_card', '4333-3333-3333-3333', '06/24', 'Mike Wilson', 1, 1),
        (4, 'credit_card', '4444-4444-4444-4444', '09/25', 'Emma Davis', 1, 1),
        (5, 'credit_card', '4555-5555-5555-5555', '12/26', 'David Brown', 1, 1),
        (6, 'paypal', None, None, 'Lisa Garcia', 1, 1),
        (7, 'credit_card', '4666-6666-6666-6666', '02/25', 'Tom Anderson', 1, 1),
        (8, 'debit_card', '4777-7777-7777-7777', '05/24', 'Anna Mueller', 1, 1),
        (9, 'credit_card', '4888-8888-8888-8888', '08/25', 'James Taylor', 1, 1),
        (10, 'paypal', None, None, 'Maria Rodriguez', 1, 1)
    ]
    
    cursor.executemany('''
        INSERT INTO payment_methods (customer_id, method_type, card_number, expiry_date, card_holder_name, is_default, is_active)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', payment_methods_data)
    
    # Orders
    orders_data = [
        (1, 1, 1, '2023-05-10 10:30:00', 'completed', 1299.99, 129.99, 15.00, 1444.98, 'Express delivery'),
        (1, 1, 1, '2023-05-15 14:20:00', 'completed', 79.99, 8.00, 5.00, 92.99, None),
        (2, 3, 3, '2023-05-12 09:15:00', 'completed', 1499.99, 150.00, 20.00, 1669.99, 'Gift wrapped'),
        (2, 3, 3, '2023-05-20 16:45:00', 'shipped', 299.99, 30.00, 25.00, 354.99, None),
        (3, 4, 4, '2023-05-08 11:00:00', 'completed', 999.99, 100.00, 10.00, 1109.99, None),
        (3, 4, 4, '2023-05-18 13:30:00', 'pending', 349.99, 35.00, 8.00, 392.99, None),
        (4, 5, 5, '2023-05-05 08:45:00', 'completed', 899.99, 90.00, 12.00, 1001.99, None),
        (4, 5, 5, '2023-05-22 15:20:00', 'completed', 89.99, 9.00, 5.00, 103.99, None),
        (4, 5, 5, '2023-05-25 10:10:00', 'shipped', 129.99, 13.00, 6.00, 148.99, None),
        (5, 6, 6, '2023-05-11 12:30:00', 'completed', 199.99, 20.00, 30.00, 249.99, 'Assembly required'),
        (6, 7, 7, '2023-05-14 14:15:00', 'completed', 29.99, 3.00, 4.00, 36.99, None),
        (6, 7, 7, '2023-05-28 09:45:00', 'pending', 89.99, 9.00, 7.00, 105.98, None),
        (7, 8, 8, '2023-05-09 16:20:00', 'completed', 120.00, 12.00, 5.00, 137.00, None),
        (8, 9, 9, '2023-05-16 11:30:00', 'completed', 80.00, 8.00, 3.00, 91.00, None),
        (9, 10, 10, '2023-05-03 13:45:00', 'completed', 400.00, 40.00, 15.00, 455.00, 'Gift card included'),
        (9, 10, 10, '2023-05-19 17:00:00', 'shipped', 180.00, 18.00, 8.00, 206.00, None),
        (10, 11, 11, '2023-05-07 10:15:00', 'completed', 350.00, 35.00, 12.00, 397.00, None),
        (10, 11, 11, '2023-05-24 14:30:00', 'pending', 50.00, 5.00, 4.00, 59.00, None)
    ]
    
    cursor.executemany('''
        INSERT INTO orders (customer_id, shipping_address_id, payment_method_id, order_date, status, subtotal, tax_amount, shipping_cost, total_amount, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', orders_data)
    
    # Order items
    order_items_data = [
        (1, 1, 1, 1299.99, 1299.99),
        (2, 10, 1, 79.99, 79.99),
        (3, 2, 1, 1499.99, 1499.99),
        (4, 8, 1, 299.99, 299.99),
        (5, 3, 1, 999.99, 999.99),
        (6, 5, 1, 349.99, 349.99),
        (7, 4, 1, 899.99, 899.99),
        (8, 12, 1, 89.99, 89.99),
        (9, 11, 1, 129.99, 129.99),
        (10, 9, 1, 199.99, 199.99),
        (11, 6, 1, 29.99, 29.99),
        (12, 7, 1, 89.99, 89.99),
        (13, 13, 1, 120.00, 120.00),
        (14, 14, 1, 80.00, 80.00),
        (15, 15, 1, 400.00, 400.00),
        (16, 15, 1, 180.00, 180.00),
        (17, 15, 1, 350.00, 350.00),
        (18, 15, 1, 50.00, 50.00)
    ]
    
    cursor.executemany('''
        INSERT INTO order_items (order_id, product_id, quantity, unit_price, total_price)
        VALUES (?, ?, ?, ?, ?)
    ''', order_items_data)
    
    # Inventory
    inventory_data = [
        (1, 'Warehouse A', 50, 10),
        (2, 'Warehouse A', 30, 5),
        (3, 'Warehouse B', 100, 20),
        (4, 'Warehouse B', 75, 15),
        (5, 'Warehouse A', 40, 8),
        (6, 'Warehouse C', 200, 25),
        (7, 'Warehouse C', 150, 20),
        (8, 'Warehouse A', 25, 5),
        (9, 'Warehouse B', 60, 12),
        (10, 'Warehouse A', 80, 15),
        (11, 'Warehouse A', 120, 20),
        (12, 'Warehouse B', 90, 15),
        (13, 'Warehouse C', 300, 50),
        (14, 'Warehouse C', 180, 30),
        (15, 'Warehouse B', 45, 10)
    ]
    
    cursor.executemany('''
        INSERT INTO inventory (product_id, warehouse_location, quantity_in_stock, reorder_level)
        VALUES (?, ?, ?, ?)
    ''', inventory_data)
    
    # Reviews
    reviews_data = [
        (1, 1, 1, 5, 'Excellent laptop', 'Great performance and battery life', 1),
        (1, 1, 2, 4, 'Good mouse', 'Comfortable and responsive', 1),
        (2, 2, 3, 5, 'Perfect for work', 'Fast and reliable', 1),
        (3, 3, 5, 4, 'Good phone', 'Nice camera quality', 1),
        (4, 4, 7, 5, 'Amazing headphones', 'Best noise cancellation', 1),
        (5, 5, 8, 3, 'Decent mixer', 'Could be better', 1),
        (6, 6, 11, 4, 'Nice shirt', 'Good quality fabric', 1),
        (7, 7, 12, 5, 'Beautiful dress', 'Perfect fit', 1),
        (8, 8, 13, 4, 'Good speaker', 'Loud and clear', 1),
        (9, 9, 15, 5, 'Great table', 'Sturdy and beautiful', 1),
        (10, 10, 17, 4, 'Good camera', 'Nice features', 1)
    ]
    
    cursor.executemany('''
        INSERT INTO reviews (product_id, customer_id, order_id, rating, title, comment, is_verified_purchase)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', reviews_data)
    
    # Product tags
    product_tags_data = [
        (1, 'laptop'), (1, 'apple'), (1, 'professional'),
        (2, 'laptop'), (2, 'dell'), (2, 'business'),
        (3, 'smartphone'), (3, 'apple'), (3, 'premium'),
        (4, 'smartphone'), (4, 'samsung'), (4, 'android'),
        (5, 'headphones'), (5, 'wireless'), (5, 'noise-canceling'),
        (6, 'clothing'), (6, 'men'), (6, 'casual'),
        (7, 'clothing'), (7, 'women'), (7, 'dress'),
        (8, 'kitchen'), (8, 'appliance'), (8, 'professional'),
        (9, 'furniture'), (9, 'wooden'), (9, 'modern'),
        (10, 'gaming'), (10, 'mouse'), (10, 'rgb'),
        (11, 'keyboard'), (11, 'wireless'), (11, 'mechanical'),
        (12, 'speaker'), (12, 'bluetooth'), (12, 'portable'),
        (13, 'shoes'), (13, 'running'), (13, 'sports'),
        (14, 'jacket'), (14, 'winter'), (14, 'warm'),
        (15, 'garden'), (15, 'tools'), (15, 'complete')
    ]
    
    cursor.executemany('''
        INSERT INTO product_tags (product_id, tag_name)
        VALUES (?, ?)
    ''', product_tags_data)
    
    # Update customer totals
    cursor.execute('''
        UPDATE customers 
        SET total_orders = (
            SELECT COUNT(*) FROM orders WHERE orders.customer_id = customers.customer_id
        ),
        total_spent = (
            SELECT COALESCE(SUM(total_amount), 0) FROM orders WHERE orders.customer_id = customers.customer_id
        )
    ''')
    
    # Commit and close
    conn.commit()
    conn.close()
    
    print("Complex e-commerce database created successfully!")
    print("Tables created:")
    print("- categories (with parent-child relationships)")
    print("- suppliers")
    print("- products")
    print("- customers")
    print("- shipping_addresses")
    print("- payment_methods")
    print("- orders")
    print("- order_items")
    print("- inventory")
    print("- reviews")
    print("- product_tags (many-to-many)")
    print("\nSample complex queries you can try:")
    print("- Show me all customers with their total spending and order count")
    print("- Find products with low inventory that need reordering")
    print("- List top 5 customers by total spending with their preferred payment methods")
    print("- Show average rating by product category")
    print("- Find customers who haven't ordered in the last 30 days")
    print("- Show revenue by supplier and country")
    print("- List products with their inventory levels and supplier information")
    print("- Find customers who have reviewed products they purchased")
    print("- Show order status distribution by customer country")
    print("- List products with tags and their average ratings")

if __name__ == "__main__":
    create_database()
