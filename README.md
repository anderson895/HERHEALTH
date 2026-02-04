# Project Setup Guide

## Prerequisites
- Python 3.x installed
- pip package manager

## Installation Steps

### 1. Set up Virtual Environment
```bash
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Database Migration
```bash
cd migrations
python run_migration.py
```

**Expected Output:**
```
✅ Successfully connected to the database.
🔹 Starting migration...
Creating 'user' table...
Creating 'chat' table...
Creating indexes...
Adding foreign key constraint...
✅ Migration completed successfully!
🔌 Database connection closed.
```

### 4. Start the Application
```bash
cd ../
python app.py
```

## Troubleshooting
- If migration fails, check your database connection settings
- Ensure all dependencies are properly installed before running migrations