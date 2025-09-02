# Database Schema Analysis Guide

## Overview

This guide explains how to analyze any existing database and extract comprehensive schema information, relationships, and examples for building natural language to SQL conversion systems.

## Table of Contents

1. [Database Introspection Methods](#database-introspection-methods)
2. [Schema Extraction Techniques](#schema-extraction-techniques)
3. [Relationship Discovery](#relationship-discovery)
4. [Complex Relationship Examples](#complex-relationship-examples)
5. [Sample Data Analysis](#sample-data-analysis)
6. [Automated Schema Generation](#automated-schema-generation)
7. [Implementation Examples](#implementation-examples)

## Database Introspection Methods

### 1. SQLite Schema Analysis

```python
import sqlite3

def analyze_sqlite_schema(db_path):
    """Analyze SQLite database schema and relationships."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    
    schema_info = {}
    
    for table in tables:
        # Get column information
        cursor.execute(f"PRAGMA table_info({table})")
        columns = cursor.fetchall()
        
        # Get foreign key information
        cursor.execute(f"PRAGMA foreign_key_list({table})")
        foreign_keys = cursor.fetchall()
        
        # Get indexes
        cursor.execute(f"PRAGMA index_list({table})")
        indexes = cursor.fetchall()
        
        schema_info[table] = {
            'columns': columns,
            'foreign_keys': foreign_keys,
            'indexes': indexes
        }
    
    conn.close()
    return schema_info
```

### 2. PostgreSQL Schema Analysis

```python
import psycopg2

def analyze_postgresql_schema(connection_params):
    """Analyze PostgreSQL database schema."""
    conn = psycopg2.connect(**connection_params)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
    """)
    tables = [row[0] for row in cursor.fetchall()]
    
    schema_info = {}
    
    for table in tables:
        # Get column information
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_name = %s
            ORDER BY ordinal_position
        """, (table,))
        columns = cursor.fetchall()
        
        # Get foreign key information
        cursor.execute("""
            SELECT
                kcu.column_name,
                ccu.table_name AS foreign_table_name,
                ccu.column_name AS foreign_column_name
            FROM information_schema.table_constraints AS tc
            JOIN information_schema.key_column_usage AS kcu
                ON tc.constraint_name = kcu.constraint_name
            JOIN information_schema.constraint_column_usage AS ccu
                ON ccu.constraint_name = tc.constraint_name
            WHERE tc.constraint_type = 'FOREIGN KEY'
                AND tc.table_name = %s
        """, (table,))
        foreign_keys = cursor.fetchall()
        
        schema_info[table] = {
            'columns': columns,
            'foreign_keys': foreign_keys
        }
    
    conn.close()
    return schema_info
```

### 3. MySQL Schema Analysis

```python
import mysql.connector

def analyze_mysql_schema(connection_params):
    """Analyze MySQL database schema."""
    conn = mysql.connector.connect(**connection_params)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SHOW TABLES")
    tables = [row[0] for row in cursor.fetchall()]
    
    schema_info = {}
    
    for table in tables:
        # Get column information
        cursor.execute(f"DESCRIBE {table}")
        columns = cursor.fetchall()
        
        # Get foreign key information
        cursor.execute(f"""
            SELECT
                COLUMN_NAME,
                REFERENCED_TABLE_NAME,
                REFERENCED_COLUMN_NAME
            FROM information_schema.KEY_COLUMN_USAGE
            WHERE TABLE_NAME = '{table}'
                AND REFERENCED_TABLE_NAME IS NOT NULL
        """)
        foreign_keys = cursor.fetchall()
        
        schema_info[table] = {
            'columns': columns,
            'foreign_keys': foreign_keys
        }
    
    conn.close()
    return schema_info
```

## Schema Extraction Techniques

### 1. Comprehensive Schema Generator

```python
def generate_comprehensive_schema(db_connection, db_type='sqlite'):
    """Generate comprehensive schema information for any database."""
    
    if db_type == 'sqlite':
        schema_info = analyze_sqlite_schema(db_connection)
    elif db_type == 'postgresql':
        schema_info = analyze_postgresql_schema(db_connection)
    elif db_type == 'mysql':
        schema_info = analyze_mysql_schema(db_connection)
    else:
        raise ValueError(f"Unsupported database type: {db_type}")
    
    schema_text = "Database Schema:\n\n"
    
    # Generate table schemas
    for table_name, info in schema_info.items():
        schema_text += f"Table: {table_name}\n"
        schema_text += "Columns:\n"
        
        for column in info['columns']:
            if db_type == 'sqlite':
                col_name, col_type, not_null, default_val, pk = column
                pk_indicator = " [PRIMARY KEY]" if pk else ""
                schema_text += f"  - {col_name} ({col_type}){pk_indicator}\n"
            elif db_type == 'postgresql':
                col_name, col_type, is_nullable, default_val = column
                schema_text += f"  - {col_name} ({col_type})\n"
            elif db_type == 'mysql':
                col_name, col_type, null, key, default_val, extra = column
                pk_indicator = " [PRIMARY KEY]" if key == 'PRI' else ""
                schema_text += f"  - {col_name} ({col_type}){pk_indicator}\n"
        
        # Add foreign key information
        if info['foreign_keys']:
            schema_text += "Foreign Keys:\n"
            for fk in info['foreign_keys']:
                if db_type == 'sqlite':
                    id, seq, table, from_col, to_col, on_update, on_delete, match = fk
                    schema_text += f"  - {from_col} → {table}.{to_col}\n"
                elif db_type == 'postgresql':
                    col_name, foreign_table, foreign_column = fk
                    schema_text += f"  - {col_name} → {foreign_table}.{foreign_column}\n"
                elif db_type == 'mysql':
                    col_name, foreign_table, foreign_column = fk
                    schema_text += f"  - {col_name} → {foreign_table}.{foreign_column}\n"
        
        schema_text += "\n"
    
    return schema_text
```

### 2. Sample Data Extractor

```python
def extract_sample_data(db_connection, db_type='sqlite', sample_size=3):
    """Extract sample data from all tables."""
    
    if db_type == 'sqlite':
        conn = sqlite3.connect(db_connection)
    elif db_type == 'postgresql':
        conn = psycopg2.connect(**db_connection)
    elif db_type == 'mysql':
        conn = mysql.connector.connect(**db_connection)
    
    cursor = conn.cursor()
    
    # Get all table names
    if db_type == 'sqlite':
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    elif db_type == 'postgresql':
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    elif db_type == 'mysql':
        cursor.execute("SHOW TABLES")
    
    tables = [row[0] for row in cursor.fetchall()]
    
    sample_data = {}
    
    for table in tables:
        try:
            cursor.execute(f"SELECT * FROM {table} LIMIT {sample_size}")
            rows = cursor.fetchall()
            
            # Get column names
            if db_type == 'sqlite':
                cursor.execute(f"PRAGMA table_info({table})")
                columns = [row[1] for row in cursor.fetchall()]
            elif db_type == 'postgresql':
                cursor.execute("""
                    SELECT column_name FROM information_schema.columns
                    WHERE table_name = %s ORDER BY ordinal_position
                """, (table,))
                columns = [row[0] for row in cursor.fetchall()]
            elif db_type == 'mysql':
                cursor.execute(f"DESCRIBE {table}")
                columns = [row[0] for row in cursor.fetchall()]
            
            sample_data[table] = {
                'columns': columns,
                'rows': rows
            }
        except Exception as e:
            print(f"Error sampling table {table}: {e}")
    
    conn.close()
    return sample_data
```

## Relationship Discovery

### 1. Foreign Key Relationship Mapper

```python
def map_relationships(schema_info):
    """Map all relationships between tables."""
    
    relationships = {}
    
    for table_name, info in schema_info.items():
        relationships[table_name] = {
            'references': [],  # Tables this table references
            'referenced_by': []  # Tables that reference this table
        }
        
        # Find outgoing relationships (foreign keys)
        for fk in info['foreign_keys']:
            if len(fk) >= 3:
                if isinstance(fk, tuple) and len(fk) >= 3:
                    foreign_table = fk[2] if len(fk) > 2 else fk[1]
                    relationships[table_name]['references'].append(foreign_table)
        
        # Find incoming relationships
        for other_table, other_info in schema_info.items():
            if other_table != table_name:
                for fk in other_info['foreign_keys']:
                    if len(fk) >= 3:
                        if isinstance(fk, tuple) and len(fk) >= 3:
                            foreign_table = fk[2] if len(fk) > 2 else fk[1]
                            if foreign_table == table_name:
                                relationships[table_name]['referenced_by'].append(other_table)
    
    return relationships
```

### 2. Relationship Path Finder

```python
def find_relationship_paths(relationships, start_table, end_table, max_depth=3):
    """Find all possible relationship paths between two tables."""
    
    def find_paths(current_table, target_table, path, depth):
        if depth > max_depth:
            return []
        
        if current_table == target_table:
            return [path]
        
        paths = []
        
        # Follow outgoing relationships
        for ref_table in relationships[current_table]['references']:
            if ref_table not in path:  # Avoid cycles
                new_path = path + [ref_table]
                paths.extend(find_paths(ref_table, target_table, new_path, depth + 1))
        
        # Follow incoming relationships
        for ref_table in relationships[current_table]['referenced_by']:
            if ref_table not in path:  # Avoid cycles
                new_path = path + [ref_table]
                paths.extend(find_paths(ref_table, target_table, new_path, depth + 1))
        
        return paths
    
    return find_paths(start_table, end_table, [start_table], 0)
```

## Complex Relationship Examples

### 1. Hierarchical Relationship Detector

```python
def detect_hierarchical_relationships(schema_info):
    """Detect self-referencing (hierarchical) relationships."""
    
    hierarchical_tables = []
    
    for table_name, info in schema_info.items():
        for fk in info['foreign_keys']:
            if len(fk) >= 3:
                if isinstance(fk, tuple) and len(fk) >= 3:
                    foreign_table = fk[2] if len(fk) > 2 else fk[1]
                    if foreign_table == table_name:
                        hierarchical_tables.append({
                            'table': table_name,
                            'self_reference': fk
                        })
    
    return hierarchical_tables
```

### 2. Many-to-Many Relationship Detector

```python
def detect_many_to_many_relationships(schema_info):
    """Detect many-to-many relationships through junction tables."""
    
    many_to_many = []
    
    for table_name, info in schema_info.items():
        # Check if table has exactly 2 foreign keys (likely a junction table)
        if len(info['foreign_keys']) == 2:
            fk1, fk2 = info['foreign_keys']
            
            if len(fk1) >= 3 and len(fk2) >= 3:
                table1 = fk1[2] if len(fk1) > 2 else fk1[1]
                table2 = fk2[2] if len(fk2) > 2 else fk2[1]
                
                many_to_many.append({
                    'junction_table': table_name,
                    'table1': table1,
                    'table2': table2,
                    'relationship': f"{table1} ↔ {table2} (via {table_name})"
                })
    
    return many_to_many
```

### 3. Complex Join Path Generator

```python
def generate_complex_join_examples(relationships, schema_info):
    """Generate examples of complex join paths."""
    
    examples = []
    
    # Find tables with multiple relationships
    for table_name, rel_info in relationships.items():
        if len(rel_info['references']) > 1 or len(rel_info['referenced_by']) > 1:
            # Generate join examples
            if rel_info['references']:
                for ref_table in rel_info['references']:
                    examples.append({
                        'type': 'INNER JOIN',
                        'description': f"{table_name} → {ref_table}",
                        'sql_pattern': f"SELECT * FROM {table_name} INNER JOIN {ref_table} ON {table_name}.id = {ref_table}.{table_name}_id"
                    })
            
            if rel_info['referenced_by']:
                for ref_table in rel_info['referenced_by']:
                    examples.append({
                        'type': 'LEFT JOIN',
                        'description': f"{ref_table} → {table_name}",
                        'sql_pattern': f"SELECT * FROM {ref_table} LEFT JOIN {table_name} ON {ref_table}.{table_name}_id = {table_name}.id"
                    })
    
    return examples
```

## Sample Data Analysis

### 1. Data Type Inference

```python
def infer_data_types(sample_data):
    """Infer data types from sample data."""
    
    data_types = {}
    
    for table_name, data in sample_data.items():
        data_types[table_name] = {}
        
        for i, column in enumerate(data['columns']):
            column_types = []
            
            for row in data['rows']:
                if i < len(row):
                    value = row[i]
                    if value is None:
                        column_types.append('NULL')
                    elif isinstance(value, int):
                        column_types.append('INTEGER')
                    elif isinstance(value, float):
                        column_types.append('REAL')
                    elif isinstance(value, str):
                        if len(value) > 255:
                            column_types.append('TEXT')
                        else:
                            column_types.append('VARCHAR')
                    elif isinstance(value, bool):
                        column_types.append('BOOLEAN')
                    else:
                        column_types.append('UNKNOWN')
            
            # Determine most common type
            from collections import Counter
            type_counts = Counter(column_types)
            most_common_type = type_counts.most_common(1)[0][0]
            
            data_types[table_name][column] = most_common_type
    
    return data_types
```

### 2. Value Range Analysis

```python
def analyze_value_ranges(sample_data):
    """Analyze value ranges and patterns in sample data."""
    
    analysis = {}
    
    for table_name, data in sample_data.items():
        analysis[table_name] = {}
        
        for i, column in enumerate(data['columns']):
            values = [row[i] for row in data['rows'] if row[i] is not None]
            
            if values:
                if isinstance(values[0], (int, float)):
                    analysis[table_name][column] = {
                        'type': 'numeric',
                        'min': min(values),
                        'max': max(values),
                        'unique_count': len(set(values))
                    }
                elif isinstance(values[0], str):
                    analysis[table_name][column] = {
                        'type': 'text',
                        'min_length': min(len(v) for v in values),
                        'max_length': max(len(v) for v in values),
                        'unique_count': len(set(values)),
                        'sample_values': list(set(values))[:5]
                    }
    
    return analysis
```

## Automated Schema Generation

### 1. Complete Schema Generator

```python
def generate_complete_schema_analysis(db_connection, db_type='sqlite'):
    """Generate complete schema analysis for any database."""
    
    # Extract basic schema
    schema_info = generate_comprehensive_schema(db_connection, db_type)
    
    # Extract sample data
    sample_data = extract_sample_data(db_connection, db_type)
    
    # Map relationships
    relationships = map_relationships(schema_info)
    
    # Detect complex relationships
    hierarchical = detect_hierarchical_relationships(schema_info)
    many_to_many = detect_many_to_many_relationships(schema_info)
    
    # Generate join examples
    join_examples = generate_complex_join_examples(relationships, schema_info)
    
    # Analyze data
    data_types = infer_data_types(sample_data)
    value_analysis = analyze_value_ranges(sample_data)
    
    return {
        'schema_info': schema_info,
        'sample_data': sample_data,
        'relationships': relationships,
        'hierarchical_relationships': hierarchical,
        'many_to_many_relationships': many_to_many,
        'join_examples': join_examples,
        'data_types': data_types,
        'value_analysis': value_analysis
    }
```

### 2. Natural Language Schema Formatter

```python
def format_schema_for_nl_sql(analysis_result):
    """Format schema analysis for natural language to SQL systems."""
    
    schema_text = "Database Schema Analysis:\n\n"
    
    # Basic schema
    schema_text += "Tables and Columns:\n"
    for table_name, info in analysis_result['schema_info'].items():
        schema_text += f"\nTable: {table_name}\n"
        schema_text += "Columns:\n"
        for column in info['columns']:
            schema_text += f"  - {column[1]} ({column[2]})\n"
    
    # Relationships
    schema_text += "\n\nRelationships:\n"
    for table_name, rel_info in analysis_result['relationships'].items():
        if rel_info['references'] or rel_info['referenced_by']:
            schema_text += f"\n{table_name}:\n"
            if rel_info['references']:
                schema_text += f"  References: {', '.join(rel_info['references'])}\n"
            if rel_info['referenced_by']:
                schema_text += f"  Referenced by: {', '.join(rel_info['referenced_by'])}\n"
    
    # Complex relationships
    if analysis_result['hierarchical_relationships']:
        schema_text += "\n\nHierarchical Relationships:\n"
        for rel in analysis_result['hierarchical_relationships']:
            schema_text += f"- {rel['table']} (self-referencing)\n"
    
    if analysis_result['many_to_many_relationships']:
        schema_text += "\n\nMany-to-Many Relationships:\n"
        for rel in analysis_result['many_to_many_relationships']:
            schema_text += f"- {rel['relationship']}\n"
    
    # Sample data
    schema_text += "\n\nSample Data:\n"
    for table_name, data in analysis_result['sample_data'].items():
        schema_text += f"\n{table_name}:\n"
        for row in data['rows'][:2]:  # Show first 2 rows
            schema_text += f"  {row}\n"
    
    return schema_text
```

## Implementation Examples

### 1. Universal Database Analyzer

```python
class UniversalDatabaseAnalyzer:
    """Universal database analyzer for any database type."""
    
    def __init__(self, db_connection, db_type='sqlite'):
        self.db_connection = db_connection
        self.db_type = db_type
        self.analysis = None
    
    def analyze(self):
        """Perform complete database analysis."""
        self.analysis = generate_complete_schema_analysis(
            self.db_connection, 
            self.db_type
        )
        return self.analysis
    
    def get_schema_for_nl_sql(self):
        """Get schema formatted for natural language to SQL systems."""
        if not self.analysis:
            self.analyze()
        return format_schema_for_nl_sql(self.analysis)
    
    def get_relationship_examples(self):
        """Get relationship examples for the database."""
        if not self.analysis:
            self.analyze()
        
        examples = []
        
        # Add join examples
        examples.extend(self.analysis['join_examples'])
        
        # Add hierarchical examples
        for rel in self.analysis['hierarchical_relationships']:
            examples.append({
                'type': 'SELF JOIN',
                'description': f"{rel['table']} hierarchical relationship",
                'sql_pattern': f"SELECT * FROM {rel['table']} t1 JOIN {rel['table']} t2 ON t1.parent_id = t2.id"
            })
        
        # Add many-to-many examples
        for rel in self.analysis['many_to_many_relationships']:
            examples.append({
                'type': 'MANY-TO-MANY',
                'description': rel['relationship'],
                'sql_pattern': f"SELECT * FROM {rel['table1']} t1 JOIN {rel['junction_table']} j ON t1.id = j.{rel['table1']}_id JOIN {rel['table2']} t2 ON j.{rel['table2']}_id = t2.id"
            })
        
        return examples
```

### 2. Usage Example

```python
# Example usage for different database types

# SQLite
analyzer = UniversalDatabaseAnalyzer('path/to/database.db', 'sqlite')
schema = analyzer.get_schema_for_nl_sql()
examples = analyzer.get_relationship_examples()

# PostgreSQL
analyzer = UniversalDatabaseAnalyzer({
    'host': 'localhost',
    'database': 'mydb',
    'user': 'user',
    'password': 'password'
}, 'postgresql')
schema = analyzer.get_schema_for_nl_sql()

# MySQL
analyzer = UniversalDatabaseAnalyzer({
    'host': 'localhost',
    'database': 'mydb',
    'user': 'user',
    'password': 'password'
}, 'mysql')
schema = analyzer.get_schema_for_nl_sql()
```

## Best Practices

### 1. Schema Analysis Best Practices

- **Always sample data** to understand actual data types and patterns
- **Detect relationships** automatically rather than relying on manual documentation
- **Include sample data** in schema descriptions for better AI understanding
- **Document complex relationships** with clear examples
- **Handle edge cases** like self-referencing tables and many-to-many relationships

### 2. Natural Language Integration

- **Use descriptive table and column names** in schema descriptions
- **Include relationship context** in schema text
- **Provide join examples** for complex relationships
- **Document data patterns** and constraints
- **Include sample queries** that demonstrate common use cases

### 3. Performance Considerations

- **Limit sample data size** to avoid overwhelming the AI
- **Cache schema analysis** results for large databases
- **Use efficient queries** for schema introspection
- **Handle large databases** by analyzing subsets of tables

## Conclusion

This guide provides comprehensive methods for analyzing any database and extracting the information needed for natural language to SQL systems. The key is to:

1. **Automatically discover** table structures and relationships
2. **Extract sample data** to understand data patterns
3. **Map complex relationships** including hierarchical and many-to-many
4. **Format information** in a way that's useful for AI systems
5. **Provide examples** of common query patterns

By following these techniques, you can create natural language to SQL systems for any existing database without manual schema documentation.
