# Natural Language to SQL Query Tool

This project demonstrates natural language to SQL conversion using OpenAI's GPT models with progressively complex database schemas.

## Project Structure

### 1. Simple Single Table (`1_Simple_single_table/`)
- **Single table**: `customers` with basic customer information
- **Features**: Basic queries, filtering, sorting, aggregations
- **Example queries**: "Show me all customers from the USA", "Find customers who spent more than $1000"

### 2. Two Tables with Joins (`2_Two_tables_with_joins/`)
- **Two tables**: `customers` and `orders` with foreign key relationship
- **Features**: INNER JOIN, LEFT JOIN, aggregations across tables
- **Example queries**: "Show me all customers with their total order amounts", "Find customers who have placed more than 2 orders"

### 3. Complex E-commerce Database (`3_Complex_ecommerce_database/`)
- **11+ tables**: Comprehensive e-commerce schema with complex relationships
- **Features**: All join types, hierarchical data, many-to-many relationships, complex aggregations
- **Example queries**: "Show me all customers with their total spending and order count", "Find products with low inventory that need reordering"

### 4. TicketQueue System (`4_TicketQueue/`)
- **8+ tables**: Comprehensive ticket management system with role-based access
- **Features**: Complex joins, dependencies, file attachments, time tracking, priority management
- **Example queries**: "Show me all ticket items assigned to Bob Developer", "List ticket queues with high priority", "Find overdue ticket items"

## Setup Instructions

### Prerequisites
- Python 3.7+
- OpenAI API key

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd DB_SQL_Natural_Language
```

2. **Install dependencies for each example**
```bash
# For each example directory
cd 1_Simple_single_table
pip install -r requirements.txt

cd ../2_Two_tables_with_joins
pip install -r requirements.txt

cd ../3_Complex_ecommerce_database
pip install -r requirements.txt

cd ../4_TicketQueue
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
# Copy the example environment file
cp env_example.txt .env

# Edit .env and add your OpenAI API key
OPENAI_API_KEY=your-openai-api-key-here
```

4. **Create the database**
```bash
# For each example
python setup_database.py
```

5. **Run the application**
```bash
python main.py
```

## Usage

Each example provides a Gradio web interface where you can:

1. **Enter natural language queries** in plain English
2. **View the generated SQL** that the AI creates
3. **See the query results** from the database
4. **Try example queries** provided in the interface

## Key Features

### Natural Language Processing
- Converts plain English to SQL queries
- Handles complex relationships and joins
- Supports aggregations, filtering, and sorting
- Uses OpenAI GPT models for intelligent query generation

### Database Schema Awareness
- AI understands table relationships
- Recognizes pre-calculated fields
- Generates appropriate JOIN types
- Handles hierarchical and many-to-many relationships

### Progressive Complexity
- Start with simple single-table queries
- Progress to multi-table joins
- Advance to complex e-commerce scenarios

## Example Queries by Complexity

### Simple (Single Table)
- "Show me all customers from the USA"
- "Find customers who spent more than $1000"
- "List customers by age, youngest first"

### Intermediate (Two Tables)
- "Show me all customers with their total order amounts"
- "Find customers who have placed more than 2 orders"
- "List orders with customer names and product details"

### Advanced (Complex Schema)
- "Show me all customers with their total spending and order count"
- "Find products with low inventory that need reordering"
- "Show average rating by product category"
- "Find customers who haven't ordered in the last 30 days"

### Enterprise (Ticket Management)
- "Show me all ticket items assigned to Bob Developer"
- "List ticket queues with high priority"
- "Find overdue ticket items"
- "Show ticket items with their dependencies"

## Technology Stack

- **Backend**: Python, SQLite
- **AI/ML**: OpenAI GPT-3.5-turbo
- **Web Interface**: Gradio
- **Database**: SQLite with complex schemas

## Security Notes

- **Never commit `.env` files** - they contain sensitive API keys
- **Database files are excluded** from version control
- **Use environment variables** for configuration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with different query types
5. Submit a pull request

## License

This project is for educational purposes. Please respect OpenAI's terms of service when using their API.
