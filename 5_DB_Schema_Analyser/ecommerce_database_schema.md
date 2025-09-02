# Database Schema Analysis

**Database**: `mydb.sqlite`  
**Analysis Date**: 2025-09-02 11:28:29  
**Total Tables**: 12

## Database Overview

This database contains 12 tables with complex relationships and comprehensive data structures.

## Table Schemas

### categories

**Columns:**
- `category_id` (INTEGER) 🔑
- `name` (TEXT) NOT NULL
- `description` (TEXT)
- `parent_category_id` (INTEGER)
- `is_active` (BOOLEAN) DEFAULT 1
- `created_at` (TIMESTAMP) DEFAULT CURRENT_TIMESTAMP

**Foreign Keys:**
- `parent_category_id` → `categories.category_id`

**Sample Data:**
```
(1, 'Electronics', 'Electronic devices and accessories', None, 1, '2025-09-01 05:48:45')
(2, 'Clothing', 'Fashion and apparel', None, 1, '2025-09-01 05:48:45')
(3, 'Home & Garden', 'Home improvement and garden supplies', None, 1, '2025-09-01 05:48:45')
```

### customers

**Columns:**
- `customer_id` (INTEGER) 🔑
- `first_name` (TEXT) NOT NULL
- `last_name` (TEXT) NOT NULL
- `email` (TEXT) NOT NULL
- `phone` (TEXT)
- `date_of_birth` (DATE)
- `registration_date` (TIMESTAMP) DEFAULT CURRENT_TIMESTAMP
- `is_active` (BOOLEAN) DEFAULT 1
- `total_orders` (INTEGER) DEFAULT 0
- `total_spent` (REAL) DEFAULT 0.0

**Sample Data:**
```
(1, 'John', 'Smith', 'john.smith@email.com', '+1-555-0001', '1990-05-15', '2023-01-10', 1, 2, 1537.97)
(2, 'Sarah', 'Johnson', 'sarah.j@email.com', '+1-555-0002', '1988-12-03', '2023-02-15', 1, 2, 2024.98)
(3, 'Mike', 'Wilson', 'mike.wilson@email.com', '+1-555-0003', '1975-08-22', '2023-01-25', 1, 2, 1502.98)
```

### inventory

**Columns:**
- `inventory_id` (INTEGER) 🔑
- `product_id` (INTEGER) NOT NULL
- `warehouse_location` (TEXT) DEFAULT 'Main'
- `quantity_in_stock` (INTEGER) NOT NULL
- `reorder_level` (INTEGER) DEFAULT 10
- `last_updated` (TIMESTAMP) DEFAULT CURRENT_TIMESTAMP

**Foreign Keys:**
- `product_id` → `products.product_id`

**Sample Data:**
```
(1, 1, 'Warehouse A', 50, 10, '2025-09-01 05:48:45')
(2, 2, 'Warehouse A', 30, 5, '2025-09-01 05:48:45')
(3, 3, 'Warehouse B', 100, 20, '2025-09-01 05:48:45')
```

### order_items

**Columns:**
- `order_item_id` (INTEGER) 🔑
- `order_id` (INTEGER) NOT NULL
- `product_id` (INTEGER) NOT NULL
- `quantity` (INTEGER) NOT NULL
- `unit_price` (REAL) NOT NULL
- `total_price` (REAL) NOT NULL

**Foreign Keys:**
- `product_id` → `products.product_id`
- `order_id` → `orders.order_id`

**Sample Data:**
```
(1, 1, 1, 1, 1299.99, 1299.99)
(2, 2, 10, 1, 79.99, 79.99)
(3, 3, 2, 1, 1499.99, 1499.99)
```

### orders

**Columns:**
- `order_id` (INTEGER) 🔑
- `customer_id` (INTEGER) NOT NULL
- `shipping_address_id` (INTEGER) NOT NULL
- `payment_method_id` (INTEGER) NOT NULL
- `order_date` (TIMESTAMP) DEFAULT CURRENT_TIMESTAMP
- `status` (TEXT) DEFAULT 'pending'
- `subtotal` (REAL) NOT NULL
- `tax_amount` (REAL) DEFAULT 0.0
- `shipping_cost` (REAL) DEFAULT 0.0
- `total_amount` (REAL) NOT NULL
- `notes` (TEXT)

**Foreign Keys:**
- `payment_method_id` → `payment_methods.payment_method_id`
- `shipping_address_id` → `shipping_addresses.address_id`
- `customer_id` → `customers.customer_id`

