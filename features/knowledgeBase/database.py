"""
Database schema for the knowledge base.
This module creates the database and defines its schema.
"""
import sqlite3
import os
from flask import current_app

def init_db():
    """Initialize the database with required tables."""
    db_path = current_app.config['DB_PATH']
    
    # Check if database directory exists
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create knowledge table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS knowledge (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        tags TEXT,
        created_at TIMESTAMP NOT NULL,
        updated_at TIMESTAMP
    )
    ''')
    
    # Create index on title for faster searching
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_knowledge_title ON knowledge(title)')
    
    # Create index on tags for faster filtering
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_knowledge_tags ON knowledge(tags)')
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    current_app.logger.info(f"Database initialized at {db_path}")