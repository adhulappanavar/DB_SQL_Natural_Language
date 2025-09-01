# Complex Join Examples for TicketQueue NL to SQL System

This document showcases the complex join patterns that the enhanced Natural Language to SQL system can handle with the new examples.

## 🏗️ Complex Join Patterns

### 1. Multi-Table Joins with Dependencies

#### "Show ticket items with their dependencies, assigned users, and ticket queue information"
```sql
SELECT 
    dep.title as dependent_item, 
    pre.title as prerequisite,
    u.first_name || ' ' || u.last_name as assigned_user, 
    wq.title as ticket_queue
FROM ticket_item_dependencies wid
JOIN ticket_items dep ON wid.dependent_item_id = dep.id
JOIN ticket_items pre ON wid.prerequisite_item_id = pre.id
LEFT JOIN users u ON dep.assigned_to = u.id
LEFT JOIN ticket_queue wq ON dep.ticket_queue_id = wq.id
ORDER BY wq.title, dep.title;
```

**Join Pattern:** Self-referencing + User + Ticket Queue (4 tables)

### 2. Conditional Joins with Filtering

#### "Find users who have both assigned ticket items and have made comments on other ticket items"
```sql
SELECT DISTINCT
    u.first_name || ' ' || u.last_name as user_name,
    COUNT(DISTINCT wi.id) as assigned_items,
    COUNT(DISTINCT wic.id) as comments_made
FROM users u
LEFT JOIN ticket_items wi ON u.id = wi.assigned_to
LEFT JOIN ticket_item_comments wic ON u.id = wic.user_id
WHERE wi.id IS NOT NULL AND wic.id IS NOT NULL
GROUP BY u.id, u.first_name, u.last_name
HAVING assigned_items > 0 AND comments_made > 0;
```

**Join Pattern:** User + Ticket Items + Comments with conditional filtering

### 3. Many-to-Many with Aggregation

#### "Show ticket queues with their categories, assigned users, and total ticket items count"
```sql
SELECT 
    wq.title as ticket_queue,
    GROUP_CONCAT(DISTINCT wqc.name, ', ') as categories,
    u.first_name || ' ' || u.last_name as assigned_user,
    COUNT(wi.id) as total_ticket_items,
    COUNT(CASE WHEN wi.status = 'completed' THEN 1 END) as completed_items
FROM ticket_queue wq
LEFT JOIN ticket_queue_category_assignment wqca ON wq.id = wqca.ticket_queue_id
LEFT JOIN ticket_queue_categories wqc ON wqca.category_id = wqc.id
LEFT JOIN users u ON wq.assigned_to = u.id
LEFT JOIN ticket_items wi ON wq.id = wi.ticket_queue_id
GROUP BY wq.id, wq.title, u.first_name, u.last_name
ORDER BY total_ticket_items DESC;
```

**Join Pattern:** Ticket Queue + Categories (many-to-many) + Users + Ticket Items (5 tables)

### 4. Self-Referencing with Aggregation

#### "List ticket items with their dependencies, comments count, and attachment count"
```sql
SELECT 
    wi.title as ticket_item,
    COUNT(DISTINCT wid.dependent_item_id) as dependencies_count,
    COUNT(DISTINCT wic.id) as comments_count,
    COUNT(DISTINCT wia.id) as attachments_count,
    u.first_name || ' ' || u.last_name as assigned_user
FROM ticket_items wi
LEFT JOIN ticket_item_dependencies wid ON wi.id = wid.dependent_item_id
LEFT JOIN ticket_item_comments wic ON wi.id = wic.ticket_item_id
LEFT JOIN ticket_item_attachments wia ON wi.id = wia.ticket_item_id
LEFT JOIN users u ON wi.assigned_to = u.id
GROUP BY wi.id, wi.title, u.first_name, u.last_name
ORDER BY dependencies_count DESC, comments_count DESC;
```

**Join Pattern:** Ticket Items + Dependencies (self-referencing) + Comments + Attachments + Users (5 tables)

### 5. Complex Filtering with Multiple Conditions