**Sample Data:**
```
(1, 1, 1, 1, '2023-05-10 10:30:00', 'completed', 1299.99, 129.99, 15.0, 1444.98, 'Express delivery')
(2, 1, 1, 1, '2023-05-15 14:20:00', 'completed', 79.99, 8.0, 5.0, 92.99, None)
(3, 2, 3, 3, '2023-05-12 09:15:00', 'completed', 1499.99, 150.0, 20.0, 1669.99, 'Gift wrapped')
```

### payment_methods

**Columns:**
- `payment_method_id` (INTEGER) 🔑
- `customer_id` (INTEGER) NOT NULL
- `method_type` (TEXT) NOT NULL
- `card_number` (TEXT)
- `expiry_date` (TEXT)
- `card_holder_name` (TEXT)
- `is_default` (BOOLEAN) DEFAULT 0
- `is_active` (BOOLEAN) DEFAULT 1
- `created_at` (TIMESTAMP) DEFAULT CURRENT_TIMESTAMP

**Foreign Keys:**
- `customer_id` → `customers.customer_id`

**Sample Data:**
```
(1, 1, 'credit_card', '4111-1111-1111-1111', '12/25', 'John Smith', 1, 1, '2025-09-01 05:48:45')
(2, 1, 'paypal', None, None, 'John Smith', 0, 1, '2025-09-01 05:48:45')
(3, 2, 'credit_card', '4222-2222-2222-2222', '03/26', 'Sarah Johnson', 1, 1, '2025-09-01 05:48:45')
```

### product_tags

**Columns:**
- `product_id` (INTEGER) 🔑 NOT NULL
- `tag_name` (TEXT) 🔑 NOT NULL

**Foreign Keys:**
- `product_id` → `products.product_id`

**Sample Data:**
```
(1, 'laptop')
(1, 'apple')
(1, 'professional')
```

### products

**Columns:**
- `product_id` (INTEGER) 🔑
- `name` (TEXT) NOT NULL
- `description` (TEXT)
- `category_id` (INTEGER) NOT NULL
- `supplier_id` (INTEGER) NOT NULL
- `sku` (TEXT) NOT NULL
- `price` (REAL) NOT NULL
- `cost_price` (REAL) NOT NULL
- `weight` (REAL)
- `dimensions` (TEXT)
- `is_active` (BOOLEAN) DEFAULT 1
- `created_at` (TIMESTAMP) DEFAULT CURRENT_TIMESTAMP

**Foreign Keys:**
- `supplier_id` → `suppliers.supplier_id`
- `category_id` → `categories.category_id`

**Sample Data:**
```
(1, 'MacBook Pro 13"', 'Apple MacBook Pro with M2 chip', 13, 1, 'MBP13-001', 1299.99, 800.0, 1.4, '12.3" x 8.6" x 0.6"', 1, '2025-09-01 05:48:45')
(2, 'Dell XPS 15', 'Dell XPS 15 laptop with Intel i7', 13, 1, 'DXP15-001', 1499.99, 900.0, 2.1, '13.6" x 9.1" x 0.7"', 1, '2025-09-01 05:48:45')
(3, 'iPhone 15 Pro', 'Apple iPhone 15 Pro 128GB', 14, 1, 'IP15P-001', 999.99, 600.0, 0.19, '5.8" x 2.8" x 0.3"', 1, '2025-09-01 05:48:45')
```

### reviews

**Columns:**
- `review_id` (INTEGER) 🔑
- `product_id` (INTEGER) NOT NULL
- `customer_id` (INTEGER) NOT NULL
- `order_id` (INTEGER) NOT NULL
- `rating` (INTEGER) NOT NULL
- `title` (TEXT)
- `comment` (TEXT)
- `review_date` (TIMESTAMP) DEFAULT CURRENT_TIMESTAMP
- `is_verified_purchase` (BOOLEAN) DEFAULT 1

**Foreign Keys:**
- `order_id` → `orders.order_id`
- `customer_id` → `customers.customer_id`
- `product_id` → `products.product_id`

**Sample Data:**
```
(1, 1, 1, 1, 5, 'Excellent laptop', 'Great performance and battery life', '2025-09-01 05:48:45', 1)
(2, 1, 1, 2, 4, 'Good mouse', 'Comfortable and responsive', '2025-09-01 05:48:45', 1)
(3, 2, 2, 3, 5, 'Perfect for work', 'Fast and reliable', '2025-09-01 05:48:45', 1)
```

### shipping_addresses

**Columns:**
- `address_id` (INTEGER) 🔑
- `customer_id` (INTEGER) NOT NULL
- `address_line1` (TEXT) NOT NULL
- `address_line2` (TEXT)
- `city` (TEXT) NOT NULL
- `state` (TEXT)
- `country` (TEXT) NOT NULL
- `postal_code` (TEXT) NOT NULL
- `is_default` (BOOLEAN) DEFAULT 0
- `created_at` (TIMESTAMP) DEFAULT CURRENT_TIMESTAMP

