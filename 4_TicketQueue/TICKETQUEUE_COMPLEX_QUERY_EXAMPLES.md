# Complex Query Examples for TicketQueue NL to SQL System

This document showcases the enhanced Natural Language to SQL system with complex relationships, calculated fields, and advanced query patterns based on the ecommerce database approach.

## 🏗️ Enhanced Database Features

### Pre-Calculated Fields (Use These Instead of Complex Joins)

#### User Fields
- `users.total_assigned_items` - Total ticket items assigned to user
- `users.total_completed_items` - Total completed ticket items for user  
- `users.total_estimated_hours` - Total estimated hours for user's tasks
- `users.total_actual_hours` - Total actual hours spent by user

#### Ticket Queue Fields
- `ticket_queue.total_estimated_hours` - Total estimated hours for all ticket items in queue
- `ticket_queue.total_actual_hours` - Total actual hours for all ticket items in queue
- `ticket_queue.total_ticket_items` - Total number of ticket items in queue
- `ticket_queue.completed_ticket_items` - Number of completed ticket items in queue

### Complex Relationships

```
users → ticket_queue (assigned_to, created_by)
users → ticket_items (assigned_to)
ticket_queue → ticket_items (1:N)
ticket_items → ticket_item_comments (1:N)
ticket_items → ticket_item_attachments (1:N)
ticket_queue → ticket_queue_category_assignment (1:N)
ticket_queue_category_assignment → ticket_queue_categories (N:1)
ticket_items → ticket_item_dependencies (self-referencing)
```

## 🎯 Natural Language Query Examples

### Simple Queries (Using Pre-Calculated Fields)

#### User Ticket Load Queries
```sql
-- "Show users with their ticket load summary"
SELECT first_name, last_name, total_assigned_items, total_completed_items, 
       total_estimated_hours, total_actual_hours 
FROM users;

-- "Show users with their completion rate"
SELECT first_name, last_name, total_assigned_items, total_completed_items,
       CASE 
           WHEN total_assigned_items > 0 
           THEN ROUND((total_completed_items * 100.0 / total_assigned_items), 2)
           ELSE 0 
       END as completion_rate
FROM users;
```

#### Ticket Queue Progress Queries
```sql
-- "Show ticket queues with their progress"
SELECT title, total_ticket_items, completed_ticket_items, 
       total_estimated_hours, total_actual_hours
FROM ticket_queue;

-- "Show ticket queues with completion percentage"
SELECT title, total_ticket_items, completed_ticket_items,
       CASE 
           WHEN total_ticket_items > 0 
           THEN ROUND((completed_ticket_items * 100.0 / total_ticket_items), 2)
           ELSE 0 
       END as completion_percentage
FROM ticket_queue;
```

### Complex Relationship Queries

#### Multi-Table Joins
```sql
-- "Show users with their assigned ticket items and queue information"
SELECT u.first_name, u.last_name, wi.title as ticket_item, 
       wq.title as ticket_queue, wi.status, wi.estimated_hours
FROM users u
LEFT JOIN ticket_items wi ON u.id = wi.assigned_to
LEFT JOIN ticket_queue wq ON wi.ticket_queue_id = wq.id
ORDER BY u.first_name, wi.title;

-- "Show ticket queues with their categories and assigned users"
SELECT wq.title as ticket_queue, wqc.name as category, 
       u.first_name || ' ' || u.last_name as assigned_user
FROM ticket_queue wq
LEFT JOIN ticket_queue_category_assignment wqca ON wq.id = wqca.ticket_queue_id
LEFT JOIN ticket_queue_categories wqc ON wqca.category_id = wqc.id
LEFT JOIN users u ON wq.assigned_to = u.id
ORDER BY wq.title, wqc.name;
```