#### "Find ticket items that are overdue with their assigned users, ticket queue, and priority level"
```sql
SELECT 
    wi.title as ticket_item,
    wi.due_date,
    wi.priority,
    CASE wi.priority 
        WHEN 1 THEN 'High' 
        WHEN 2 THEN 'Medium' 
        WHEN 3 THEN 'Low' 
    END as priority_level,
    u.first_name || ' ' || u.last_name as assigned_user,
    wq.title as ticket_queue,
    wi.estimated_hours,
    wi.actual_hours
FROM ticket_items wi
LEFT JOIN users u ON wi.assigned_to = u.id
LEFT JOIN ticket_queue wq ON wi.ticket_queue_id = wq.id
WHERE wi.due_date < datetime('now') 
AND wi.status != 'completed'
ORDER BY wi.priority, wi.due_date ASC;
```

**Join Pattern:** Ticket Items + Users + Ticket Queue with complex WHERE conditions

### 6. Cross-Table Analysis

#### "Show users with their assigned ticket items, ticket queue information, and completion status"
```sql
SELECT 
    u.first_name || ' ' || u.last_name as user_name,
    u.role,
    wi.title as ticket_item,
    wq.title as ticket_queue,
    wi.status,
    wi.estimated_hours,
    wi.actual_hours,
    CASE 
        WHEN wi.status = 'completed' THEN 'Completed'
        WHEN wi.actual_hours IS NULL THEN 'Not Started'
        WHEN wi.actual_hours <= wi.estimated_hours THEN 'On Track'
        ELSE 'Over Budget'
    END as completion_status
FROM users u
LEFT JOIN ticket_items wi ON u.id = wi.assigned_to
LEFT JOIN ticket_queue wq ON wi.ticket_queue_id = wq.id
WHERE wi.id IS NOT NULL
ORDER BY u.first_name, wi.status, wi.title;
```

**Join Pattern:** Users + Ticket Items + Ticket Queue with conditional logic

### 7. Hierarchical Data with Multiple Joins

#### "List ticket items with their prerequisites, assigned users, and estimated vs actual hours"
```sql
SELECT 
    dep.title as dependent_item,
    pre.title as prerequisite_item,
    u.first_name || ' ' || u.last_name as assigned_user,
    dep.estimated_hours as dep_estimated,
    dep.actual_hours as dep_actual,
    pre.estimated_hours as pre_estimated,
    pre.actual_hours as pre_actual,
    CASE 
        WHEN dep.actual_hours IS NULL THEN 'Not Started'
        WHEN dep.actual_hours <= dep.estimated_hours THEN 'On Track'
        ELSE 'Over Budget'
    END as dependent_status,
    CASE 
        WHEN pre.actual_hours IS NULL THEN 'Not Started'
        WHEN pre.actual_hours <= pre.estimated_hours THEN 'On Track'
        ELSE 'Over Budget'
    END as prerequisite_status
FROM ticket_item_dependencies wid
JOIN ticket_items dep ON wid.dependent_item_id = dep.id
JOIN ticket_items pre ON wid.prerequisite_item_id = pre.id
LEFT JOIN users u ON dep.assigned_to = u.id
ORDER BY dep.title, pre.title;
```

**Join Pattern:** Dependencies (self-referencing) + Users with complex CASE statements

### 8. Many-to-Many with Status Analysis

#### "Find ticket queues with multiple categories, assigned users, and ticket items by status"
```sql
SELECT 
    wq.title as ticket_queue,
    GROUP_CONCAT(DISTINCT wqc.name, ', ') as categories,
    u.first_name || ' ' || u.last_name as assigned_user,
    COUNT(CASE WHEN wi.status = 'pending' THEN 1 END) as pending_count,
    COUNT(CASE WHEN wi.status = 'in_progress' THEN 1 END) as in_progress_count,
    COUNT(CASE WHEN wi.status = 'completed' THEN 1 END) as completed_count,
    COUNT(CASE WHEN wi.status = 'failed' THEN 1 END) as failed_count
FROM ticket_queue wq
LEFT JOIN ticket_queue_category_assignment wqca ON wq.id = wqca.ticket_queue_id
LEFT JOIN ticket_queue_categories wqc ON wqca.category_id = wqc.id
LEFT JOIN users u ON wq.assigned_to = u.id
LEFT JOIN ticket_items wi ON wq.id = wi.ticket_queue_id
GROUP BY wq.id, wq.title, u.first_name, u.last_name
HAVING COUNT(DISTINCT wqc.id) > 1
ORDER BY completed_count DESC;
```

