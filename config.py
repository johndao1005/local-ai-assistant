"""
Configuration settings for the Local AI Assistant.
This file defines different configuration classes for various environments.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev_secret_key')
    DEBUG = False
    TESTING = False
    
    # Model settings
    MODEL_PATH = os.path.join('static', 'models', 'mistral-7b-instruct-v0.2.Q4_K_M.gguf')
    MODEL_CTX_SIZE = 4096
    MODEL_BATCH_SIZE = 512
    
    # Mode settings
    MODES = {
        'normal': {'temperature': 0.7, 'top_p': 0.9, 'max_tokens': 512},
        'code': {'temperature': 0.2, 'top_p': 0.95, 'max_tokens': 1024},
        'creative': {'temperature': 0.9, 'top_p': 1.0, 'max_tokens': 750}
    }
    
    # Knowledge base settings
    DB_PATH = 'knowledge.sqlite'

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

class TestingConfig(Config):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    DB_PATH = 'test_knowledge.sqlite'

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    # In production, you might want to use a more secure secret key
    SECRET_KEY = os.getenv('SECRET_KEY', 'prod_secret_key')

# Configuration dictionary
config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}