#### Self-Referencing Relationships (Dependencies)
```sql
-- "Show ticket items with their dependencies"
SELECT dep.title as dependent_item, pre.title as prerequisite_item,
       wq.title as ticket_queue
FROM ticket_item_dependencies wid
JOIN ticket_items dep ON wid.dependent_item_id = dep.id
JOIN ticket_items pre ON wid.prerequisite_item_id = pre.id
JOIN ticket_queue wq ON dep.ticket_queue_id = wq.id
ORDER BY wq.title, dep.title;

-- "Find ticket items that are blocking other tasks"
SELECT pre.title as blocking_item, COUNT(dep.id) as blocking_count,
       wq.title as ticket_queue
FROM ticket_item_dependencies wid
JOIN ticket_items pre ON wid.prerequisite_item_id = pre.id
JOIN ticket_items dep ON wid.dependent_item_id = dep.id
JOIN ticket_queue wq ON pre.ticket_queue_id = wq.id
WHERE pre.status != 'completed'
GROUP BY pre.id, pre.title, wq.title
ORDER BY blocking_count DESC;
```

#### Many-to-Many Relationships
```sql
-- "Show ticket queues with multiple categories"
SELECT wq.title as ticket_queue, 
       GROUP_CONCAT(wqc.name, ', ') as categories,
       COUNT(wqca.category_id) as category_count
FROM ticket_queue wq
JOIN ticket_queue_category_assignment wqca ON wq.id = wqca.ticket_queue_id
JOIN ticket_queue_categories wqc ON wqca.category_id = wqc.id
GROUP BY wq.id, wq.title
HAVING category_count > 1
ORDER BY category_count DESC;
```

### Advanced Aggregation Queries

#### User Performance Analysis
```sql
-- "Show users with their performance metrics"
SELECT u.first_name, u.last_name, u.role,
       u.total_assigned_items, u.total_completed_items,
       u.total_estimated_hours, u.total_actual_hours,
       CASE 
           WHEN u.total_estimated_hours > 0 
           THEN ROUND(((u.total_actual_hours / u.total_estimated_hours) * 100), 2)
           ELSE 0 
       END as efficiency_percentage
FROM users u
WHERE u.total_assigned_items > 0
ORDER BY efficiency_percentage DESC;

-- "Find users with the most completed tasks"
SELECT u.first_name, u.last_name, u.total_completed_items,
       u.total_estimated_hours, u.total_actual_hours
FROM users u
WHERE u.total_completed_items > 0
ORDER BY u.total_completed_items DESC;
```

#### Ticket Queue Analysis
```sql
-- "Show ticket queues by priority with their progress"
SELECT wq.title, 
       CASE wq.priority 
           WHEN 1 THEN 'High' 
           WHEN 2 THEN 'Medium' 
           WHEN 3 THEN 'Low' 
       END as priority_level,
       wq.total_ticket_items, wq.completed_ticket_items,
       wq.total_estimated_hours, wq.total_actual_hours
FROM ticket_queue wq
ORDER BY wq.priority, wq.completed_ticket_items DESC;

-- "Find ticket queues that are behind schedule"
SELECT wq.title, wq.total_estimated_hours, wq.total_actual_hours,
       (wq.total_actual_hours - wq.total_estimated_hours) as hours_over_budget
FROM ticket_queue wq
WHERE wq.total_actual_hours > wq.total_estimated_hours
ORDER BY hours_over_budget DESC;
```

### Complex Filtering and Conditional Queries

#### Time-Based Analysis
```sql
-- "Show ticket items with their estimated vs actual hours"
SELECT wi.title, wi.estimated_hours, wi.actual_hours,
       CASE 
           WHEN wi.actual_hours IS NULL THEN 'Not started'
           WHEN wi.actual_hours <= wi.estimated_hours THEN 'On track'
           ELSE 'Over budget'
       END as status
FROM ticket_items wi
WHERE wi.estimated_hours IS NOT NULL
ORDER BY wi.estimated_hours DESC;

-- "Find ticket items that are overdue"
SELECT wi.title, wi.due_date, wi.estimated_hours, wi.actual_hours,
       u.first_name || ' ' || u.last_name as assigned_to,
       wq.title as ticket_queue
FROM ticket_items wi
LEFT JOIN users u ON wi.assigned_to = u.id
LEFT JOIN ticket_queue wq ON wi.ticket_queue_id = wq.id
WHERE wi.due_date < datetime('now') AND wi.status != 'completed'
ORDER BY wi.due_date ASC;

-- "Find ticket items that are over budget (time-wise)"
SELECT wi.title, wi.estimated_hours, wi.actual_hours,
       (wi.actual_hours - wi.estimated_hours) as hours_over_budget,
       u.first_name || ' ' || u.last_name as assigned_to,
       wq.title as ticket_queue
FROM ticket_items wi
LEFT JOIN users u ON wi.assigned_to = u.id
LEFT JOIN ticket_queue wq ON wi.ticket_queue_id = wq.id
WHERE wi.actual_hours > wi.estimated_hours
ORDER BY (wi.actual_hours - wi.estimated_hours) DESC;
```

