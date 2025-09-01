# Natural Language to SQL - Two Tables with Joins

This example demonstrates natural language to SQL conversion with a database containing two related tables: `customers` and `orders`.

## Database Schema

### Customers Table
- `customer_id` (PRIMARY KEY)
- `name`
- `email`
- `age`
- `city`
- `country`
- `registration_date`
- `membership_level` (standard, premium, vip)

### Orders Table
- `order_id` (PRIMARY KEY)
- `customer_id` (FOREIGN KEY to customers.customer_id)
- `order_date`
- `product_name`
- `quantity`
- `unit_price`
- `total_amount`
- `status` (pending, shipped, completed)

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

## Example Queries

The application can handle complex queries involving joins, aggregations, and filtering:

- "Show me all customers with their total order amounts"
- "Find customers who have placed more than 2 orders"
- "List orders with customer names and product details"
- "Show the total revenue by country"
- "Find VIP customers who haven't ordered recently"
- "Show average order value by membership level"
- "Which customers have pending orders?"
- "Show top 5 customers by total spending"
- "List all orders from customers in the USA"
- "Show customers and their order counts"

## Key Features

- **Two-table joins**: Handles INNER JOIN, LEFT JOIN operations
- **Aggregations**: Supports COUNT, SUM, AVG, MAX, MIN functions
- **Complex filtering**: WHERE clauses with multiple conditions
- **Grouping**: GROUP BY with HAVING clauses
- **Sorting**: ORDER BY with LIMIT
- **Relationship awareness**: Understands foreign key relationships

## Sample Data

The database includes:
- 10 customers with different membership levels
- 18 orders across various products
- Realistic e-commerce data with different order statuses
