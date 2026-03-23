"""
REST API routes for external access to portfolio data.
"""

from flask import Blueprint, jsonify, request
from portfolio_app.models import db, Project, Skill, BlogPost, ContactMessage, NewsletterSubscriber
from portfolio_app.utils import is_valid_email

api_bp = Blueprint('api', __name__, url_prefix='/api')


# ── Projects API ────────────────────────────────────────────────────────────────
@api_bp.route('/projects', methods=['GET'])
def get_projects():
    """Get all projects."""
    projects = Project.query.order_by(Project.created_at.desc()).all()
    
    return jsonify([{
        'id': p.id,
        'title': p.title,
        'description': p.description,
        'tech_stack': p.tech_stack.split(',') if p.tech_stack else [],
        'github_url': p.github_url,
        'live_url': p.live_url,
        'featured': p.featured,
        'created_at': p.created_at.isoformat()
    } for p in projects])


@api_bp.route('/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    """Get single project by ID."""
    project = Project.query.get_or_404(project_id)
    
    return jsonify({
        'id': project.id,
        'title': project.title,
        'description': project.description,
        'tech_stack': project.tech_stack.split(',') if project.tech_stack else [],
        'github_url': project.github_url,
        'live_url': project.live_url,
        'featured': project.featured,
        'created_at': project.created_at.isoformat()
    })


# ── Skills API ──────────────────────────────────────────────────────────────────
@api_bp.route('/skills', methods=['GET'])
def get_skills():
    """Get all skills."""
    skills = Skill.query.order_by(Skill.proficiency.desc()).all()
    
    return jsonify([{
        'id': s.id,
        'name': s.name,
        'category': s.category,
        'proficiency': s.proficiency
    } for s in skills])


# ── Contact API ────────────────────────────────────────────────────────────────
@api_bp.route('/contact', methods=['POST'])
def submit_contact():
    """Submit contact message via API."""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data'}), 400
    
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    message = data.get('message', '').strip()
    
    if not name or not email or not message:
        return jsonify({'error': 'name, email, message required'}), 422
    if not is_valid_email(email):
        return jsonify({'error': 'invalid email'}), 422
    
    contact_msg = ContactMessage(
        name=name,
        email=email,
        subject=data.get('subject', ''),
        message=message
    )
    
    db.session.add(contact_msg)
    db.session.commit()
    
    return jsonify({'status': 'sent', 'id': contact_msg.id}), 201


# ── Blog API ────────────────────────────────────────────────────────────────────
@api_bp.route('/blog', methods=['GET'])
def get_blog_posts():
    """Get all published blog posts."""
    posts = BlogPost.query.filter_by(published=True).order_by(BlogPost.created_at.desc()).all()
    
    return jsonify([{
        'id': p.id,
        'title': p.title,
        'slug': p.slug,
        'excerpt': p.excerpt,
        'tags': p.tags.split(',') if p.tags else [],
        'created_at': p.created_at.isoformat()
    } for p in posts])


# ── Newsletter API ──────────────────────────────────────────────────────────────
@api_bp.route('/newsletter', methods=['POST'])
def newsletter_subscribe_api():
    """Subscribe to newsletter via API."""
    data = request.get_json()
    
    if not data or not data.get('email'):
        return jsonify({'error': 'email required'}), 422
    
    email = data['email'].strip()
    if not is_valid_email(email):
        return jsonify({'error': 'invalid email'}), 422
    
    existing = NewsletterSubscriber.query.filter_by(email=email).first()
    
    if existing:
        return jsonify({'status': 'already_subscribed'}), 200
    
    subscriber = NewsletterSubscriber(
        email=email,
        name=data.get('name', '')
    )
    
    db.session.add(subscriber)
    db.session.commit()
    
    return jsonify({'status': 'subscribed'}), 201


# ── Health Check ────────────────────────────────────────────────────────────────
@api_bp.route('/health', methods=['GET'])
def health_check():
    """API health check endpoint."""
    return jsonify({'status': 'ok', 'message': 'Portfolio API is running'}), 200
