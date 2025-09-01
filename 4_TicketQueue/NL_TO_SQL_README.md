# Natural Language to SQL Query System for TicketQueue

This project provides a Natural Language to SQL query interface for the TicketQueue database using Gradio and OpenAI.

## Features

- **Natural Language Queries**: Ask questions about the TicketQueue database in plain English
- **Automatic SQL Generation**: Uses OpenAI GPT-3.5-turbo to convert natural language to SQL
- **Interactive Web Interface**: Built with Gradio for easy interaction
- **Database Statistics**: View basic statistics about the TicketQueue database
- **Example Queries**: Pre-built examples to get you started
- **Real-time Results**: Execute queries and see results immediately

## Prerequisites

- Python 3.7+
- OpenAI API key
- TicketQueue database (created by `init_ticketqueue_db.py`)

## Installation

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**:
   ```bash
   # Copy the example environment file
   cp env_example.txt .env
   
   # Edit .env and add your OpenAI API key
   OPENAI_API_KEY=your-actual-openai-api-key-here
   ```

3. **Create the TicketQueue database** (if not already done):
   ```bash
   python init_ticketqueue_db.py
   ```

## Usage

### Starting the Application

```bash
python nl_to_sql_main.py
```

This will launch a web interface at `http://localhost:7860` (or another port if 7860 is busy).

### Using the Interface

1. **NL to SQL Query Tab**:
   - Enter your natural language query in the text box
   - Click "Submit" or press Enter
   - View the generated SQL and results

2. **Database Statistics Tab**:
   - View basic statistics about all tables in the database
   - No input required, just click to see the stats

### Example Queries

The interface includes several example queries you can try:

#### User and Assignment Queries
- "Show me all ticket items assigned to Bob Developer"
- "How many ticket items does each user have assigned?"
- "Find users with the most completed tasks"

#### Ticket Queue Queries
- "List all ticket queues with high priority"
- "Show ticket queues with their categories"
- "List ticket queues by status"

#### Ticket Item Queries
- "Find completed ticket items with their assigned users"
- "Show ticket items that are in progress"
- "What's the average estimated hours for ticket items?"
- "Show ticket items that are overdue"

#### Complex Queries
- "Show ticket queues with their categories"
- "List ticket items with their dependencies"
- "Display ticket items with comments"

## Database Schema

The system works with the following TicketQueue database tables:

### Core Tables
- **users**: User accounts with roles (admin, manager, worker)
- **ticket_queue**: Main ticket queue entries with priorities and status
- **ticket_items**: Individual ticket items within queues
- **ticket_queue_categories**: Categories for organizing ticket queues

### Supporting Tables
- **ticket_item_comments**: Comments on ticket items
- **ticket_item_attachments**: File attachments for ticket items
- **ticket_queue_category_assignment**: Many-to-many relationship between queues and categories
- **ticket_item_dependencies**: Dependencies between ticket items

## Query Patterns

The system understands common query patterns and relationships:

### User Queries
- Ticket items assigned to specific users
- User ticket load and task completion statistics
- User roles and responsibilities

### Ticket Queue Queries
- Queue status and priority filtering
- Queue categories and organization
- Queue assignment and management

### Ticket Item Queries
- Item status tracking (pending, in_progress, completed, failed)
- Time tracking (estimated vs actual hours)
- Dependencies and prerequisites
- Comments and attachments

### Complex Relationships
- Users assigned to ticket queues and ticket items
- Ticket items belonging to ticket queues
- Categories assigned to ticket queues
- Dependencies between ticket items

## Technical Details

### OpenAI Integration
- Uses GPT-3.5-turbo model
- Temperature set to 0 for consistent SQL generation
- Max tokens: 500 for complex queries
- Schema-aware prompting for accurate SQL generation

### SQL Generation
- Generates SQLite-compatible queries
- Handles JOINs for related tables
- Supports aggregation functions (COUNT, AVG, SUM, etc.)
- Includes proper WHERE clauses and ORDER BY statements

### Error Handling
- Graceful handling of OpenAI API errors
- SQL execution error reporting
- Database connection error handling
- Input validation and sanitization

## Customization

### Adding New Query Examples
Edit the `examples` list in `nl_to_sql_main.py`:

```python
examples=[
    "Your new example query here",
    "Another example query",
    # ... existing examples
]
```

### Modifying the Prompt
Edit the `prompt` variable in the `nl2sql()` function to customize how the AI generates SQL.

### Adding New Tables
If you add new tables to the TicketQueue database, the system will automatically detect them and include them in the schema.

## Troubleshooting

### Common Issues

1. **OpenAI API Key Error**:
   - Ensure your `.env` file contains a valid OpenAI API key
   - Check that the API key has sufficient credits

2. **Database Not Found**:
   - Run `python init_ticketqueue_db.py` to create the database
   - Ensure `ticketqueue.db` exists in the current directory

3. **Import Errors**:
   - Install all dependencies: `pip install -r requirements.txt`
   - Check Python version (requires 3.7+)

4. **Port Already in Use**:
   - Gradio will automatically find an available port
   - Check the console output for the actual URL

### Performance Tips

- Use specific queries for better results
- Include table names in your natural language queries
- Be specific about what data you want to see

## Security Considerations

- Never commit your `.env` file with real API keys
- The system only reads from the database (no write operations)
- SQL injection is prevented by using parameterized queries
- OpenAI API calls are made securely over HTTPS

## Contributing

To extend the system:

1. Add new query patterns to the prompt
2. Include additional example queries
3. Enhance the database statistics view
4. Add new visualization features
5. Implement query history and favorites

## License

This project is open source and available under the MIT License.