**Join Pattern:** Ticket Queue + Categories (many-to-many) + Users + Ticket Items with GROUP BY and HAVING

### 9. Cross-Reference Analysis

#### "Show ticket items with their dependencies, comments from assigned users, and attachments"
```sql
SELECT 
    wi.title as ticket_item,
    COUNT(DISTINCT wid.dependent_item_id) as dependencies_count,
    COUNT(DISTINCT wic.id) as comments_from_assigned,
    COUNT(DISTINCT wia.id) as attachments_count,
    u.first_name || ' ' || u.last_name as assigned_user
FROM ticket_items wi
LEFT JOIN ticket_item_dependencies wid ON wi.id = wid.dependent_item_id
LEFT JOIN ticket_item_comments wic ON wi.id = wic.ticket_item_id AND wic.user_id = wi.assigned_to
LEFT JOIN ticket_item_attachments wia ON wi.id = wia.ticket_item_id
LEFT JOIN users u ON wi.assigned_to = u.id
GROUP BY wi.id, wi.title, u.first_name, u.last_name
ORDER BY dependencies_count DESC, comments_from_assigned DESC;
```

**Join Pattern:** Ticket Items + Dependencies + Comments (with condition) + Attachments + Users

### 10. Role-Based Complex Analysis

#### "List users with their role, assigned ticket items, and ticket queues they're managing"
```sql
SELECT 
    u.first_name || ' ' || u.last_name as user_name,
    u.role,
    COUNT(DISTINCT wi.id) as assigned_ticket_items,
    COUNT(DISTINCT wq.id) as managed_ticket_queues,
    GROUP_CONCAT(DISTINCT wi.title, '; ') as ticket_item_titles,
    GROUP_CONCAT(DISTINCT wq.title, '; ') as managed_queues
FROM users u
LEFT JOIN ticket_items wi ON u.id = wi.assigned_to
LEFT JOIN ticket_queue wq ON u.id = wq.assigned_to
GROUP BY u.id, u.first_name, u.last_name, u.role
ORDER BY u.role, assigned_ticket_items DESC;
```

**Join Pattern:** Users + Ticket Items + Ticket Queue with role-based grouping

## 🎯 Advanced Join Techniques

### Conditional Joins
```sql
-- Join only when condition is met
LEFT JOIN ticket_item_comments wic ON wi.id = wic.ticket_item_id AND wic.user_id = wi.assigned_to
```

### Self-Referencing Joins
```sql
-- Ticket item dependencies
JOIN ticket_items dep ON wid.dependent_item_id = dep.id
JOIN ticket_items pre ON wid.prerequisite_item_id = pre.id
```

### Many-to-Many Joins
```sql
-- Ticket queue categories
JOIN ticket_queue_category_assignment wqca ON wq.id = wqca.ticket_queue_id
JOIN ticket_queue_categories wqc ON wqca.category_id = wqc.id
```

### Aggregation with Multiple Tables
```sql
-- Count across multiple related tables
COUNT(DISTINCT wid.dependent_item_id) as dependencies_count,
COUNT(DISTINCT wic.id) as comments_count,
COUNT(DISTINCT wia.id) as attachments_count
```

## 💡 Best Practices for Complex Joins

1. **Use meaningful aliases** for better readability
2. **LEFT JOIN** when you want all records from the main table
3. **INNER JOIN** when you only want matching records
4. **GROUP BY** with aggregation functions for summary data
5. **HAVING** for filtering aggregated results
6. **CASE statements** for conditional logic in SELECT
7. **ORDER BY** for meaningful result ordering
8. **DISTINCT** to avoid duplicate rows in complex joins

## 🚀 Performance Considerations

- Use indexes on foreign key columns
- Limit result sets with WHERE clauses early
- Use appropriate JOIN types (LEFT vs INNER)
- Consider query complexity for large datasets
- Use GROUP BY efficiently with proper columns

These complex join patterns demonstrate the system's ability to handle sophisticated queries across multiple related tables with various relationship types!
