# TicketQueue SQLite Database Setup

This project contains a SQLite database schema for a TicketQueue system based on the WQ_ERD.png ER diagram.

## Files

- `ticketqueue_schema.sql` - Complete database schema with tables, relationships, and comprehensive sample data
- `init_ticketqueue_db.py` - Python script to initialize the database
- `ticketqueue.db` - SQLite database file (created after running the init script)
- `WQ_ERD.png` - ER diagram reference

## Database Schema

The TicketQueue database includes the following tables:

### Core Tables
- **users** - User accounts with roles (admin, manager, worker)
- **ticket_queue** - Main ticket queue entries with priorities and status
- **ticket_items** - Individual ticket items within queues
- **ticket_queue_categories** - Categories for organizing ticket queues

### Supporting Tables
- **ticket_item_comments** - Comments on ticket items
- **ticket_item_attachments** - File attachments for ticket items
- **ticket_queue_category_assignment** - Many-to-many relationship between queues and categories
- **ticket_item_dependencies** - Dependencies between ticket items

### Key Features
- **Role-based access** (admin, manager, worker)
- **Priority levels** (1=high, 2=medium, 3=low)
- **Status tracking** (pending, in_progress, completed, cancelled/failed)
- **Time tracking** (estimated vs actual hours)
- **File attachments** support
- **Ticket item dependencies** for project management
- **Category organization** with color coding
- **Foreign key constraints** for data integrity
- **Indexes** for performance optimization

## Database Relationships

```
users (1) ←→ (N) ticket_queue (created_by)
users (1) ←→ (N) ticket_queue (assigned_to)
users (1) ←→ (N) ticket_items (assigned_to)
users (1) ←→ (N) ticket_item_comments
users (1) ←→ (N) ticket_item_attachments

ticket_queue (1) ←→ (N) ticket_items
ticket_queue (N) ←→ (N) ticket_queue_categories (via assignment table)

ticket_items (1) ←→ (N) ticket_item_comments
ticket_items (1) ←→ (N) ticket_item_attachments
ticket_items (N) ←→ (N) ticket_items (via dependencies table)
```

## Setup Instructions

### Option 1: Using Python Script (Recommended)

```bash
# Run the initialization script
python init_ticketqueue_db.py
```

This will:
- Create a new `ticketqueue.db` file
- Execute the complete schema
- Load comprehensive sample data
- Run test queries to verify setup

### Option 2: Manual SQLite Commands

```bash
# Create database and run schema
sqlite3 ticketqueue.db < ticketqueue_schema.sql
```

### Option 3: Interactive SQLite

```bash
# Start SQLite shell
sqlite3 ticketqueue.db

# Run schema commands
.read ticketqueue_schema.sql

# Verify tables
.tables

# Exit
.quit
```

## Sample Data Included

The database comes with comprehensive sample data:

- **6 Users** with different roles (admin, manager, workers)
- **6 Ticket Queues** with various priorities and statuses
- **21 Ticket Items** with time tracking and dependencies
- **6 Categories** for organizing work (Bug Fixes, Feature Development, etc.)
- **12 Comments** on ticket items
- **7 File Attachments** with metadata
- **6 Category Assignments** linking queues to categories
- **16 Ticket Item Dependencies** showing task relationships

## Sample Queries

Once the database is set up, you can run these sample queries:

```sql
-- Get ticket queues with assigned users and priorities
SELECT wq.title, wq.status, wq.priority, 
       u.first_name || ' ' || u.last_name as assigned_to
FROM ticket_queue wq
LEFT JOIN users u ON wq.assigned_to = u.id
ORDER BY wq.priority, wq.due_date;

-- Get ticket items with progress tracking
SELECT wi.title, wi.status, wi.estimated_hours, wi.actual_hours,
       u.first_name || ' ' || u.last_name as assigned_to
FROM ticket_items wi
LEFT JOIN users u ON wi.assigned_to = u.id
ORDER BY wi.status, wi.priority;

-- Get user ticket load summary
SELECT u.first_name || ' ' || u.last_name as full_name, u.role,
       COUNT(wi.id) as assigned_items,
       SUM(CASE WHEN wi.status = 'completed' THEN 1 ELSE 0 END) as completed_items
FROM users u
LEFT JOIN ticket_items wi ON u.id = wi.assigned_to
GROUP BY u.id
ORDER BY assigned_items DESC;

-- Get ticket item dependencies
SELECT 
    dep.title as dependent_item,
    pre.title as prerequisite_item,
    wq.title as ticket_queue
FROM ticket_item_dependencies wid
JOIN ticket_items dep ON wid.dependent_item_id = dep.id
JOIN ticket_items pre ON wid.prerequisite_item_id = pre.id
JOIN ticket_queue wq ON dep.ticket_queue_id = wq.id
ORDER BY wq.title, dep.title;

-- Get ticket queues by category
SELECT wqc.name as category, wq.title as ticket_queue
FROM ticket_queue_category_assignment wqca
JOIN ticket_queue_categories wqc ON wqca.category_id = wqc.id
JOIN ticket_queue wq ON wqca.ticket_queue_id = wq.id
ORDER BY wqc.name, wq.title;
```

## TicketQueue Features

### Priority System
- **High Priority (1)**: Urgent tasks requiring immediate attention
- **Medium Priority (2)**: Important tasks with normal timeline
- **Low Priority (3)**: Routine tasks with flexible timeline

### Status Tracking
- **pending**: Task not yet started
- **in_progress**: Task currently being worked on
- **completed**: Task finished successfully
- **cancelled**: Task cancelled or abandoned
- **failed**: Task failed to complete

### Time Tracking
- **estimated_hours**: Planned time for the task
- **actual_hours**: Actual time spent on the task
- **started_at**: When work began
- **completed_at**: When work finished

### Dependencies
- Ticket items can have prerequisites
- Dependencies prevent circular references
- Tasks can only start when prerequisites are completed

## Notes

- Foreign key constraints are enabled by default
- All tables include timestamps for audit trails
- Comprehensive sample data is included for testing
- Indexes are created for common query patterns
- The database uses SQLite's built-in data types and constraints
- Based on the WQ_ERD.png ER diagram structure
- Supports file attachments with metadata tracking
- Includes role-based access control
