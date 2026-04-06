import sqlite3
import os

DB_FILE = "database.db"

def init_database():
    """Initialize database only if it doesn't exist or has no tables"""
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Check if table already exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='scans'")
    table_exists = cursor.fetchone()
    
    if table_exists:
        print(f"Database '{DB_FILE}' already exists with table 'scans'")
        # Count existing records
        cursor.execute("SELECT COUNT(*) FROM scans")
        count = cursor.fetchone()[0]
        print(f"Contains {count} existing records")
    else:
        print("Creating new database table...")
        cursor.execute('''
            CREATE TABLE scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                netid TEXT NOT NULL,
                year TEXT NOT NULL,
                major TEXT NOT NULL,
                scan_time TEXT NOT NULL,
                processed INTEGER DEFAULT 0
            )
        ''')
        print("Table created successfully!")
    
    conn.close()

if __name__ == "__main__":
    init_database()