#!/usr/bin/env python3
"""
Database Schema Analyzer
Analyzes any SQLite database and generates comprehensive schema information
for natural language to SQL conversion systems.
"""

import sqlite3
import os
from datetime import datetime
from collections import defaultdict

class DatabaseSchemaAnalyzer:
    """Analyzes database schema and generates markdown documentation."""
    
    def __init__(self, db_path):
        """Initialize with database path."""
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.schema_info = {}
        self.relationships = {}
        self.sample_data = {}
        
    def connect(self):
        """Connect to the database."""
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Database file not found: {self.db_path}")
        
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        print(f"✅ Connected to database: {self.db_path}")
        
    def disconnect(self):
        """Disconnect from the database."""
        if self.conn:
            self.conn.close()
            print("✅ Disconnected from database")
    
    def get_table_names(self):
        """Get all table names from the database."""
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        return [row[0] for row in self.cursor.fetchall()]
    
    def analyze_table_schema(self, table_name):
        """Analyze schema for a specific table."""
        # Get column information
        self.cursor.execute(f"PRAGMA table_info({table_name})")
        columns = self.cursor.fetchall()
        
        # Get foreign key information
        self.cursor.execute(f"PRAGMA foreign_key_list({table_name})")
        foreign_keys = self.cursor.fetchall()
        
        # Get indexes
        self.cursor.execute(f"PRAGMA index_list({table_name})")
        indexes = self.cursor.fetchall()
        
        return {
            'columns': columns,
            'foreign_keys': foreign_keys,
            'indexes': indexes
        }
    
    def extract_sample_data(self, table_name, sample_size=3):
        """Extract sample data from a table."""
        try:
            self.cursor.execute(f"SELECT * FROM {table_name} LIMIT {sample_size}")
            rows = self.cursor.fetchall()
            
            # Get column names
            self.cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [row[1] for row in self.cursor.fetchall()]
            
            return {
                'columns': columns,
                'rows': rows
            }
        except Exception as e:
            print(f"⚠️  Error sampling table {table_name}: {e}")
            return None
    
    def map_relationships(self):
        """Map all relationships between tables."""
        relationships = {}
        
        for table_name, info in self.schema_info.items():
            relationships[table_name] = {
                'references': [],  # Tables this table references
                'referenced_by': []  # Tables that reference this table
            }
            
            # Find outgoing relationships (foreign keys)
            for fk in info['foreign_keys']:
                if len(fk) >= 3:
                    foreign_table = fk[2]  # Referenced table
                    relationships[table_name]['references'].append(foreign_table)
            
            # Find incoming relationships
            for other_table, other_info in self.schema_info.items():
                if other_table != table_name:
                    for fk in other_info['foreign_keys']:
                        if len(fk) >= 3:
                            foreign_table = fk[2]  # Referenced table
                            if foreign_table == table_name:
                                relationships[table_name]['referenced_by'].append(other_table)
        
        return relationships
    
    def detect_hierarchical_relationships(self):
        """Detect self-referencing (hierarchical) relationships."""
        hierarchical_tables = []
        
        for table_name, info in self.schema_info.items():
            for fk in info['foreign_keys']:
                if len(fk) >= 3:
                    foreign_table = fk[2]  # Referenced table
                    if foreign_table == table_name:
                        hierarchical_tables.append({
                            'table': table_name,
                            'self_reference': fk
                        })
        
        return hierarchical_tables
    
    def detect_many_to_many_relationships(self):
        """Detect many-to-many relationships through junction tables."""
        many_to_many = []
        
        for table_name, info in self.schema_info.items():
            # Check if table has exactly 2 foreign keys (likely a junction table)
            if len(info['foreign_keys']) == 2:
                fk1, fk2 = info['foreign_keys']
                
                if len(fk1) >= 3 and len(fk2) >= 3:
                    table1 = fk1[2]  # First referenced table
                    table2 = fk2[2]  # Second referenced table
                    
                    many_to_many.append({
                        'junction_table': table_name,
                        'table1': table1,
                        'table2': table2,
                        'relationship': f"{table1} ↔ {table2} (via {table_name})"
                    })
        
        return many_to_many
    
    def generate_join_examples(self):
        """Generate examples of complex join paths."""
        examples = []
        
        # Find tables with multiple relationships
        for table_name, rel_info in self.relationships.items():
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
    
    def analyze_database(self):
        """Perform complete database analysis."""
        print("🔍 Analyzing database schema...")
        
        # Get all tables
        tables = self.get_table_names()
        print(f"📋 Found {len(tables)} tables: {', '.join(tables)}")
        
        # Analyze each table
        for table in tables:
            print(f"  📊 Analyzing table: {table}")
            self.schema_info[table] = self.analyze_table_schema(table)
            self.sample_data[table] = self.extract_sample_data(table)
        
        # Map relationships
        print("🔗 Mapping relationships...")
        self.relationships = self.map_relationships()
        
        # Detect complex relationships
        self.hierarchical_relationships = self.detect_hierarchical_relationships()
        self.many_to_many_relationships = self.detect_many_to_many_relationships()
        self.join_examples = self.generate_join_examples()
        
        print("✅ Database analysis complete!")
    
    def generate_markdown_schema(self):
        """Generate comprehensive markdown schema documentation."""
        
        markdown = f"""# Database Schema Analysis

**Database**: `{os.path.basename(self.db_path)}`  
**Analysis Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Total Tables**: {len(self.schema_info)}

## Database Overview

This database contains {len(self.schema_info)} tables with complex relationships and comprehensive data structures.

## Table Schemas

"""
        
        # Generate table schemas
        for table_name, info in self.schema_info.items():
            markdown += f"### {table_name}\n\n"
            markdown += "**Columns:**\n"
            
            for column in info['columns']:
                col_id, col_name, col_type, not_null, default_val, pk = column
                pk_indicator = " 🔑" if pk else ""
                not_null_indicator = " NOT NULL" if not_null else ""
                default_indicator = f" DEFAULT {default_val}" if default_val else ""
                
                markdown += f"- `{col_name}` ({col_type}){pk_indicator}{not_null_indicator}{default_indicator}\n"
            
            # Add foreign key information
            if info['foreign_keys']:
                markdown += "\n**Foreign Keys:**\n"
                for fk in info['foreign_keys']:
                    id, seq, table, from_col, to_col, on_update, on_delete, match = fk
                    markdown += f"- `{from_col}` → `{table}.{to_col}`\n"
            
            # Add sample data
            if self.sample_data[table_name]:
                markdown += "\n**Sample Data:**\n"
                markdown += "```\n"
                for row in self.sample_data[table_name]['rows']:
                    markdown += f"{row}\n"
                markdown += "```\n"
            
            markdown += "\n"
        
        # Add relationships section
        markdown += "## Relationships\n\n"
        
        for table_name, rel_info in self.relationships.items():
            if rel_info['references'] or rel_info['referenced_by']:
                markdown += f"### {table_name}\n"
                if rel_info['references']:
                    markdown += f"- **References**: {', '.join(rel_info['references'])}\n"
                if rel_info['referenced_by']:
                    markdown += f"- **Referenced by**: {', '.join(rel_info['referenced_by'])}\n"
                markdown += "\n"
        
        # Add complex relationships
        if self.hierarchical_relationships:
            markdown += "## Hierarchical Relationships\n\n"
            for rel in self.hierarchical_relationships:
                markdown += f"- **{rel['table']}**: Self-referencing (hierarchical structure)\n"
            markdown += "\n"
        
        if self.many_to_many_relationships:
            markdown += "## Many-to-Many Relationships\n\n"
            for rel in self.many_to_many_relationships:
                markdown += f"- **{rel['relationship']}**\n"
            markdown += "\n"
        
        # Add join examples
        if self.join_examples:
            markdown += "## Join Examples\n\n"
            for example in self.join_examples:
                markdown += f"### {example['type']}: {example['description']}\n"
                markdown += f"```sql\n{example['sql_pattern']}\n```\n\n"
        
        # Add complex relationship examples
        markdown += "## Complex Relationship Examples\n\n"
        
        # Generate relationship paths
        relationship_paths = []
        for table_name, rel_info in self.relationships.items():
            if rel_info['references']:
                for ref_table in rel_info['references']:
                    relationship_paths.append(f"- `{table_name}` → `{ref_table}`")
        
        if relationship_paths:
            markdown += "**Relationship Paths:**\n"
            for path in relationship_paths:
                markdown += f"{path}\n"
            markdown += "\n"
        
        # Add natural language query examples
        markdown += "## Natural Language Query Examples\n\n"
        markdown += "Based on the schema analysis, here are example queries you can try:\n\n"
        
        # Generate example queries based on table names and relationships
        example_queries = self.generate_example_queries()
        for category, queries in example_queries.items():
            markdown += f"### {category}\n"
            for query in queries:
                markdown += f"- \"{query}\"\n"
            markdown += "\n"
        
        return markdown
    
    def generate_example_queries(self):
        """Generate example natural language queries based on schema."""
        examples = {
            "Basic Queries": [],
            "Relationship Queries": [],
            "Aggregation Queries": [],
            "Complex Queries": []
        }
        
        table_names = list(self.schema_info.keys())
        
        # Basic queries
        for table in table_names:
            examples["Basic Queries"].append(f"Show me all records from {table}")
            examples["Basic Queries"].append(f"List {table} with their details")
        
        # Relationship queries
        for table_name, rel_info in self.relationships.items():
            if rel_info['references']:
                for ref_table in rel_info['references']:
                    examples["Relationship Queries"].append(f"Show {table_name} with their {ref_table} information")
                    examples["Relationship Queries"].append(f"List {table_name} and their related {ref_table}")
        
        # Aggregation queries
        for table in table_names:
            examples["Aggregation Queries"].append(f"How many records are in {table}?")
            examples["Aggregation Queries"].append(f"Show the total count by category in {table}")
        
        # Complex queries
        if len(table_names) >= 2:
            examples["Complex Queries"].append(f"Show data from {table_names[0]} and {table_names[1]} together")
            examples["Complex Queries"].append(f"Find records that exist in both {table_names[0]} and {table_names[1]}")
        
        return examples
    
    def save_markdown(self, output_file):
        """Save the markdown schema to a file."""
        markdown_content = self.generate_markdown_schema()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"✅ Markdown schema saved to: {output_file}")
        return output_file

def main():
    """Main function to analyze the e-commerce database."""
    
    # Database path
    db_path = "/Users/anidhula/learn/DB_SQL_Natural_Language/3_Complex_ecommerce_database/mydb.sqlite"
    
    # Output file
    output_file = "ecommerce_database_schema.md"
    
    print("🚀 Database Schema Analyzer")
    print("=" * 50)
    
    try:
        # Initialize analyzer
        analyzer = DatabaseSchemaAnalyzer(db_path)
        
        # Connect to database
        analyzer.connect()
        
        # Analyze database
        analyzer.analyze_database()
        
        # Generate and save markdown
        analyzer.save_markdown(output_file)
        
        # Disconnect
        analyzer.disconnect()
        
        print("\n🎉 Analysis complete!")
        print(f"📄 Schema documentation: {output_file}")
        print(f"📊 Tables analyzed: {len(analyzer.schema_info)}")
        print(f"🔗 Relationships found: {sum(len(rel['references']) + len(rel['referenced_by']) for rel in analyzer.relationships.values())}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
