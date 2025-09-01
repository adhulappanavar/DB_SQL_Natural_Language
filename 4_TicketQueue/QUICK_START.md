# Quick Start Guide - Natural Language to SQL for TicketQueue

## 🚀 Get Started in 3 Steps

### 1. Run the Setup Script
```bash
python setup_nl_to_sql.py
```

This will:
- ✅ Check Python version compatibility
- ✅ Install required dependencies (gradio, openai, python-dotenv)
- ✅ Create the TicketQueue database with sample data
- ✅ Set up environment configuration
- ✅ Run tests to verify everything works

### 2. Add Your OpenAI API Key
Edit the `.env` file and add your OpenAI API key:
```
OPENAI_API_KEY=your-actual-openai-api-key-here
```

### 3. Launch the Application
```bash
python nl_to_sql_main.py
```

Open your browser to the URL shown (usually `http://localhost:7860`)

## 🎯 Try These Example Queries

### User Queries
- "Show me all ticket items assigned to Bob Developer"
- "How many ticket items does each user have assigned?"
- "Find users with the most completed tasks"

### Ticket Queue Queries
- "List all ticket queues with high priority"
- "Show ticket queues with their categories"
- "List ticket queues by status"

### Ticket Item Queries
- "Find completed ticket items with their assigned users"
- "Show ticket items that are in progress"
- "What's the average estimated hours for ticket items?"

### Complex Queries
- "Show ticket queues with their categories"
- "List ticket items with their dependencies"
- "Display ticket items with comments"

## 📁 Project Structure

```
wq/
├── ticketqueue.db                    # SQLite database
├── ticketqueue_schema.sql           # Database schema
├── init_ticketqueue_db.py           # Database initialization
├── nl_to_sql_main.py              # Main NL to SQL application
├── test_nl_to_sql.py              # Test suite
├── setup_nl_to_sql.py             # Setup script
├── requirements.txt               # Python dependencies
├── env_example.txt                # Environment template
├── .env                           # Your API keys (create this)
├── README.md                      # TicketQueue database docs
├── NL_TO_SQL_README.md            # Detailed NL to SQL docs
└── QUICK_START.md                 # This file
```

## 🔧 Troubleshooting

### Common Issues

**"OpenAI API Key Error"**
- Make sure you have a valid OpenAI API key in your `.env` file
- Check that your API key has sufficient credits

**"Database Not Found"**
- Run `python init_ticketqueue_db.py` to create the database

**"Import Errors"**
- Run `pip install -r requirements.txt` to install dependencies

**"Port Already in Use"**
- Gradio will automatically find an available port
- Check the console output for the actual URL

### Testing Without OpenAI

If you want to test the system without an OpenAI API key:
```bash
python test_nl_to_sql.py
```

This will test database connectivity and basic functionality.

## 🎨 Features

- **Natural Language Interface**: Ask questions in plain English
- **Real-time SQL Generation**: Uses OpenAI GPT-3.5-turbo
- **Interactive Web UI**: Built with Gradio
- **Database Statistics**: View table counts and summaries
- **Example Queries**: Pre-built examples to get started
- **Error Handling**: Graceful error reporting
- **Schema Awareness**: Understands TicketQueue database structure

## 📊 Database Schema

The system works with a comprehensive TicketQueue database including:

- **Users** (admin, manager, worker roles)
- **Ticket Queues** (with priorities and status)
- **Ticket Items** (with time tracking and dependencies)
- **Categories** (for organizing work)
- **Comments** (on ticket items)
- **Attachments** (file uploads)
- **Dependencies** (task relationships)

## 🚀 Advanced Usage

### Custom Queries
The system can handle complex queries like:
- "Show me all ticket items that are overdue and assigned to managers"
- "Find ticket queues with more than 5 ticket items"
- "List users who have completed tasks in the last 30 days"

### Database Statistics
Use the "Database Statistics" tab to see:
- Record counts for all tables
- Quick overview of data distribution

### Query Patterns
The AI understands common patterns:
- User assignments and ticket load
- Ticket queue priorities and status
- Time tracking and dependencies
- Category organization

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Run the test suite: `python test_nl_to_sql.py`
3. Verify your OpenAI API key is valid
4. Check that all dependencies are installed

## 🎉 Success!

Once everything is working, you'll have a powerful Natural Language to SQL interface for your TicketQueue database that can understand complex queries and generate accurate SQL automatically!
