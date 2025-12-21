"""
Configuration Management for Algorithm Playground
Version: 2.0.0
"""

import os
from datetime import timedelta

class BaseConfig:
    """Base configuration shared across environments"""
    
    # Flask Core
    SECRET_KEY = os.getenv('SECRET_KEY', 'algorithm-playground-secret-key-2024')
    DEBUG = False
    TESTING = False
    
    # Server Configuration
    PORT = int(os.getenv('PORT', 2344))
    HOST = os.getenv('HOST', '0.0.0.0')
    
    # Application Settings
    JSON_SORT_KEYS = False
    SEND_FILE_MAX_AGE_DEFAULT = 31536000
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    
    # Session Configuration
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)
    SESSION_REFRESH_EACH_REQUEST = True
    
    # Logging Configuration
    LOG_TO_FILE = True
    LOG_FILE = 'app.log'
    LOG_LEVEL = 'INFO'
    
    # CORS Configuration
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')
    CORS_METHODS = ['GET', 'POST', 'OPTIONS']
    CORS_ALLOW_HEADERS = ['Content-Type', 'Authorization']
    
    # Algorithm Settings
    MAX_ARRAY_SIZE = 10000
    MAX_GRID_SIZE = 100
    ALGORITHM_TIMEOUT = 30000  # milliseconds
    
    # Feature Flags
    ENABLE_VISUALIZER = True
    ENABLE_BENCHMARKING = True
    ENABLE_COMPARISONS = True
    ENABLE_EXPORT = True

class DevelopmentConfig(BaseConfig):
    """Development environment configuration"""
    
    DEBUG = True
    FLASK_ENV = 'development'
    TESTING = False
    
    # Development-specific settings
    ENV = 'development'
    PROPAGATE_EXCEPTIONS = True
    PRESERVE_CONTEXT_ON_EXCEPTION = True
    
    # Disable some optimizations for debugging
    SEND_FILE_MAX_AGE_DEFAULT = 0
    
    # Enable detailed logging
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(BaseConfig):
    """Production environment configuration"""
    
    DEBUG = False
    FLASK_ENV = 'production'
    TESTING = False
    
    # Production-specific settings
    ENV = 'production'
    PROPAGATE_EXCEPTIONS = False
    
    # Enable caching
    SEND_FILE_MAX_AGE_DEFAULT = 31536000
    
    # Minimal logging
    LOG_LEVEL = 'WARNING'
    
    # Security settings for production
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

class TestingConfig(BaseConfig):
    """Testing environment configuration"""
    
    DEBUG = True
    TESTING = True
    FLASK_ENV = 'testing'
    
    # Testing-specific settings
    ENV = 'testing'
    PROPAGATE_EXCEPTIONS = True
    
    # Disable CSRF for testing
    WTF_CSRF_ENABLED = False
    
    # Use in-memory database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
    # Detailed logging for tests
    LOG_LEVEL = 'DEBUG'

def get_config():
    """Get configuration based on FLASK_ENV"""
    env = os.getenv('FLASK_ENV', 'development').lower()
    
    config_map = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig
    }
    
    return config_map.get(env, DevelopmentConfig)
