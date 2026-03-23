"""
Portfolio Application - Main Entry Point

Simple entry point to run the Flask application.
Run with: python main.py
"""

import os
from portfolio_app import create_app

# Create the Flask application
app = create_app()

if __name__ == '__main__':
    # Get configuration from environment variables
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'

    print("=" * 60)
    print("Portfolio Application Starting")
    print("=" * 60)
    print(f"URL: http://{host}:{port}")
    print(f"Debug: {debug}")
    print(f"Environment: {os.environ.get('FLASK_ENV', 'development')}")
    print("=" * 60)

    # Run the application
    app.run(host=host, port=port, debug=debug)
