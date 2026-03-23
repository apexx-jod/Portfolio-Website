"""
Database initialization and seeding for Portfolio application.
"""

from datetime import datetime
from portfolio_app.models import db, Project, Skill, BlogPost, Testimonial


def init_db(app):
    """Initialize database tables."""
    with app.app_context():
        db.create_all()


def seed_db():
    """Seed database with initial data."""
    
    # Seed Projects
    if Project.query.count() == 0:
        projects = [
            Project(
                title="E Commerce Platform",
                description="A full stack e commerce solution with real time inventory management, payment processing, and a sleek customer dashboard.",
                tech_stack="Python,Flask,React,PostgreSQL,Stripe",
                github_url="#",
                live_url="#",
                featured=True
            ),
            Project(
                title="AI Chat Assistant",
                description="Intelligent conversational AI powered by modern LLMs, featuring context memory, multi language support, and voice input.",
                tech_stack="Python,FastAPI,OpenAI,WebSockets,Redis",
                github_url="#",
                live_url="#",
                featured=True
            ),
            Project(
                title="Data Visualisation Dashboard",
                description="Interactive analytics dashboard with beautiful charts, real time data streaming, and customisable widgets for business intelligence.",
                tech_stack="D3.js,Python,Pandas,PostgreSQL,Docker",
                github_url="#",
                live_url="#",
                featured=True
            ),
            Project(
                title="Mobile Fitness App",
                description="Cross platform fitness tracker with workout logging, progress analytics, social challenges, and personalised training plans.",
                tech_stack="React Native,Node.js,MongoDB,Firebase",
                github_url="#",
                live_url="#",
                featured=False
            ),
            Project(
                title="DevOps Automation Suite",
                description="End to end CI/CD pipeline automation with Kubernetes orchestration, monitoring dashboards, and one click deployment workflows.",
                tech_stack="Python,Kubernetes,Docker,Terraform,GitHub Actions",
                github_url="#",
                live_url="#",
                featured=False
            ),
            Project(
                title="Open Source CMS",
                description="Headless CMS with a visual editor, multi site support, role based permissions, and REST + GraphQL APIs.",
                tech_stack="TypeScript,Next.js,GraphQL,PostgreSQL,AWS S3",
                github_url="#",
                live_url="#",
                featured=False
            ),
        ]
        db.session.add_all(projects)
        db.session.commit()
    
    # Seed Skills
    if Skill.query.count() == 0:
        skills = [
            Skill(name="Python", category="Backend", proficiency=95),
            Skill(name="Flask / FastAPI", category="Backend", proficiency=92),
            Skill(name="JavaScript", category="Frontend", proficiency=88),
            Skill(name="React", category="Frontend", proficiency=85),
            Skill(name="PostgreSQL", category="Database", proficiency=87),
            Skill(name="Docker", category="DevOps", proficiency=83),
            Skill(name="AWS", category="Cloud", proficiency=78),
            Skill(name="Git & CI/CD", category="DevOps", proficiency=90),
            Skill(name="REST APIs", category="Backend", proficiency=94),
            Skill(name="Machine Learning", category="AI/ML", proficiency=72),
            Skill(name="TypeScript", category="Frontend", proficiency=80),
            Skill(name="Linux / Bash", category="DevOps", proficiency=85),
        ]
        db.session.add_all(skills)
        db.session.commit()
    
    # Seed Blog Posts
    if BlogPost.query.count() == 0:
        posts = [
            BlogPost(
                title="Building Scalable REST APIs with Flask",
                slug="building-scalable-rest-apis-flask",
                excerpt="A deep dive into designing production ready REST APIs using Flask, SQLAlchemy, and best practices for authentication and rate limiting.",
                content="## Introduction\n\nBuilding a REST API that scales is both an art and a science. In this post, I'll walk through the key decisions I make when architecting Flask APIs for production.\n\n## Project Structure\n\nA well-organised Flask project separates concerns cleanly.",
                tags="Flask,Python,API,Backend",
                published=True
            ),
            BlogPost(
                title="Docker for Python Developers: A Practical Guide",
                slug="docker-python-developers-practical-guide",
                excerpt="Everything you need to containerise your Python applications properly, from Dockerfiles to multi stage builds and docker compose workflows.",
                content="## Why Docker?\n\nDocker eliminates the classic \"works on my machine\" problem. Every environment runs the exact same container.",
                tags="Docker,DevOps,Python,Containers",
                published=True
            ),
            BlogPost(
                title="CSS Architecture for Large Projects",
                slug="css-architecture-large-projects",
                excerpt="How I structure CSS at scale using custom properties, utility patterns, and component scoped styles to keep codebases maintainable.",
                content="## The Problem with CSS at Scale\n\nCSS is easy to write but notoriously hard to maintain. Without a clear architecture, stylesheets become a tangled mess.",
                tags="CSS,Frontend,Design,Architecture",
                published=True
            ),
        ]
        db.session.add_all(posts)
        db.session.commit()
    
    # Seed Testimonials
    if Testimonial.query.count() == 0:
        testimonials = [
            Testimonial(
                name="Sarah Chen",
                title="CTO",
                company="TechVentures Inc.",
                quote="Alex delivered our entire platform rewrite in record time. The code quality was exceptional — clean, well-tested, and thoroughly documented.",
                rating=5
            ),
            Testimonial(
                name="Marcus Reid",
                title="Product Manager",
                company="GrowthLab",
                quote="Working with Alex felt like having a senior engineer and a product thinker in one. He proactively identified issues we hadn't even considered.",
                rating=5
            ),
            Testimonial(
                name="Priya Nair",
                title="Founder",
                company="DataPulse",
                quote="Alex built our entire data pipeline from scratch. The performance improvements were dramatic — queries went from 8 seconds to under 200ms.",
                rating=5
            ),
            Testimonial(
                name="James Okafor",
                title="Engineering Lead",
                company="Finflow",
                quote="I've worked with many freelancers, but Alex stands out for communication and reliability. He hits every deadline and always flags blockers early.",
                rating=5
            ),
        ]
        db.session.add_all(testimonials)
        db.session.commit()
