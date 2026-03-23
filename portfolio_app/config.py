"""
Configuration management for Flask Portfolio application.
"""

import os
import secrets
from datetime import timedelta

# Get the root directory (parent of portfolio_app)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


class Config:
    """Base configuration with default settings."""

    # Flask Core
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_urlsafe(48)

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'sqlite:///' + os.path.join(BASE_DIR, 'instance', 'portfolio.db')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }

    # File Uploads
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'instance', 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'pdf'}

    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'false').lower() == 'true'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SECURE = SESSION_COOKIE_SECURE
    REMEMBER_COOKIE_SAMESITE = 'Lax'

    # Security
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None

    # Performance
    SEND_FILE_MAX_AGE_DEFAULT = int(os.environ.get('SEND_FILE_MAX_AGE_DEFAULT', 31536000))

class DevelopmentConfig(Config):
    """Development environment configuration."""

    DEBUG = True
    FLASK_ENV = 'development'
    TESTING = False


class ProductionConfig(Config):
    """Production environment configuration."""

    DEBUG = False
    FLASK_ENV = 'production'
    TESTING = False

    # In production, secure cookies are recommended; can be overridden per env.
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'true').lower() == 'true'
    REMEMBER_COOKIE_SECURE = SESSION_COOKIE_SECURE


class TestingConfig(Config):
    """Testing environment configuration."""

    DEBUG = True
    TESTING = True
    FLASK_ENV = 'testing'

    # Use in-memory database for tests
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

    # Disable CSRF for testing
    WTF_CSRF_ENABLED = False


# Configuration dictionary
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(config_name=None):
    """
    Get configuration object based on environment.

    Args:
        config_name: Name of configuration ('development', 'production', 'testing').
                    If None, uses FLASK_ENV environment variable.

    Returns:
        Configuration class.
    """
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    return config_by_name.get(config_name, DevelopmentConfig)
