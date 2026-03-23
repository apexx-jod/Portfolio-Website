"""
Utility functions for Portfolio application.
"""

import re
import os
from email_validator import EmailNotValidError, validate_email
from werkzeug.utils import secure_filename
from flask import current_app


def allowed_file(filename):
    """Check if file extension is allowed."""
    if '.' not in filename:
        return False
    
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in current_app.config['ALLOWED_EXTENSIONS']


def secure_upload_file(file):
    """Securely save uploaded file and return filename."""
    if not file or not allowed_file(file.filename):
        return None
    
    # Create secure filename
    filename = secure_filename(file.filename)
    if not filename:
        return None
    
    # Generate unique filename to avoid collisions
    import uuid
    ext = filename.rsplit('.', 1)[1].lower()
    unique_filename = f"{uuid.uuid4().hex}.{ext}"
    
    # Ensure upload folder exists
    upload_folder = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)
    
    # Save file
    filepath = os.path.join(upload_folder, unique_filename)
    file.save(filepath)
    
    return unique_filename


def slugify(text):
    """Convert text to URL-friendly slug."""
    if not text:
        return ''
    
    # Convert to lowercase and strip whitespace
    text = text.lower().strip()
    
    # Remove non-alphanumeric characters (except hyphens and spaces)
    text = re.sub(r'[^\w\s-]', '', text)
    
    # Replace spaces and multiple hyphens with single hyphen
    text = re.sub(r'[\s_-]+', '-', text)
    
    # Remove leading/trailing hyphens
    text = text.strip('-')
    
    return text


def generate_unique_slug(base_slug, query_model, existing_id=None):
    """Generate unique slug by appending numbers if needed."""
    slug = base_slug
    counter = 1

    while True:
        # Check if slug exists
        query = query_model.query.filter_by(slug=slug)

        # Exclude existing post when editing
        if existing_id:
            query = query.filter(query_model.id != existing_id)

        if not query.first():
            break

        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug


def get_tag_list(tags_string):
    """Parse comma-separated tags into list."""
    if not tags_string:
        return []
    
    return [tag.strip() for tag in tags_string.split(',') if tag.strip()]


def get_tech_stack(tech_string):
    """Parse comma-separated tech stack into list."""
    if not tech_string:
        return []
    
    return [tech.strip() for tech in tech_string.split(',') if tech.strip()]


def is_valid_email(email):
    """Validate email format without requiring DNS availability."""
    if not email:
        return False

    try:
        validate_email(email, check_deliverability=False)
        return True
    except EmailNotValidError:
        return False
