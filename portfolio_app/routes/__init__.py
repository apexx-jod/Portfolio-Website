"""
Route blueprints initialization.
"""

from portfolio_app.routes.public import public_bp
from portfolio_app.routes.api import api_bp


def register_blueprints(app):
    """Register all route blueprints with the Flask app."""
    app.register_blueprint(public_bp)
    app.register_blueprint(api_bp)
