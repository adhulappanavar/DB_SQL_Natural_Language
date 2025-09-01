import gradio as gr
import sqlite3
import os
from openai import OpenAI
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_ticketqueue_schema():
    """Get the schema of all tables with sample data and relationships."""
    conn = sqlite3.connect('ticketqueue.db')
    cursor = conn.cursor()
    
    schema = "Complex TicketQueue Management Database Schema:\n\n"
    
    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")
    tables = cursor.fetchall()
    
    # Define table relationships
    relationships = {
        'users': 'Referenced by ticket_queue (assigned_to, created_by), ticket_items (assigned_to), ticket_item_comments, ticket_item_attachments',
        'ticket_queue': 'References users (assigned_to, created_by). Referenced by ticket_items, ticket_queue_category_assignment',
        'ticket_items': 'References ticket_queue, users (assigned_to). Referenced by ticket_item_comments, ticket_item_attachments, ticket_item_dependencies',
        'ticket_item_comments': 'References ticket_items, users',
        'ticket_item_attachments': 'References ticket_items, users (uploaded_by)',
        'ticket_queue_categories': 'Referenced by ticket_queue_category_assignment',
        'ticket_queue_category_assignment': 'Many-to-many relationship between ticket_queue and ticket_queue_categories',
        'ticket_item_dependencies': 'Self-referencing (dependent_item_id, prerequisite_item_id → ticket_items.id)'
    }
    
    # Get schema for each table
    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 2")
        sample_data = cursor.fetchall()
        
        schema += f"Table: {table_name}\n"
        schema += "Columns:\n"
        for col in columns:
            schema += f"  - {col[1]} ({col[2]})"
            if col[5] == 1:  # Primary key
                schema += " [PRIMARY KEY]"
            schema += "\n"
        
        schema += f"Relationships: {relationships.get(table_name, 'None')}\n"
        
        if sample_data:
            schema += f"Sample {table_name} data:\n"
            for row in sample_data:
                schema += f"  {row}\n"
        
        schema += "\n"
    
    # Add complex relationship examples
    schema += "Complex Relationship Examples:\n"
    schema += "- users → ticket_queue → ticket_items → ticket_item_comments\n"
    schema += "- users → ticket_queue → ticket_items → ticket_item_attachments\n"
    schema += "- ticket_queue → ticket_queue_category_assignment → ticket_queue_categories\n"
    schema += "- ticket_items → ticket_item_dependencies (self-referencing for task dependencies)\n"
    schema += "- users → ticket_items (assignment tracking)\n"
    schema += "- ticket_queue → ticket_items (queue management)\n"
    schema += "- ticket_items → ticket_item_comments (collaboration)\n"
    schema += "- ticket_items → ticket_item_attachments (file management)\n"
    
    # Add pre-calculated fields information
    schema += "\nPRE-CALCULATED FIELDS (Use these instead of complex joins when possible):\n"
    schema += "- users.total_assigned_items: Total ticket items assigned to user\n"
    schema += "- users.total_completed_items: Total completed ticket items for user\n"
    schema += "- users.total_estimated_hours: Total estimated hours for user's tasks\n"
    schema += "- users.total_actual_hours: Total actual hours spent by user\n"
    schema += "- ticket_queue.total_estimated_hours: Total estimated hours for all ticket items in queue\n"
    schema += "- ticket_queue.total_actual_hours: Total actual hours for all ticket items in queue\n"
    schema += "- ticket_queue.total_ticket_items: Total number of ticket items in queue\n"
    schema += "- ticket_queue.completed_ticket_items: Number of completed ticket items in queue\n"
    schema += "- ticket_items.estimated_hours: Pre-calculated time estimates\n"
    schema += "- ticket_items.actual_hours: Actual time spent on tasks\n"
    
    conn.close()
    return schema

