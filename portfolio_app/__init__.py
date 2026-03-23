"""
Application factory and core Flask app initialization.
"""

import os
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from portfolio_app.config import get_config
from portfolio_app.models import db
from portfolio_app.database import init_db, seed_db
from portfolio_app.routes import register_blueprints


def create_app(config=None):
    """
    Application factory function.
    
    Args:
        config: Configuration object. If None, uses environment-based config.
    
    Returns:
        Configured Flask application instance.
    """
    
    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'),
        static_folder=os.path.join(os.path.dirname(__file__), '..', 'static')
    )
    
    # Load configuration
    if config is None:
        config = get_config()
    
    app.config.from_object(config)

    if os.environ.get('TRUST_PROXY', 'false').lower() == 'true':
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    register_blueprints(app)
    
    # Initialize database
    with app.app_context():
        init_db(app)
        seed_db()
    
    # Create necessary directories
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join('instance', 'resume'), exist_ok=True)
    
    # Register error handlers
    register_error_handlers(app)

    @app.after_request
    def add_security_headers(response):
        """Apply conservative HTTP security headers for the public site."""
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response.headers['Permissions-Policy'] = 'camera=(), microphone=(), geolocation=()'
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; "
            "img-src 'self' data: https:; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com; "
            "script-src 'self' 'unsafe-inline'; "
            "connect-src 'self'; "
            "frame-ancestors 'none'; "
            "base-uri 'self'; "
            "form-action 'self'"
        )
        return response
    
    return app


def register_error_handlers(app):
    """Register error handlers for the application."""
    
    @app.errorhandler(404)
    def not_found_error(error):
        """Handle 404 errors."""
        from flask import render_template
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors."""
        from flask import render_template
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(403)
    def forbidden_error(error):
        """Handle 403 errors."""
        from flask import render_template
        return render_template('errors/403.html'), 403
