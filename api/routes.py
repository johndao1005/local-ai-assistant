"""
API route definitions for the Local AI Assistant.
This module registers all API endpoints with the Flask application.
"""
from flask import request, jsonify
# from .chat import chat_endpoint
from .knowledge import get_knowledge, add_knowledge, delete_knowledge
from .search import search_endpoint, get_webpage_endpoint

def register_routes(app, chat_processor):
    """
    Register all API routes.
    
    Args:
        app (Flask): The Flask application
        chat_processor (ChatProcessor): The chat processor instance
    """
    # # Register chat endpoint
    # @app.route('/api/chat', methods=['POST'])
    # def chat():
    #     return chat_endpoint(request, chat_processor)
    
    # Knowledge base endpoints
    @app.route('/api/knowledge', methods=['GET'])
    def api_get_knowledge():
        return get_knowledge()
    
    @app.route('/api/knowledge', methods=['POST'])
    def api_add_knowledge():
        return add_knowledge(request)
    
    @app.route('/api/knowledge/<int:knowledge_id>', methods=['DELETE'])
    def api_delete_knowledge(knowledge_id):
        return delete_knowledge(knowledge_id)
    
    # Search endpoints
    @app.route('/api/search', methods=['POST'])
    def api_search():
        return search_endpoint(request)
    
    @app.route('/api/webpage', methods=['POST'])
    def api_get_webpage():
        return get_webpage_endpoint(request)