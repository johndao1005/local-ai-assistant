"""
Setup script for the Local AI Assistant.
This script initializes the environment and downloads required models.
"""
import os
import sys
import requests
from tqdm import tqdm
import sqlite3
import dotenv

def setup_environment():
    """Set up the project environment."""
    print("Setting up environment...")
    
    # Create .env file if it doesn't exist
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write('SECRET_KEY=your_secret_key_here\n')
            f.write('FLASK_ENV=development\n')
        print("Created .env file with default settings")
    
    # Ensure model directory exists
    model_dir = os.path.join('static', 'models')
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
        print(f"Created model directory: {model_dir}")

def download_model():
    """Download the LLM model."""
    model_dir = os.path.join('static', 'models')
    model_path = os.path.join(model_dir, 'mistral-7b-instruct-v0.2.Q4_K_M.gguf')
    
    # Check if model already exists
    if os.path.exists(model_path):
        print(f"Model already exists at {model_path}")
        return True
    
    # Model URL
    url = "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf"
    
    print(f"Downloading model from {url}")
    print("This may take a while depending on your internet connection...")
    
    try:
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        
        with open(model_path, 'wb') as f, tqdm(
            desc="Downloading model",
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in response.iter_content(chunk_size=1024):
                size = f.write(data)
                bar.update(size)
        
        print(f"Model downloaded successfully to {model_path}")
        return True
    
    except Exception as e:
        print(f"Error downloading model: {e}")
        if os.path.exists(model_path):
            os.remove(model_path)
        return False

def init_database():
    """Initialize the SQLite database."""
    from dotenv import load_dotenv
    load_dotenv()
    
    # Get environment and database path
    flask_env = os.getenv('FLASK_ENV', 'development')
    
    # Determine database path based on environment
    if flask_env == 'testing':
        db_path = 'test_knowledge.sqlite'
    else:
        db_path = 'knowledge.sqlite'
    
    print(f"Initializing database at {db_path}...")
    
    # Connect to database and create tables
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
    
    # Create indexes
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_knowledge_title ON knowledge(title)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_knowledge_tags ON knowledge(tags)')
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print("Database initialized successfully")

if __name__ == "__main__":
    print("=== Local AI Assistant Setup ===")
    
    # Set up environment
    setup_environment()
    
    # Initialize database
    init_database()
    
    # Ask if user wants to download the model
    model_prompt = input("\nDo you want to download the model now? (y/n): ").lower()
    if model_prompt.startswith('y'):
        download_model()
    
    print("\nSetup complete! You can now run the application with:")
    print("python app.py")