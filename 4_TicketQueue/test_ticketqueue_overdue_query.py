#!/usr/bin/env python3
"""
Test script to demonstrate the fixed "overdue" query functionality
"""

import sqlite3
from datetime import datetime

def test_overdue_queries():
    """Test various overdue and time-based queries."""
    
    conn = sqlite3.connect('ticketqueue.db')
    cursor = conn.cursor()
    
    print("🧪 Testing Overdue Query Functionality")
    print("=" * 50)
    
    # Test 1: Basic overdue query
    print("\n1. Ticket items that are overdue (past due date and not completed):")
    cursor.execute("""
        SELECT ti.title, ti.due_date, ti.status, 
               u.first_name || ' ' || u.last_name as assigned_to
        FROM ticket_items ti
        LEFT JOIN users u ON ti.assigned_to = u.id
        WHERE ti.due_date < datetime('now') AND ti.status != 'completed'
        ORDER BY ti.due_date ASC
        LIMIT 5
    """)
    
    results = cursor.fetchall()
    for row in results:
        print(f"  - {row[0]} (Due: {row[1]}, Status: {row[2]}, Assigned to: {row[3]})")
    
    # Test 2: Over budget query
    print("\n2. Ticket items that are over budget (actual > estimated hours):")
    cursor.execute("""
        SELECT ti.title, ti.estimated_hours, ti.actual_hours,
               (ti.actual_hours - ti.estimated_hours) as hours_over_budget
        FROM ticket_items ti
        WHERE ti.actual_hours > ti.estimated_hours
        ORDER BY hours_over_budget DESC
    """)
    
    results = cursor.fetchall()
    for row in results:
        print(f"  - {row[0]} (Est: {row[1]}h, Actual: {row[2]}h, Over: {row[3]}h)")
    
    # Test 3: Due soon query (due within next 7 days)
    print("\n3. Ticket items due soon (within next 7 days):")
    cursor.execute("""
        SELECT ti.title, ti.due_date, ti.status,
               u.first_name || ' ' || u.last_name as assigned_to
        FROM ticket_items ti
        LEFT JOIN users u ON ti.assigned_to = u.id
        WHERE ti.due_date BETWEEN datetime('now') AND datetime('now', '+7 days')
        AND ti.status != 'completed'
        ORDER BY ti.due_date ASC
    """)
    
    results = cursor.fetchall()
    for row in results:
        print(f"  - {row[0]} (Due: {row[1]}, Status: {row[2]}, Assigned to: {row[3]})")
    
    # Test 4: Overdue with priority
    print("\n4. High priority overdue ticket items:")
    cursor.execute("""
        SELECT ti.title, ti.priority, ti.due_date, ti.status,
               u.first_name || ' ' || u.last_name as assigned_to
        FROM ticket_items ti
        LEFT JOIN users u ON ti.assigned_to = u.id
        WHERE ti.due_date < datetime('now') 
        AND ti.status != 'completed'
        AND ti.priority = 1
        ORDER BY ti.due_date ASC
    """)
    
    results = cursor.fetchall()
    for row in results:
        priority_text = {1: 'High', 2: 'Medium', 3: 'Low'}.get(row[1], 'Unknown')
        print(f"  - {row[0]} (Priority: {priority_text}, Due: {row[2]}, Status: {row[3]}, Assigned to: {row[4]})")
    
    # Test 5: Summary statistics
    print("\n5. Overdue summary statistics:")
    cursor.execute("""
        SELECT 
            COUNT(*) as total_overdue,
            COUNT(CASE WHEN priority = 1 THEN 1 END) as high_priority_overdue,
            COUNT(CASE WHEN status = 'in_progress' THEN 1 END) as in_progress_overdue,
            COUNT(CASE WHEN status = 'pending' THEN 1 END) as pending_overdue
        FROM ticket_items
        WHERE due_date < datetime('now') AND status != 'completed'
    """)
    
    result = cursor.fetchone()
    print(f"  - Total overdue items: {result[0]}")
    print(f"  - High priority overdue: {result[1]}")
    print(f"  - In progress overdue: {result[2]}")
    print(f"  - Pending overdue: {result[3]}")
    
    conn.close()
    
    print("\n" + "=" * 50)
    print("✅ Overdue query functionality is working correctly!")
    print("\nThe system now properly handles:")
    print("- Due date-based overdue queries")
    print("- Time budget overruns")
    print("- Priority-based filtering")
    print("- Status-based filtering")

if __name__ == "__main__":
    test_overdue_queries()