def nl2sql(nl_query):
    """Convert natural language to SQL using OpenAI."""
    
    schema = get_ticketqueue_schema()
    
    prompt = f"""
You are a SQL expert specializing in TicketQueue management systems. Convert the following natural language query to SQL.

{schema}

Natural Language Query: {nl_query}

CRITICAL RULES:
1. ALWAYS check if the requested data is already available in a single table before using joins
2. Use pre-calculated fields when available (e.g., ticket_items.estimated_hours, ticket_items.actual_hours)
3. Only use JOINs when you need data from multiple tables
4. Prefer simple queries over complex ones when they achieve the same result
5. Use appropriate JOIN types (INNER JOIN, LEFT JOIN) based on the query needs
6. Use proper aggregation functions (COUNT, SUM, AVG, MAX, MIN) when needed
7. Apply appropriate filtering with WHERE clauses
8. Use GROUP BY and HAVING for grouped aggregations
9. Use ORDER BY and LIMIT for sorting and limiting results
10. Use meaningful table aliases for readability
11. Handle self-referencing relationships properly (ticket_item_dependencies)
12. Consider many-to-many relationships (ticket_queue_category_assignment)
13. For "overdue" queries: use ticket_items.due_date < datetime('now') AND status != 'completed'
14. For "over budget" queries: use actual_hours > estimated_hours
15. Return ONLY the SQL query, no explanations

EXAMPLES:
- "Show users with their ticket load summary" → SELECT first_name, last_name, total_assigned_items, total_completed_items, total_estimated_hours, total_actual_hours FROM users
- "Show ticket queues with their progress" → SELECT title, total_ticket_items, completed_ticket_items, total_estimated_hours, total_actual_hours FROM ticket_queue
- "Show ticket items that are overdue" → SELECT ti.title, ti.due_date, ti.estimated_hours, ti.actual_hours, u.first_name || ' ' || u.last_name as assigned_to FROM ticket_items ti LEFT JOIN users u ON ti.assigned_to = u.id WHERE ti.due_date < datetime('now') AND ti.status != 'completed'
- "Show ticket items that are over budget" → SELECT ti.title, ti.estimated_hours, ti.actual_hours, (ti.actual_hours - ti.estimated_hours) as hours_over_budget FROM ticket_items ti WHERE ti.actual_hours > ti.estimated_hours
- "Show users with their assigned ticket items" → SELECT u.first_name, u.last_name, ti.title FROM users u LEFT JOIN ticket_items ti ON u.id = ti.assigned_to
- "Show ticket queues with their categories" → SELECT tq.title, tqc.name FROM ticket_queue tq JOIN ticket_queue_category_assignment tqca ON tq.id = tqca.ticket_queue_id JOIN ticket_queue_categories tqc ON tqca.category_id = tqc.id
- "Show ticket items with their dependencies" → SELECT dep.title as dependent_item, pre.title as prerequisite FROM ticket_item_dependencies tid JOIN ticket_items dep ON tid.dependent_item_id = dep.id JOIN ticket_items pre ON tid.prerequisite_item_id = pre.id
- "Show ticket items with dependencies, users, and ticket queue" → SELECT dep.title as dependent_item, pre.title as prerequisite, u.first_name || ' ' || u.last_name as assigned_user, tq.title as ticket_queue FROM ticket_item_dependencies tid JOIN ticket_items dep ON tid.dependent_item_id = dep.id JOIN ticket_items pre ON tid.prerequisite_item_id = pre.id LEFT JOIN users u ON dep.assigned_to = u.id LEFT JOIN ticket_queue tq ON dep.ticket_queue_id = tq.id
- "Show ticket items with comments from assigned users" → SELECT ti.title, tic.comment, u.first_name || ' ' || u.last_name as comment_author FROM ticket_items ti JOIN ticket_item_comments tic ON ti.id = tic.ticket_item_id JOIN users u ON tic.user_id = u.id WHERE u.id = ti.assigned_to
- "Show ticket queues with categories and assigned users" → SELECT tq.title, tqc.name as category, u.first_name || ' ' || u.last_name as assigned_user FROM ticket_queue tq LEFT JOIN ticket_queue_category_assignment tqca ON tq.id = tqca.ticket_queue_id LEFT JOIN ticket_queue_categories tqc ON tqca.category_id = tqc.id LEFT JOIN users u ON tq.assigned_to = u.id
- "Show ticket items with dependencies and attachment count" → SELECT ti.title, COUNT(tid.dependent_item_id) as dependency_count, COUNT(tia.id) as attachment_count FROM ticket_items ti LEFT JOIN ticket_item_dependencies tid ON ti.id = tid.dependent_item_id LEFT JOIN ticket_item_attachments tia ON ti.id = tia.ticket_item_id GROUP BY ti.id, ti.title

SQL Query:
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0
        )
        
        sql_query = response.choices[0].message.content.strip()
        return sql_query
        
    except Exception as e:
        return f"Error generating SQL: {str(e)}"

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

def query_ticketqueue_with_nl(nl_query):
    """Converts natural language to SQL and executes the query."""
    if not nl_query.strip():
        return "Please enter a natural language query."
    
    # Convert NL to SQL
    sql_query = nl2sql(nl_query)
    
    # Execute SQL
    results = execute_sql(sql_query)
    
    # Format output
    output = f"Natural Language Query: {nl_query}\n\n"
    output += f"Generated SQL: {sql_query}\n\n"
    output += results
    
    return output

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

# Check if database exists
if not os.path.exists('ticketqueue.db'):
    print("TicketQueue database not found. Please run 'python init_ticketqueue_db.py' first to create the database.")
    exit(1)

# Create Gradio interface
iface = gr.Interface(
    fn=query_ticketqueue_with_nl,
    inputs=gr.Textbox(
        label="Natural Language Query",
        placeholder="e.g., Show me all ticket items assigned to Bob Developer",
        lines=3
    ),
    outputs=gr.Textbox(
        label="SQL Query and Results",
        lines=25
    ),
    title="TicketQueue Natural Language to SQL Query Tool",
    description="Ask questions about the TicketQueue database in plain English",
    examples=[
        "Show me all ticket items assigned to Bob Developer",
        "List all ticket queues with high priority",
        "Find completed ticket items with their assigned users",
        "Show ticket items that are in progress",
        "How many ticket items does each user have assigned?",
        "What's the average estimated hours for ticket items?",
        "Show ticket queues with their categories",
        "List ticket items with their dependencies",
        "Find users with the most completed tasks",
        "Show ticket items that are overdue",
        "Display ticket items with comments",
        "List ticket queues by status",
        "Show users with their total assigned ticket items and completion rate",
        "Find ticket queues with multiple categories and their assigned users",
        "List ticket items with their prerequisites and estimated completion time",
        "Show ticket items with attachments and their uploaders",
        "Find users who have commented on ticket items they're assigned to",
        "Show ticket queues by priority with their total estimated hours",
        "List ticket items with dependencies and their current status",
        "Find ticket items that are blocking other tasks",
        "Show users with their ticket load by ticket queue",
        "List ticket items with comments and their assigned users",
        "Find ticket queues with high priority items that are behind schedule",
        "Show ticket items with their estimated vs actual hours",
        "List users with their role and assigned ticket items by status",
        "Show ticket items with their dependencies, assigned users, and ticket queue information",
        "Find users who have both assigned ticket items and have made comments on other ticket items",
        "Show ticket queues with their categories, assigned users, and total ticket items count",
        "List ticket items with their dependencies, comments count, and attachment count",
        "Find ticket items that are overdue with their assigned users, ticket queue, and priority level",
        "Show users with their assigned ticket items, ticket queue information, and completion status",
        "List ticket items with their prerequisites, assigned users, and estimated vs actual hours",
        "Find ticket queues with multiple categories, assigned users, and ticket items by status",
        "Show ticket items with their dependencies, comments from assigned users, and attachments",
        "List users with their role, assigned ticket items, and ticket queues they're managing",
        "Find ticket items that are blocking other tasks with their assigned users and ticket queue details",
        "Show ticket queues with their categories, assigned users, and overdue ticket items count",
        "List ticket items with their dependencies, comments from all users, and attachment information",
        "Find users who have commented on ticket items they're not assigned to",
        "Show ticket items with their prerequisites, assigned users, ticket queue, and category information",
        "List ticket queues with their assigned users, ticket items by priority, and completion statistics",
        "Find ticket items with multiple dependencies, their assigned users, and ticket queue details",
        "Show users with their assigned ticket items, ticket queue information, and performance metrics",
        "List ticket items with their dependencies, comments from assigned users, and attachment details",
        "Find ticket queues with high priority overdue items, their assigned users, and category information"
    ],
    theme=gr.themes.Soft()
)

# Add a separate interface for database statistics
stats_iface = gr.Interface(
    fn=get_database_stats,
    inputs=None,
    outputs=gr.Textbox(label="Database Statistics", lines=10),
    title="TicketQueue Database Statistics",
    description="View basic statistics about the TicketQueue database"
)

# Combine interfaces
combined_iface = gr.TabbedInterface(
    [iface, stats_iface],
    ["NL to SQL Query", "Database Statistics"],
    title="TicketQueue Database Query System"
)

if __name__ == "__main__":
    combined_iface.launch()
