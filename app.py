"""
Main application entry point for the Local AI Assistant.
This file initializes the Flask application and sets up all routes and extensions.
"""
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import os
import uuid
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import configuration
from config import config_by_name

# Create Flask app
app = Flask(__name__)
app.config.from_object(config_by_name[os.getenv('FLASK_ENV', 'development')])

# Generate unique agent ID if not set
if 'AGENT_ID' not in app.config:
    app.config['AGENT_ID'] = str(uuid.uuid4())[:8]

# Set default agent name if not set
if 'AGENT_NAME' not in app.config:
    app.config['AGENT_NAME'] = "Local Assistant"

# Set up Socket.IO
socketio = SocketIO(app)
app.app_context().push()
# Initialize database
from api.knowledge import get_db_connection
def init_db():
    """Initialize the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    # Create knowledge table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS knowledge (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            tags TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
init_db()
# Initialize CORS
from flask_cors import CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})
# Initialize logging
import logging
logging.basicConfig(level=logging.DEBUG)
# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()       
# Import core components after app initialization
from core.model_manager import ModelManager
from core.chat_processor import ChatProcessor
from api.routes import register_routes

# Initialize components
model_manager = ModelManager()
chat_processor = ChatProcessor(model_manager)

# Register API routes
register_routes(app, chat_processor)

# Basic routes
@app.route('/')
def index():
    """Render the main chat interface."""
    return render_template('index.html')

@app.route('/settings')
def settings():
    """Render the settings page."""
    return render_template('settings.html')

@app.route('/agent-manager')
def agent_manager():
    """Render the agent manager page."""
    return render_template('agent_manager.html')

# Socket.IO event handlers
@socketio.on('connect')
def handle_connect():
    """Handle client connection to Socket.IO."""
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection from Socket.IO."""
    print('Client disconnected')

@socketio.on('chat_message')
def handle_message(data):
    """Process incoming chat messages via Socket.IO."""
    user_input = data.get('message', '')
    mode = data.get('mode', 'normal')
    
    # Process the message
    response = chat_processor.process_message(user_input, mode)
    
    # Emit response back to client
    socketio.emit('response', {'response': response})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=app.config['PORT'], debug=app.config['DEBUG'])