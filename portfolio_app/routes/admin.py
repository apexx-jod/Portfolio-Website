"""
Admin dashboard routes for managing projects, blog posts, messages, etc.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from portfolio_app.models import db, Project, BlogPost, ContactMessage, Testimonial, NewsletterSubscriber, GalleryImage
from portfolio_app.utils import slugify, generate_unique_slug

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/')
@login_required
def dashboard():
    """Render admin dashboard."""
    if not current_user.is_admin:
        flash('Access denied.', 'error')
        return redirect(url_for('public.index'))
    
    projects = Project.query.order_by(Project.created_at.desc()).all()
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    unread_count = ContactMessage.query.filter_by(read=False).count()
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    subscribers = NewsletterSubscriber.query.filter_by(active=True).count()
    gallery_count = GalleryImage.query.count()
    testimonials = Testimonial.query.order_by(Testimonial.created_at.desc()).all()
    
    return render_template(
        'admin.html',
        projects=projects,
        messages=messages,
        unread=unread_count,
        posts=posts,
        subscribers=subscribers,
        gallery_count=gallery_count,
        testimonials=testimonials
    )


# ── Messages ────────────────────────────────────────────────────────────────────
@admin_bp.route('/message/<int:msg_id>/read', methods=['POST'])
@login_required
def mark_message_read(msg_id):
    """Mark contact message as read."""
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    msg = ContactMessage.query.get_or_404(msg_id)
    msg.read = True
    db.session.commit()
    
    return jsonify({'status': 'ok'})


@admin_bp.route('/message/<int:msg_id>/delete', methods=['POST'])
@login_required
def delete_message(msg_id):
    """Delete contact message."""
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    msg = ContactMessage.query.get_or_404(msg_id)
    db.session.delete(msg)
    db.session.commit()
    
    return jsonify({'status': 'deleted'})


# ── Blog Posts ──────────────────────────────────────────────────────────────────
@admin_bp.route('/blog/new', methods=['GET', 'POST'])
@login_required
def create_post():
    """Create new blog post."""
    if not current_user.is_admin:
        flash('Access denied.', 'error')
        return redirect(url_for('public.index'))
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        
        if not title or not content:
            flash('Title and content are required.', 'error')
            return render_template('admin_post_form.html', post=None)
        
        base_slug = slugify(title)
        slug = generate_unique_slug(base_slug, BlogPost)
        
        post = BlogPost(
            title=title,
            slug=slug,
            excerpt=request.form.get('excerpt', '').strip(),
            content=content,
            tags=request.form.get('tags', '').strip(),
            published='published' in request.form,
            author_id=current_user.id
        )
        
        db.session.add(post)
        db.session.commit()
        
        flash('Post created!', 'success')
        return redirect(url_for('admin.dashboard'))
    
    return render_template('admin_post_form.html', post=None)


@admin_bp.route('/blog/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    """Edit existing blog post."""
    if not current_user.is_admin:
        flash('Access denied.', 'error')
        return redirect(url_for('public.index'))
    
    post = BlogPost.query.get_or_404(post_id)
    
    if request.method == 'POST':
        post.title = request.form.get('title', '').strip()
        post.excerpt = request.form.get('excerpt', '').strip()
        post.content = request.form.get('content', '').strip()
        post.tags = request.form.get('tags', '').strip()
        post.published = 'published' in request.form
        post.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        flash('Post updated!', 'success')
        return redirect(url_for('admin.dashboard'))
    
    return render_template('admin_post_form.html', post=post)


@admin_bp.route('/blog/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    """Delete blog post."""
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    post = BlogPost.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    
    return jsonify({'status': 'deleted'})


# ── Testimonials ────────────────────────────────────────────────────────────────
@admin_bp.route('/testimonial/<int:t_id>/toggle', methods=['POST'])
@login_required
def toggle_testimonial(t_id):
    """Toggle testimonial approval status."""
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    testimonial = Testimonial.query.get_or_404(t_id)
    testimonial.approved = not testimonial.approved
    db.session.commit()
    
    return jsonify({'status': 'ok', 'approved': testimonial.approved})


@admin_bp.route('/testimonial/<int:t_id>/delete', methods=['POST'])
@login_required
def delete_testimonial(t_id):
    """Delete testimonial."""
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    testimonial = Testimonial.query.get_or_404(t_id)
    db.session.delete(testimonial)
    db.session.commit()
    
    return jsonify({'status': 'deleted'})
