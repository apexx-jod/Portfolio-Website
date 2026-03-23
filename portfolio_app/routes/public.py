"""
Public-facing routes (homepage, projects, blog, gallery, etc.).
"""

import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory
from portfolio_app.models import db, Project, Skill, BlogPost, ContactMessage, Testimonial, NewsletterSubscriber, GalleryImage
from portfolio_app.utils import is_valid_email

public_bp = Blueprint('public', __name__)


@public_bp.route('/')
def index():
    """Render homepage."""
    featured_projects = Project.query.filter_by(featured=True).order_by(Project.created_at.desc()).all()
    skills = Skill.query.order_by(Skill.proficiency.desc()).all()
    testimonials = Testimonial.query.filter_by(approved=True).order_by(Testimonial.created_at.desc()).all()
    recent_posts = BlogPost.query.filter_by(published=True).order_by(BlogPost.created_at.desc()).limit(3).all()
    
    return render_template(
        'index.html',
        projects=featured_projects,
        skills=skills,
        testimonials=testimonials,
        recent_posts=recent_posts
    )


@public_bp.route('/projects')
def projects():
    """Display all projects."""
    all_projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('projects.html', projects=all_projects)


@public_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    """Handle contact form submission."""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()
        
        if not name or not email or not message:
            flash('Please fill in all required fields.', 'error')
            return render_template('contact.html')
        if not is_valid_email(email):
            flash('Please enter a valid email address.', 'error')
            return render_template('contact.html')
        
        contact_msg = ContactMessage(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        db.session.add(contact_msg)
        db.session.commit()
        
        flash("Your message has been sent! I'll be in touch soon.", 'success')
        return redirect(url_for('public.contact'))
    
    return render_template('contact.html')


@public_bp.route('/blog')
def blog():
    """Display blog posts with optional tag filter."""
    tag = request.args.get('tag')
    query = BlogPost.query.filter_by(published=True)
    
    if tag:
        query = query.filter(BlogPost.tags.contains(tag))
    
    posts = query.order_by(BlogPost.created_at.desc()).all()
    
    # Extract all unique tags
    all_tags = set()
    for post in BlogPost.query.filter_by(published=True).all():
        if post.tags:
            for t in post.tags.split(','):
                all_tags.add(t.strip())
    
    return render_template(
        'blog.html',
        posts=posts,
        all_tags=sorted(all_tags),
        active_tag=tag
    )


@public_bp.route('/blog/<slug>')
def blog_post(slug):
    """Display individual blog post."""
    post = BlogPost.query.filter_by(slug=slug, published=True).first_or_404()
    related = BlogPost.query.filter(
        BlogPost.published == True,
        BlogPost.id != post.id
    ).order_by(BlogPost.created_at.desc()).limit(2).all()
    
    return render_template('blog_post.html', post=post, related=related)


@public_bp.route('/resume')
def resume():
    """Display resume page."""
    skills = Skill.query.order_by(Skill.category, Skill.proficiency.desc()).all()
    
    skill_groups = {}
    for skill in skills:
        skill_groups.setdefault(skill.category, []).append(skill)
    
    return render_template('resume.html', skill_groups=skill_groups)


@public_bp.route('/resume/download')
def resume_download():
    """Download resume PDF."""
    resume_path = os.path.join('instance', 'resume')
    filename = 'alex-porter-cv.pdf'
    
    if os.path.exists(os.path.join(resume_path, filename)):
        return send_from_directory(resume_path, filename, as_attachment=True)
    
    flash('Resume PDF not yet uploaded. Check back soon!', 'info')
    return redirect(url_for('public.resume'))


@public_bp.route('/gallery')
def gallery():
    """Display gallery with optional category filter."""
    category = request.args.get('cat')
    query = GalleryImage.query
    
    if category:
        query = query.filter_by(category=category)
    
    images = query.order_by(GalleryImage.created_at.desc()).all()
    categories = [c[0] for c in db.session.query(GalleryImage.category).distinct().all()]
    
    return render_template(
        'gallery.html',
        images=images,
        categories=categories,
        active_cat=category
    )


@public_bp.route('/newsletter/subscribe', methods=['POST'])
def newsletter_subscribe():
    """Subscribe to newsletter."""
    email = request.form.get('email', '').strip()
    name = request.form.get('name', '').strip()
    
    if not email or not is_valid_email(email):
        flash('Please enter a valid email address.', 'error')
        return redirect(request.referrer or url_for('public.index'))
    
    existing = NewsletterSubscriber.query.filter_by(email=email).first()
    
    if existing:
        if not existing.active:
            existing.active = True
            db.session.commit()
            flash("Welcome back! You've been re-subscribed.", 'success')
        else:
            flash("You're already subscribed!", 'info')
    else:
        subscriber = NewsletterSubscriber(email=email, name=name)
        db.session.add(subscriber)
        db.session.commit()
        flash("You're subscribed! Thanks for joining.", 'success')
    
    return redirect(request.referrer or url_for('public.index'))


@public_bp.route('/newsletter/unsubscribe/<email>')
def newsletter_unsubscribe(email):
    """Unsubscribe from newsletter."""
    subscriber = NewsletterSubscriber.query.filter_by(email=email).first()
    
    if subscriber:
        subscriber.active = False
        db.session.commit()
    
    flash('You have been unsubscribed.', 'info')
    return redirect(url_for('public.index'))
