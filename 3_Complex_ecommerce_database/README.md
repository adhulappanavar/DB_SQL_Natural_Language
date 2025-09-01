# Natural Language to SQL - Complex E-commerce Database

This example demonstrates natural language to SQL conversion with a comprehensive e-commerce database containing 11+ tables with complex relationships and all types of joins.

## Database Schema

### Core Tables

#### 1. Categories Table
- `category_id` (PRIMARY KEY)
- `name`
- `description`
- `parent_category_id` (SELF-REFERENCING FK)
- `is_active`
- `created_at`

#### 2. Suppliers Table
- `supplier_id` (PRIMARY KEY)
- `name`
- `email`
- `phone`
- `address`
- `country`
- `rating`
- `is_active`
- `created_at`

#### 3. Products Table
- `product_id` (PRIMARY KEY)
- `name`
- `description`
- `category_id` (FK to categories)
- `supplier_id` (FK to suppliers)
- `sku`
- `price`
- `cost_price`
- `weight`
- `dimensions`
- `is_active`
- `created_at`

#### 4. Customers Table
- `customer_id` (PRIMARY KEY)
- `first_name`
- `last_name`
- `email`
- `phone`
- `date_of_birth`
- `registration_date`
- `is_active`
- `total_orders`
- `total_spent`

#### 5. Shipping Addresses Table
- `address_id` (PRIMARY KEY)
- `customer_id` (FK to customers)
- `address_line1`
- `address_line2`
- `city`
- `state`
- `country`
- `postal_code`
- `is_default`
- `created_at`

#### 6. Payment Methods Table
- `payment_method_id` (PRIMARY KEY)
- `customer_id` (FK to customers)
- `method_type`
- `card_number`
- `expiry_date`
- `card_holder_name`
- `is_default`
- `is_active`
- `created_at`

#### 7. Orders Table
- `order_id` (PRIMARY KEY)
- `customer_id` (FK to customers)
- `shipping_address_id` (FK to shipping_addresses)
- `payment_method_id` (FK to payment_methods)
- `order_date`
- `status`
- `subtotal`
- `tax_amount`
- `shipping_cost`
- `total_amount`
- `notes`

#### 8. Order Items Table
- `order_item_id` (PRIMARY KEY)
- `order_id` (FK to orders)
- `product_id` (FK to products)
- `quantity`
- `unit_price`
- `total_price`

#### 9. Inventory Table
- `inventory_id` (PRIMARY KEY)
- `product_id` (FK to products)
- `warehouse_location`
- `quantity_in_stock`
- `reorder_level`
- `last_updated`

#### 10. Reviews Table
- `review_id` (PRIMARY KEY)
- `product_id` (FK to products)
- `customer_id` (FK to customers)
- `order_id` (FK to orders)
- `rating`
- `title`
- `comment`
- `review_date`
- `is_verified_purchase`

#### 11. Product Tags Table (Many-to-Many)
- `product_id` (FK to products)
- `tag_name`

## Complex Relationships

### Hierarchical Relationships
- **Categories**: Self-referencing (parent_category_id → category_id)
- **Product Categories**: Electronics → Computers → Laptops

### One-to-Many Relationships
- **Customer → Orders**: One customer can have multiple orders
- **Customer → Addresses**: One customer can have multiple shipping addresses
- **Customer → Payment Methods**: One customer can have multiple payment methods
- **Product → Order Items**: One product can be in multiple order items
- **Product → Inventory**: One product can have inventory in multiple warehouses
- **Product → Reviews**: One product can have multiple reviews

### Many-to-Many Relationships
- **Products ↔ Tags**: Products can have multiple tags, tags can be on multiple products

### Complex Join Paths
- `customers → orders → order_items → products → categories`
- `customers → shipping_addresses → orders`
- `customers → payment_methods → orders`
- `suppliers → products → order_items → orders`
- `products → inventory (stock levels)`
- `products → reviews (customer feedback)`

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your OpenAI API key:
```bash
cp env_example.txt .env
# Edit .env and add your OpenAI API key
```

3. Create the database:
```bash
python setup_database.py
```

4. Run the application:
```bash
python main.py
```

## Example Complex Queries

The application can handle sophisticated queries involving multiple joins, aggregations, and complex filtering:

### Customer Analytics
- "Show me all customers with their total spending and order count"
- "List top 5 customers by total spending with their preferred payment methods"
- "Find customers who haven't ordered in the last 30 days"
- "Show customers and their shipping addresses by country"

### Inventory Management
- "Find products with low inventory that need reordering"
- "List products with their inventory levels and supplier information"
- "Show inventory levels by warehouse location"

### Sales & Revenue Analysis
- "Show revenue by supplier and country"
- "Find the most profitable products by supplier"
- "Show order status distribution by customer country"

### Product Analysis
- "Show average rating by product category"
- "List products with tags and their average ratings"
- "List products in Electronics category with their reviews"

### Order Analysis
- "Find orders with multiple items and their total values"
- "Find customers who have reviewed products they purchased"

## Join Types Demonstrated

### INNER JOIN
- Customer orders with product details
- Products with their categories and suppliers

### LEFT JOIN
- Customers with their orders (including those without orders)
- Products with inventory (including products without inventory)

### Self-JOIN
- Category hierarchies (parent-child relationships)

### Multiple Table Joins
- Customer → Order → Order Items → Products → Categories
- Products → Reviews → Customers

### Subqueries and CTEs
- Complex aggregations and filtering
- Ranking and window functions

## Key Features

- **11+ interconnected tables** with realistic e-commerce data
- **All join types**: INNER, LEFT, RIGHT, SELF, and complex multi-table joins
- **Hierarchical data**: Category parent-child relationships
- **Many-to-many relationships**: Product tags
- **Complex aggregations**: Revenue analysis, customer analytics
- **Realistic data**: 10 customers, 15 products, 18 orders, 11 reviews
- **Multiple warehouses**: Inventory across different locations
- **Payment methods**: Credit cards, PayPal, etc.
- **International data**: Customers from multiple countries

## Sample Data Included

- **Categories**: 15 categories with hierarchical structure
- **Suppliers**: 5 suppliers from different countries
- **Products**: 15 products across electronics, clothing, home & garden
- **Customers**: 10 customers from 6 countries
- **Orders**: 18 orders with various statuses and amounts
- **Inventory**: Stock levels across 3 warehouses
- **Reviews**: 11 verified purchase reviews
- **Tags**: 45 product tags for categorization
