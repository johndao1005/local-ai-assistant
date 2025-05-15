"""
Model manager for loading and interacting with the LLM.
This module handles model initialization, inference, and parameter adjustments.
"""
import os
from llama_cpp import Llama
from flask import current_app

class ModelManager:
    """Manages the local LLM model and inference."""
    
    def __init__(self):
        """Initialize the model manager."""
        self.model = None
        self.model_loaded = False
        self._load_model()
    
    def _load_model(self):
        """Load the LLM model."""
        try:
            model_path = current_app.config['MODEL_PATH']
            
            # Check if model exists
            if not os.path.exists(model_path):
                current_app.logger.error(f"Model not found at {model_path}")
                return False
            
            # Load model with llama-cpp-python
            self.model = Llama(
                model_path=model_path,
                n_ctx=current_app.config['MODEL_CTX_SIZE'],
                n_batch=current_app.config['MODEL_BATCH_SIZE']
            )
            
            self.model_loaded = True
            current_app.logger.info("Model loaded successfully")
            return True
            
        except Exception as e:
            current_app.logger.error(f"Error loading model: {e}")
            return False
    
    def generate_response(self, prompt, mode='normal'):
        """
        Generate a response using the loaded model.
        
        Args:
            prompt (str): The input prompt
            mode (str): The operating mode (normal, code, creative)
            
        Returns:
            str: The generated response
        """
        if not self.model_loaded:
            return "Model not loaded. Please check logs for details."
        
        # Get settings for the selected mode
        mode_settings = current_app.config['MODES'].get(
            mode, 
            current_app.config['MODES']['normal']
        )
        
        try:
            # Generate response
            response = self.model(
                prompt,
                max_tokens=mode_settings['max_tokens'],
                temperature=mode_settings['temperature'],
                top_p=mode_settings['top_p'],
                stop=["USER:"],
                echo=False
            )
            
            # Extract and return the generated text
            return response['choices'][0]['text'].strip()
            
        except Exception as e:
            current_app.logger.error(f"Error generating response: {e}")
            return "Sorry, I encountered an error generating a response."