#### Role-Based Queries
```sql
-- "Show managers with their team ticket load"
SELECT u.first_name, u.last_name, u.role,
       u.total_assigned_items, u.total_completed_items
FROM users u
WHERE u.role = 'manager'
ORDER BY u.total_assigned_items DESC;

-- "Show workers with their task distribution by status"
SELECT u.first_name, u.last_name,
       COUNT(CASE WHEN wi.status = 'pending' THEN 1 END) as pending_tasks,
       COUNT(CASE WHEN wi.status = 'in_progress' THEN 1 END) as in_progress_tasks,
       COUNT(CASE WHEN wi.status = 'completed' THEN 1 END) as completed_tasks
FROM users u
LEFT JOIN ticket_items wi ON u.id = wi.assigned_to
WHERE u.role = 'worker'
GROUP BY u.id, u.first_name, u.last_name
ORDER BY u.first_name;
```

### Collaboration and Communication Queries

#### Comments and Attachments
```sql
-- "Show ticket items with comments and their authors"
SELECT wi.title as ticket_item, wic.comment, 
       u.first_name || ' ' || u.last_name as comment_author,
       wic.created_at
FROM ticket_items wi
JOIN ticket_item_comments wic ON wi.id = wic.ticket_item_id
JOIN users u ON wic.user_id = u.id
ORDER BY wic.created_at DESC;

-- "Show ticket items with attachments"
SELECT wi.title as ticket_item, wia.filename, wia.file_size,
       u.first_name || ' ' || u.last_name as uploaded_by,
       wia.uploaded_at
FROM ticket_items wi
JOIN ticket_item_attachments wia ON wi.id = wia.ticket_item_id
JOIN users u ON wia.uploaded_by = u.id
ORDER BY wia.uploaded_at DESC;
```

## 🚀 Natural Language Query Patterns

### User-Centric Queries
- "Show users with their total assigned ticket items and completion rate"
- "Find users with the most completed tasks"
- "Show users with their ticket load by ticket queue"
- "List users with their role and assigned ticket items by status"

### Ticket Queue-Centric Queries
- "Show ticket queues with their progress"
- "Find ticket queues with multiple categories and their assigned users"
- "Show ticket queues by priority with their total estimated hours"
- "Find ticket queues with high priority items that are behind schedule"

### Ticket Item-Centric Queries
- "List ticket items with their prerequisites and estimated completion time"
- "Show ticket items with their dependencies and current status"
- "Find ticket items that are blocking other tasks"
- "Show ticket items with their estimated vs actual hours"

### Collaboration Queries
- "Show ticket items with attachments and their uploaders"
- "Find users who have commented on ticket items they're assigned to"
- "List ticket items with comments and their assigned users"

### Performance Analysis Queries
- "Show users with their performance metrics"
- "Find ticket queues that are behind schedule"
- "Show ticket items that are overdue"
- "Calculate efficiency percentages for all users"

## 💡 Best Practices

1. **Use Pre-Calculated Fields**: Always check if data is available in calculated fields before using complex JOINs
2. **Optimize for Readability**: Use meaningful table aliases and clear column names
3. **Handle NULL Values**: Use COALESCE and CASE statements for proper NULL handling
4. **Group Related Data**: Use GROUP BY and aggregation functions for summary data
5. **Filter Early**: Apply WHERE clauses before JOINs when possible
6. **Consider Performance**: Use indexes and avoid unnecessary subqueries

## 🔧 Advanced Features

### Triggers for Data Consistency
The system includes triggers that automatically update calculated fields:
- `update_ticket_queue_totals_insert/update` - Updates ticket queue totals when ticket items change
- `update_user_totals_insert/update` - Updates user totals when ticket items change

### Indexes for Performance
- Primary key indexes on all tables
- Foreign key indexes for relationship queries
- Status and priority indexes for filtering

This enhanced system provides a powerful foundation for complex TicketQueue management queries with natural language interface!
