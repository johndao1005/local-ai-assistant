"""
Knowledge API endpoint implementation.
This module handles knowledge database operations.
"""
import sqlite3
from flask import jsonify, current_app
import json

def get_db_connection():
    """Create a connection to the SQLite database."""
    conn = sqlite3.connect(current_app.config['DB_PATH'])
    conn.row_factory = sqlite3.Row
    return conn

def get_knowledge():
    """
    Retrieve all knowledge entries from the database.
    
    Returns:
        Response: JSON with knowledge entries
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM knowledge ORDER BY created_at DESC')
        knowledge = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return jsonify({'knowledge': knowledge})
    
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

def add_knowledge(request):
    """
    Add a new knowledge entry to the database.
    
    Args:
        request (Request): The Flask request object
        
    Returns:
        Response: JSON confirmation or error
    """
    data = request.json
    
    if not data or 'content' not in data:
        return jsonify({'error': 'No content provided'}), 400
    
    content = data.get('content', '')
    title = data.get('title', 'Untitled')
    tags = data.get('tags', [])
    
    # Convert tags to JSON string
    tags_json = json.dumps(tags)
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO knowledge (title, content, tags, created_at) VALUES (?, ?, ?, datetime("now"))',
            (title, content, tags_json)
        )
        conn.commit()
        knowledge_id = cursor.lastrowid
        conn.close()
        
        return jsonify({'id': knowledge_id, 'message': 'Knowledge added successfully'})
    
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

def delete_knowledge(knowledge_id):
    """
    Delete a knowledge entry from the database.
    
    Args:
        knowledge_id (int): ID of the knowledge entry to delete
        
    Returns:
        Response: JSON confirmation or error
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM knowledge WHERE id = ?', (knowledge_id,))
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Knowledge deleted successfully'})
    
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500