**Foreign Keys:**
- `customer_id` → `customers.customer_id`

**Sample Data:**
```
(1, 1, '123 Main St', 'Apt 4B', 'New York', 'NY', 'USA', '10001', 1, '2025-09-01 05:48:45')
(2, 1, '456 Oak Ave', None, 'Brooklyn', 'NY', 'USA', '11201', 0, '2025-09-01 05:48:45')
(3, 2, '789 Pine Rd', 'Suite 100', 'Los Angeles', 'CA', 'USA', '90210', 1, '2025-09-01 05:48:45')
```

### sqlite_sequence

**Columns:**
- `name` ()
- `seq` ()

**Sample Data:**
```
('categories', 15)
('suppliers', 5)
('products', 15)
```

### suppliers

**Columns:**
- `supplier_id` (INTEGER) 🔑
- `name` (TEXT) NOT NULL
- `email` (TEXT) NOT NULL
- `phone` (TEXT)
- `address` (TEXT)
- `country` (TEXT)
- `rating` (REAL) DEFAULT 0.0
- `is_active` (BOOLEAN) DEFAULT 1
- `created_at` (TIMESTAMP) DEFAULT CURRENT_TIMESTAMP

**Sample Data:**
```
(1, 'TechCorp', 'tech@techcorp.com', '+1-555-0101', '123 Tech St, Silicon Valley', 'USA', 4.5, 1, '2025-09-01 05:48:45')
(2, 'FashionHub', 'contact@fashionhub.com', '+1-555-0102', '456 Fashion Ave, NYC', 'USA', 4.2, 1, '2025-09-01 05:48:45')
(3, 'HomeGoods Inc', 'sales@homegoods.com', '+1-555-0103', '789 Home Rd, Chicago', 'USA', 4.0, 1, '2025-09-01 05:48:45')
```

## Relationships

### categories
- **References**: categories
- **Referenced by**: products

### customers
- **Referenced by**: orders, payment_methods, reviews, shipping_addresses

### inventory
- **References**: products

### order_items
- **References**: products, orders

### orders
- **References**: payment_methods, shipping_addresses, customers
- **Referenced by**: order_items, reviews

### payment_methods
- **References**: customers
- **Referenced by**: orders

### product_tags
- **References**: products

### products
- **References**: suppliers, categories
- **Referenced by**: inventory, order_items, product_tags, reviews

### reviews
- **References**: orders, customers, products

### shipping_addresses
- **References**: customers
- **Referenced by**: orders

### suppliers
- **Referenced by**: products

## Hierarchical Relationships

- **categories**: Self-referencing (hierarchical structure)

## Many-to-Many Relationships

- **products ↔ orders (via order_items)**
- **suppliers ↔ categories (via products)**

## Join Examples

### LEFT JOIN: orders → customers
```sql
SELECT * FROM orders LEFT JOIN customers ON orders.customers_id = customers.id
```

### LEFT JOIN: payment_methods → customers
```sql
SELECT * FROM payment_methods LEFT JOIN customers ON payment_methods.customers_id = customers.id
```

### LEFT JOIN: reviews → customers
```sql
SELECT * FROM reviews LEFT JOIN customers ON reviews.customers_id = customers.id
```

### LEFT JOIN: shipping_addresses → customers
```sql
SELECT * FROM shipping_addresses LEFT JOIN customers ON shipping_addresses.customers_id = customers.id
```

### INNER JOIN: order_items → products
```sql
SELECT * FROM order_items INNER JOIN products ON order_items.id = products.order_items_id
```

### INNER JOIN: order_items → orders
```sql
SELECT * FROM order_items INNER JOIN orders ON order_items.id = orders.order_items_id
```

### INNER JOIN: orders → payment_methods
```sql
SELECT * FROM orders INNER JOIN payment_methods ON orders.id = payment_methods.orders_id
```

### INNER JOIN: orders → shipping_addresses
```sql
SELECT * FROM orders INNER JOIN shipping_addresses ON orders.id = shipping_addresses.orders_id
```

### INNER JOIN: orders → customers
```sql
SELECT * FROM orders INNER JOIN customers ON orders.id = customers.orders_id
```

### LEFT JOIN: order_items → orders
```sql
SELECT * FROM order_items LEFT JOIN orders ON order_items.orders_id = orders.id
```

### LEFT JOIN: reviews → orders
```sql
SELECT * FROM reviews LEFT JOIN orders ON reviews.orders_id = orders.id
```

### INNER JOIN: products → suppliers
```sql
SELECT * FROM products INNER JOIN suppliers ON products.id = suppliers.products_id
```

