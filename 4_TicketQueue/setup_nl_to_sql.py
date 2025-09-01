#!/usr/bin/env python3
"""
Setup script for the Natural Language to SQL system
Helps users get everything configured and running
"""

import os
import subprocess
import sys

def check_python_version():
    """Check if Python version is compatible."""
    print("Checking Python version...")
    
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ is required. Current version:", sys.version)
        return False
    
    print(f"✅ Python version {sys.version.split()[0]} is compatible")
    return True

def install_dependencies():
    """Install required dependencies."""
    print("\nInstalling dependencies...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_database():
    """Create the TicketQueue database if it doesn't exist."""
    print("\nChecking database...")
    
    if os.path.exists('ticketqueue.db'):
        print("✅ TicketQueue database already exists")
        return True
    
    print("Creating TicketQueue database...")
    try:
        subprocess.check_call([sys.executable, "init_ticketqueue_db.py"])
        print("✅ TicketQueue database created successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create database: {e}")
        return False

def setup_environment():
    """Set up environment file."""
    print("\nSetting up environment...")
    
    if os.path.exists('.env'):
        print("✅ .env file already exists")
        return True
    
    if os.path.exists('env_example.txt'):
        try:
            with open('env_example.txt', 'r') as f:
                content = f.read()
            
            with open('.env', 'w') as f:
                f.write(content)
            
            print("✅ .env file created from template")
            print("⚠️  Please edit .env and add your OpenAI API key")
            return True
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False
    else:
        print("❌ env_example.txt not found")
        return False

def run_tests():
    """Run the test suite."""
    print("\nRunning tests...")
    
    try:
        subprocess.check_call([sys.executable, "test_nl_to_sql.py"])
        print("✅ All tests passed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Tests failed: {e}")
        return False

def main():
    """Main setup function."""
    print("🚀 Setting up Natural Language to SQL System")
    print("=" * 50)
    
    steps = [
        ("Python Version Check", check_python_version),
        ("Install Dependencies", install_dependencies),
        ("Create Database", create_database),
        ("Setup Environment", setup_environment),
        ("Run Tests", run_tests)
    ]
    
    failed_steps = []
    
    for step_name, step_func in steps:
        print(f"\n📋 {step_name}...")
        if not step_func():
            failed_steps.append(step_name)
    
    print("\n" + "=" * 50)
    
    if not failed_steps:
        print("🎉 Setup completed successfully!")
        print("\nNext steps:")
        print("1. Edit .env file and add your OpenAI API key")
        print("2. Run: python nl_to_sql_main.py")
        print("3. Open your browser to the URL shown")
        print("\nExample queries to try:")
        print("- 'Show me all ticket items assigned to Bob Developer'")
        print("- 'List all ticket queues with high priority'")
        print("- 'How many ticket items does each user have assigned?'")
    else:
        print("❌ Setup failed on the following steps:")
        for step in failed_steps:
            print(f"   - {step}")
        print("\nPlease fix the issues above and run setup again.")

if __name__ == "__main__":
    main()
