#!/usr/bin/env python3
"""
Integration Example: Using Generated Schema in Natural Language to SQL App
This shows how to use the generated markdown schema in your NL-to-SQL application.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class NLToSQLWithSchema:
    """Natural Language to SQL converter using generated schema."""
    
    def __init__(self, schema_file_path):
        """Initialize with path to generated schema markdown file."""
        self.schema_file_path = schema_file_path
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.schema_content = self.load_schema()
    
    def load_schema(self):
        """Load the generated schema markdown file."""
        try:
            with open(self.schema_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"✅ Loaded schema from: {self.schema_file_path}")
            return content
        except FileNotFoundError:
            print(f"❌ Schema file not found: {self.schema_file_path}")
            return None
    
    def generate_sql(self, natural_language_query):
        """Generate SQL from natural language using the schema."""
        
        if not self.schema_content:
            return "Error: Schema not loaded"
        
        prompt = f"""
You are a SQL expert. Convert the following natural language query to SQL.

Database Schema:
{self.schema_content}

Natural Language Query: {natural_language_query}

CRITICAL RULES:
1. ALWAYS check if the requested data is already available in a single table before using joins
2. Use pre-calculated fields when available (e.g., customers.total_spent, customers.total_orders)
3. Only use JOINs when you need data from multiple tables
4. Prefer simple queries over complex ones when they achieve the same result
5. Use appropriate JOIN types (INNER JOIN, LEFT JOIN) based on the query needs
6. Use proper aggregation functions (COUNT, SUM, AVG, MAX, MIN) when needed
7. Apply appropriate filtering with WHERE clauses
8. Use GROUP BY and HAVING for grouped aggregations
9. Use ORDER BY and LIMIT for sorting and limiting results
10. Use meaningful table aliases for readability
11. Return ONLY the SQL query, no explanations

SQL Query:
"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0
            )
            
            sql_query = response.choices[0].message.content.strip()
            return sql_query
            
        except Exception as e:
            return f"Error generating SQL: {str(e)}"
    
    def test_queries(self):
        """Test the system with example queries."""
        
        test_queries = [
            "Show me all customers with their total spending and order count",
            "List products with their categories and suppliers",
            "Find customers who have placed orders",
            "Show the average rating by product category",
            "List orders with their customer names and shipping addresses",
            "Find products with low inventory that need reordering",
            "Show customers and their payment methods",
            "List products with their reviews and ratings"
        ]
        
        print("🧪 Testing Natural Language to SQL with Generated Schema")
        print("=" * 60)
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n{i}. Query: {query}")
            sql = self.generate_sql(query)
            print(f"   SQL: {sql}")
            print("-" * 60)

def main():
    """Main function to demonstrate the integration."""
    
    # Path to the generated schema file
    schema_file = "ecommerce_database_schema.md"
    
    print("🚀 Natural Language to SQL with Generated Schema")
    print("=" * 50)
    
    # Check if schema file exists
    if not os.path.exists(schema_file):
        print(f"❌ Schema file not found: {schema_file}")
        print("Please run 'python db_schema_analyzer.py' first to generate the schema.")
        return 1
    
    # Initialize the NL-to-SQL converter
    nl_sql = NLToSQLWithSchema(schema_file)
    
    # Test with example queries
    nl_sql.test_queries()
    
    print("\n🎉 Integration test complete!")
    print("\nTo use this in your own app:")
    print("1. Generate schema: python db_schema_analyzer.py")
    print("2. Load schema in your app: nl_sql = NLToSQLWithSchema('schema.md')")
    print("3. Generate SQL: sql = nl_sql.generate_sql('your query')")
    
    return 0

if __name__ == "__main__":
    exit(main())
