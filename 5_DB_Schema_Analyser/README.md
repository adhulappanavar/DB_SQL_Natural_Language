# Database Schema Analyzer

This tool analyzes any SQLite database and generates comprehensive markdown documentation that can be fed into natural language to SQL conversion systems.

## Features

- **Automatic Schema Discovery**: Analyzes all tables, columns, and relationships
- **Relationship Mapping**: Detects foreign keys, hierarchical structures, and many-to-many relationships
- **Sample Data Extraction**: Includes sample data for better AI understanding
- **Markdown Output**: Generates formatted documentation ready for NL-to-SQL systems
- **Complex Join Examples**: Provides SQL examples for different relationship types

## Quick Start

### 1. Run the Analyzer

```bash
python db_schema_analyzer.py
```

This will:
- Connect to the e-commerce database
- Analyze all tables and relationships
- Generate comprehensive markdown documentation
- Save output to `ecommerce_database_schema.md`

### 2. Use the Output

The generated markdown file contains:
- Complete table schemas with column types and constraints
- Foreign key relationships
- Sample data from each table
- Complex relationship examples
- Natural language query examples
- Join patterns and SQL examples

## Output Format

The generated markdown includes:

### Table Schemas
```markdown
### customers
**Columns:**
- `customer_id` (INTEGER) 🔑 NOT NULL
- `first_name` (TEXT) NOT NULL
- `last_name` (TEXT) NOT NULL
- `email` (TEXT) NOT NULL
```

### Relationships
```markdown
### customers
- **References**: orders
- **Referenced by**: shipping_addresses, payment_methods
```

### Sample Data
```markdown
**Sample Data:**
```
(1, 'John', 'Smith', 'john.smith@email.com', ...)
(2, 'Sarah', 'Johnson', 'sarah.j@email.com', ...)
```

### Natural Language Examples
```markdown
### Basic Queries
- "Show me all records from customers"
- "List products with their details"

### Relationship Queries
- "Show customers with their orders information"
- "List products and their related categories"
```

## Customization

To analyze a different database, modify the `db_path` variable in the `main()` function:

```python
db_path = "/path/to/your/database.db"
```

## Integration with NL-to-SQL Systems

The generated markdown can be directly used in natural language to SQL systems by:

1. **Reading the markdown file** into your NL-to-SQL application
2. **Parsing the schema information** for AI context
3. **Using the relationship examples** to understand complex joins
4. **Referencing sample data** for better query generation

## Example Usage in NL-to-SQL App

```python
# Read the generated schema
with open('ecommerce_database_schema.md', 'r') as f:
    schema_documentation = f.read()

# Use in your NL-to-SQL prompt
prompt = f"""
Database Schema:
{schema_documentation}

Natural Language Query: {user_query}

Generate SQL:
"""
```

## Database Support

Currently supports:
- **SQLite** (primary focus)
- Easily extensible to PostgreSQL, MySQL, etc.

## Output Files

- `ecommerce_database_schema.md` - Complete schema documentation
- Console output with analysis progress and statistics
