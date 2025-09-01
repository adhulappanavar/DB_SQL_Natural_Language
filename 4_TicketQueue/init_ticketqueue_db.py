#!/usr/bin/env python3
"""
TicketQueue SQLite Database Initialization Script
Creates and populates the database based on the TQ_ERD.png ER diagram
"""

import sqlite3
import os
from pathlib import Path

def init_ticketqueue_database(db_path='ticketqueue.db'):
    """Initialize the TicketQueue SQLite database with schema and sample data"""
    
    # Connect to database (creates it if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if database already has tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        existing_tables = cursor.fetchall()
        
        if not existing_tables or len(existing_tables) <= 1:  # Only sqlite_sequence or empty
            # Read and execute the schema file
            schema_file = Path(__file__).parent / 'ticketqueue_schema.sql'
            
            if schema_file.exists():
                with open(schema_file, 'r') as f:
                    schema_sql = f.read()
            
                # Execute the schema (split by semicolon for multiple statements)
                statements = schema_sql.split(';')
                for statement in statements:
                    statement = statement.strip()
                    if statement:
                        cursor.execute(statement)
                
                conn.commit()
                print(f"TicketQueue database initialized successfully: {db_path}")
                
                # Verify tables were created
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                print(f"Created tables: {[table[0] for table in tables]}")
                
                # Show sample data counts
                cursor.execute("SELECT COUNT(*) FROM users")
                user_count = cursor.fetchone()[0]
                cursor.execute("SELECT COUNT(*) FROM ticket_queue")
                ticket_queue_count = cursor.fetchone()[0]
                cursor.execute("SELECT COUNT(*) FROM ticket_items")
                ticket_item_count = cursor.fetchone()[0]
                cursor.execute("SELECT COUNT(*) FROM ticket_queue_categories")
                category_count = cursor.fetchone()[0]
                cursor.execute("SELECT COUNT(*) FROM ticket_item_comments")
                comment_count = cursor.fetchone()[0]
                cursor.execute("SELECT COUNT(*) FROM ticket_item_attachments")
                attachment_count = cursor.fetchone()[0]
                
                print(f"Sample data loaded:")
                print(f"  - Users: {user_count}")
                print(f"  - Ticket Queues: {ticket_queue_count}")
                print(f"  - Ticket Items: {ticket_item_count}")
                print(f"  - Categories: {category_count}")
                print(f"  - Comments: {comment_count}")
                print(f"  - Attachments: {attachment_count}")
                
            else:
                print(f"Schema file not found: {schema_file}")
                return False
            
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        conn.close()
    
    return True

def test_ticketqueue_database(db_path='ticketqueue.db'):
    """Test the TicketQueue database with comprehensive sample queries"""
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        print("\n--- TicketQueue Database Test Queries ---")
        
        # Test 1: Get ticket queues with their status and assigned users
        cursor.execute("""
            SELECT tq.title, tq.status, tq.priority, 
                u.first_name || ' ' || u.last_name as assigned_to,
                tq.due_date
            FROM ticket_queue tq
            LEFT JOIN users u ON tq.assigned_to = u.id
            ORDER BY tq.priority, tq.due_date
        """)
        
        print("Ticket Queues by Priority:")
        for row in cursor.fetchall():
            priority_text = {1: 'High', 2: 'Medium', 3: 'Low'}.get(row[2], 'Unknown')
            print(f"  - {row[0]} ({priority_text} Priority) - {row[1]} - Assigned to: {row[3] or 'Unassigned'}")
        
        # Test 2: Get ticket items by status with progress
        cursor.execute("""
            SELECT ti.title, ti.status, ti.estimated_hours, ti.actual_hours,
                    u.first_name || ' ' || u.last_name as assigned_to,
                    tq.title as ticket_queue
            FROM ticket_items ti
            JOIN ticket_queue tq ON ti.ticket_queue_id = tq.id
            LEFT JOIN users u ON ti.assigned_to = u.id
            ORDER BY ti.status, ti.priority
        """)
        
        print("\nTicket Items by Status:")
        current_status = None
        for row in cursor.fetchall():
            if row[1] != current_status:
                current_status = row[1]
                print(f"\n{current_status.upper()}:")
            
            progress = ""
            if row[2] and row[3]:
                progress = f" ({row[3]}/{row[2]} hours)"
            elif row[2]:
                progress = f" (0/{row[2]} hours)"
            
            print(f"  - {row[0]} - {row[4] or 'Unassigned'}{progress} - Queue: {row[5]}")
        
        # Test 3: Get users with their ticket load
        cursor.execute("""
            SELECT u.first_name || ' ' || u.last_name as full_name, u.role,
                COUNT(ti.id) as assigned_items,
                SUM(CASE WHEN ti.status = 'completed' THEN 1 ELSE 0 END) as completed_items,
                SUM(ti.estimated_hours) as total_estimated_hours,
                SUM(ti.actual_hours) as total_actual_hours
            FROM users u
            LEFT JOIN ticket_items ti ON u.id = ti.assigned_to
            GROUP BY u.id
            ORDER BY assigned_items DESC
        """)
        
        print("\nUser Ticket Load Summary:")
        for row in cursor.fetchall():
            print(f"  - {row[0]} ({row[1]}) - {row[2]} assigned items, {row[3]} completed")
        
        # Test 4: Get ticket item dependencies
        cursor.execute("""
            SELECT 
                dep.title as dependent_item,
                pre.title as prerequisite_item,
                tq.title as ticket_queue
            FROM ticket_item_dependencies wid
            JOIN ticket_items dep ON wid.dependent_item_id = dep.id
            JOIN ticket_items pre ON wid.prerequisite_item_id = pre.id
            JOIN ticket_queue tq ON dep.ticket_queue_id = tq.id
            ORDER BY tq.title, dep.title
        """)
        
        print("\nTicket Item Dependencies:")
        current_queue = None
        for row in cursor.fetchall():
            if row[2] != current_queue:
                current_queue = row[2]
                print(f"\n{current_queue}:")
            print(f"  - {row[0]} depends on {row[1]}")
        
        # Test 5: Get category assignments
        cursor.execute("""
            SELECT tqc.name as category, tq.title as ticket_queue, tqc.color
            FROM ticket_queue_category_assignment tqca
            JOIN ticket_queue_categories tqc ON tqca.category_id = tqc.id
            JOIN ticket_queue tq ON tqca.ticket_queue_id = tq.id
            ORDER BY tqc.name, tq.title
        """)
        
        print("\nTicket Queue Categories:")
        current_category = None
        for row in cursor.fetchall():
            if row[0] != current_category:
                current_category = row[0]
                print(f"\n{current_category}:")
            print(f"  - {row[1]}")
        
        # Test 6: Check foreign key constraints
        cursor.execute("PRAGMA foreign_key_check")
        fk_issues = cursor.fetchall()
        
        if not fk_issues:
            print("\n✓ Foreign key constraints are valid")
        else:
            print(f"\n⚠ Foreign key issues found: {fk_issues}")
            
    except sqlite3.Error as e:
        print(f"Database error during testing: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    print("Initializing TicketQueue SQLite database based on TQ_ERD.png...")
    
    if init_ticketqueue_database():
        test_ticketqueue_database()
        print("\nTicketQueue database setup complete!")
    else:
        print("TicketQueue database setup failed!")