### INNER JOIN: products → categories
```sql
SELECT * FROM products INNER JOIN categories ON products.id = categories.products_id
```

### LEFT JOIN: inventory → products
```sql
SELECT * FROM inventory LEFT JOIN products ON inventory.products_id = products.id
```

### LEFT JOIN: order_items → products
```sql
SELECT * FROM order_items LEFT JOIN products ON order_items.products_id = products.id
```

### LEFT JOIN: product_tags → products
```sql
SELECT * FROM product_tags LEFT JOIN products ON product_tags.products_id = products.id
```

### LEFT JOIN: reviews → products
```sql
SELECT * FROM reviews LEFT JOIN products ON reviews.products_id = products.id
```

### INNER JOIN: reviews → orders
```sql
SELECT * FROM reviews INNER JOIN orders ON reviews.id = orders.reviews_id
```

### INNER JOIN: reviews → customers
```sql
SELECT * FROM reviews INNER JOIN customers ON reviews.id = customers.reviews_id
```

### INNER JOIN: reviews → products
```sql
SELECT * FROM reviews INNER JOIN products ON reviews.id = products.reviews_id
```

## Complex Relationship Examples

**Relationship Paths:**
- `categories` → `categories`
- `inventory` → `products`
- `order_items` → `products`
- `order_items` → `orders`
- `orders` → `payment_methods`
- `orders` → `shipping_addresses`
- `orders` → `customers`
- `payment_methods` → `customers`
- `product_tags` → `products`
- `products` → `suppliers`
- `products` → `categories`
- `reviews` → `orders`
- `reviews` → `customers`
- `reviews` → `products`
- `shipping_addresses` → `customers`

## Natural Language Query Examples

Based on the schema analysis, here are example queries you can try:

### Basic Queries
- "Show me all records from categories"
- "List categories with their details"
- "Show me all records from customers"
- "List customers with their details"
- "Show me all records from inventory"
- "List inventory with their details"
- "Show me all records from order_items"
- "List order_items with their details"
- "Show me all records from orders"
- "List orders with their details"
- "Show me all records from payment_methods"
- "List payment_methods with their details"
- "Show me all records from product_tags"
- "List product_tags with their details"
- "Show me all records from products"
- "List products with their details"
- "Show me all records from reviews"
- "List reviews with their details"
- "Show me all records from shipping_addresses"
- "List shipping_addresses with their details"
- "Show me all records from sqlite_sequence"
- "List sqlite_sequence with their details"
- "Show me all records from suppliers"
- "List suppliers with their details"

### Relationship Queries
- "Show categories with their categories information"
- "List categories and their related categories"
- "Show inventory with their products information"
- "List inventory and their related products"
- "Show order_items with their products information"
- "List order_items and their related products"
- "Show order_items with their orders information"
- "List order_items and their related orders"
- "Show orders with their payment_methods information"
- "List orders and their related payment_methods"
- "Show orders with their shipping_addresses information"
- "List orders and their related shipping_addresses"
- "Show orders with their customers information"
- "List orders and their related customers"
- "Show payment_methods with their customers information"
- "List payment_methods and their related customers"
- "Show product_tags with their products information"
- "List product_tags and their related products"
- "Show products with their suppliers information"
- "List products and their related suppliers"
- "Show products with their categories information"
- "List products and their related categories"
- "Show reviews with their orders information"
- "List reviews and their related orders"
- "Show reviews with their customers information"
- "List reviews and their related customers"
- "Show reviews with their products information"
- "List reviews and their related products"
- "Show shipping_addresses with their customers information"
- "List shipping_addresses and their related customers"

### Aggregation Queries
- "How many records are in categories?"
- "Show the total count by category in categories"
- "How many records are in customers?"
- "Show the total count by category in customers"
- "How many records are in inventory?"
- "Show the total count by category in inventory"
- "How many records are in order_items?"
- "Show the total count by category in order_items"
- "How many records are in orders?"
- "Show the total count by category in orders"
- "How many records are in payment_methods?"
- "Show the total count by category in payment_methods"
- "How many records are in product_tags?"
- "Show the total count by category in product_tags"
- "How many records are in products?"
- "Show the total count by category in products"
- "How many records are in reviews?"
- "Show the total count by category in reviews"
- "How many records are in shipping_addresses?"
- "Show the total count by category in shipping_addresses"
- "How many records are in sqlite_sequence?"
- "Show the total count by category in sqlite_sequence"
- "How many records are in suppliers?"
- "Show the total count by category in suppliers"

### Complex Queries
- "Show data from categories and customers together"
- "Find records that exist in both categories and customers"

