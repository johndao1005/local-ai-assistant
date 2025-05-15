"""
Chat processor for handling user messages.
This module processes chat messages and prepares prompts for the model.
"""
from flask import current_app

class ChatProcessor:
    """Processes chat messages and manages conversation context."""
    
    def __init__(self, model_manager):
        """
        Initialize the chat processor.
        
        Args:
            model_manager (ModelManager): The model manager instance
        """
        self.model_manager = model_manager
        
    def process_message(self, message, mode='normal'):
        """
        Process a user message and generate a response.
        
        Args:
            message (str): The user's message
            mode (str): The operating mode
            
        Returns:
            str: The assistant's response
        """
        # Create a prompt for the model
        prompt = self._create_prompt(message)
        
        # Generate response using the model
        response = self.model_manager.generate_response(prompt, mode)
        
        return response
        
    def _create_prompt(self, message):
        """
        Create a prompt for the model based on the user message.
        
        Args:
            message (str): The user's message
            
        Returns:
            str: The formatted prompt
        """
        # Simple prompt format - can be expanded to include context
        return f"USER: {message}\nASSISTANT:"