#!/usr/bin/env python3
"""
Test script for the Natural Language to SQL system
Tests database connectivity and basic functionality without requiring OpenAI API
"""

import sqlite3
import os
import sys

# Add the current directory to the path so we can import functions
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import functions directly to avoid OpenAI dependency
def get_ticketqueue_schema():
    """Get the schema of all tables in the TicketQueue database."""
    conn = sqlite3.connect('ticketqueue.db')
    cursor = conn.cursor()
    
    schema_info = {}
    
    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    tables = cursor.fetchall()
    
    for table in tables:
        table_name = table[0]
        
        # Get table schema
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        # Get sample data (limit to 3 rows)
        try:
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
            sample_data = cursor.fetchall()
        except:
            sample_data = []
        
        schema_info[table_name] = {
            'columns': columns,
            'sample_data': sample_data
        }
    
    conn.close()
    
    # Format schema for prompt
    schema_text = "Database Schema:\n\n"
    
    for table_name, info in schema_info.items():
        schema_text += f"Table: {table_name}\n"
        schema_text += "Columns:\n"
        for col in info['columns']:
            schema_text += f"  - {col[1]} ({col[2]})"
            if col[5]:  # If NOT NULL
                schema_text += " NOT NULL"
            if col[3]:  # If has default value
                schema_text += f" DEFAULT {col[3]}"
            schema_text += "\n"
        
        if info['sample_data']:
            schema_text += "Sample data:\n"
            for row in info['sample_data']:
                schema_text += f"  {row}\n"
        
        schema_text += "\n"
    
    return schema_text

def get_database_stats():
    """Get basic statistics about the TicketQueue database."""
    conn = sqlite3.connect('ticketqueue.db')
    cursor = conn.cursor()
    
    stats = {}
    
    # Count records in each table
    tables = ['users', 'ticket_queue', 'ticket_items', 'ticket_queue_categories',
              'ticket_item_comments', 'ticket_item_attachments', 'ticket_item_dependencies']
    
    for table in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            stats[table] = count
        except:
            stats[table] = 0
    
    conn.close()
    
    stats_text = "Database Statistics:\n\n"
    for table, count in stats.items():
        stats_text += f"{table}: {count} records\n"
    
    return stats_text

def execute_sql(sql_query):
    """Execute SQL query and return results."""
    try:
        conn = sqlite3.connect('ticketqueue.db')
        cursor = conn.cursor()
        
        cursor.execute(sql_query)
        results = cursor.fetchall()
        
        # Get column names
        column_names = [description[0] for description in cursor.description] if cursor.description else []
        
        conn.close()
        
        if not results:
            return "Query executed successfully. No results returned."
        
        # Format results as a table
        if len(results) > 0:
            # Create header
            output = "Query Results:\n"
            output += " | ".join(column_names) + "\n"
            output += "-" * (len(" | ".join(column_names)) + 10) + "\n"
            
            # Add rows
            for row in results:
                output += " | ".join(str(cell) for cell in row) + "\n"
            
            # Add summary
            output += f"\nTotal rows returned: {len(results)}"
        else:
            output = "Query executed successfully. No results returned."
        
        return output
        
    except Exception as e:
        return f"Error executing SQL: {str(e)}"

def test_database_connection():
    """Test if the TicketQueue database exists and is accessible."""
    print("Testing database connection...")
    
    if not os.path.exists('ticketqueue.db'):
        print("❌ TicketQueue database not found!")
        print("Please run 'python init_ticketqueue_db.py' first.")
        return False
    
    try:
        conn = sqlite3.connect('ticketqueue.db')
        cursor = conn.cursor()
        
        # Test basic query
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        
        conn.close()
        
        print(f"✅ Database connection successful!")
        print(f"   Found {user_count} users in the database")
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_schema_generation():
    """Test if the schema generation function works."""
    print("\nTesting schema generation...")
    
    try:
        schema = get_ticketqueue_schema()
        
        if "Table: users" in schema and "Table: ticket_queue" in schema:
            print("✅ Schema generation successful!")
            print(f"   Schema length: {len(schema)} characters")
            return True
        else:
            print("❌ Schema generation failed - missing expected tables")
            return False
            
    except Exception as e:
        print(f"❌ Schema generation failed: {e}")
        return False

def test_database_stats():
    """Test if the database statistics function works."""
    print("\nTesting database statistics...")
    
    try:
        stats = get_database_stats()
        
        if "users:" in stats and "ticket_queue:" in stats:
            print("✅ Database statistics generation successful!")
            print("   Statistics generated successfully")
            return True
        else:
            print("❌ Database statistics generation failed")
            return False
            
    except Exception as e:
        print(f"❌ Database statistics generation failed: {e}")
        return False

def test_sql_execution():
    """Test if SQL execution works with sample queries."""
    print("\nTesting SQL execution...")
    
    test_queries = [
        "SELECT COUNT(*) as user_count FROM users",
        "SELECT COUNT(*) as queue_count FROM ticket_queue",
        "SELECT COUNT(*) as item_count FROM ticket_items",
        "SELECT u.first_name, u.last_name, COUNT(ti.id) as assigned_items FROM users u LEFT JOIN ticket_items ti ON u.id = ti.assigned_to GROUP BY u.id ORDER BY assigned_items DESC"
    ]
    
    for i, query in enumerate(test_queries, 1):
        try:
            result = execute_sql(query)
            
            if "Error" not in result:
                print(f"✅ Test query {i} successful!")
            else:
                print(f"❌ Test query {i} failed: {result}")
                return False
                
        except Exception as e:
            print(f"❌ Test query {i} failed with exception: {e}")
            return False
    
    return True

def test_sample_data():
    """Test if sample data is properly loaded."""
    print("\nTesting sample data...")
    
    try:
        conn = sqlite3.connect('ticketqueue.db')
        cursor = conn.cursor()
        
        # Check key tables have data
        tables_to_check = [
            ('users', 6),
            ('ticket_queue', 6),
            ('ticket_items', 22),
            ('ticket_queue_categories', 6)
        ]
        
        all_good = True
        for table, expected_min in tables_to_check:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            
            if count >= expected_min:
                print(f"✅ {table}: {count} records (expected ≥{expected_min})")
            else:
                print(f"❌ {table}: {count} records (expected ≥{expected_min})")
                all_good = False
        
        conn.close()
        return all_good
        
    except Exception as e:
        print(f"❌ Sample data test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing Natural Language to SQL System")
    print("=" * 50)
    
    tests = [
        test_database_connection,
        test_schema_generation,
        test_database_stats,
        test_sql_execution,
        test_sample_data
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The system is ready to use.")
        print("\nTo start the application:")
        print("1. Set up your OpenAI API key in .env file")
        print("2. Run: python nl_to_sql_main.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\nMake sure to:")
        print("1. Run 'python init_ticketqueue_db.py' to create the database")
        print("2. Check that all dependencies are installed")

if __name__ == "__main__":
    main()
