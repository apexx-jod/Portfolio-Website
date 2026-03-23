# Portfolio Website

A modern personal portfolio website built with Flask, SQLite, and a clean, responsive UI. Features a complete dashboard, blog system, project showcase, REST API, and Docker support.
![WhatsApp Image 2026-03-23 at 7 53 03 PM](https://github.com/user-attachments/assets/1176433c-13e0-4440-9694-0da74dd57d47)


## Features

| Feature | Details |
|---------|---------|
| User Authentication | Register, Login, Logout with hashed passwords |
| Database | SQLite with SQLAlchemy ORM |
| REST API | Full JSON API for projects, skills, and contact |
| Contact Form | Messages stored in database, viewable in dashboard |
| Dashboard | Manage projects, blog posts, messages, testimonials and gallery |
| Blog System | Create, edit, publish blog posts with tags and search |
| Gallery | Upload and organize portfolio images by category |
| Newsletter | Email subscription management system |
| Skills and Testimonials | Showcase technical expertise and client testimonials |
| Docker Ready | Production grade Dockerfile with Gunicorn |
| Responsive | Mobile first design with modern UI |
| Security | CSRF protection, secure passwords, role based access control |

## Project Structure

```
portfolio/
├── main.py                       # Application entry point
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Docker image definition
├── docker-compose.yml            # Docker Compose configuration
├── .dockerignore                 # Docker ignore rules
├── .env.example                  # Environment variables template
├── .gitignore                    # Git ignore rules
├── README.md                     # This file
│
├── portfolio_app/                # Application package
│   ├── __init__.py               # App factory and initialization
│   ├── config.py                 # Configuration management
│   ├── models.py                 # Database models
│   ├── database.py               # DB initialization and seeding
│   ├── utils.py                  # Helper functions
│   └── routes/                   # Route blueprints
│       ├── __init__.py           # Blueprint registration
│       ├── public.py             # Public facing routes
│       ├── admin.py              # Dashboard routes
│       ├── auth.py               # Authentication routes
│       └── api.py                # REST API endpoints
│
├── templates/                    # Jinja2 templates
│   ├── base.html                 # Base template
│   ├── index.html                # Homepage
│   ├── projects.html             # Projects page
│   ├── blog.html                 # Blog list
│   ├── blog_post.html            # Single blog post
│   ├── contact.html              # Contact form
│   ├── gallery.html              # Image gallery
│   ├── resume.html               # Resume page
│   ├── login.html                # Login page
│   ├── register.html             # Registration page
│   ├── admin.html                # Dashboard
│   ├── admin_post_form.html      # Blog post form
│   └── errors/                   # Error pages
│       ├── 403.html              # Forbidden
│       ├── 404.html              # Not found
│       └── 500.html              # Server error
│
├── static/                       # Static files
│   ├── css/
│   │   └── style.css             # Main stylesheet
│   └── js/
│       └── main.js               # JavaScript
│
└── instance/                     # Data directory (gitignored)
    ├── portfolio.db              # SQLite database
    ├── uploads/                  # User uploads
    └── resume/                   # Resume PDFs
```

## Quick Start

### Option 1: Docker (Recommended)

```bash
# 1. Clone the repository
git clone <repository_url> portfolio
cd portfolio

# 2. Create environment file
cp .env.example .env
# Edit .env with your configuration

# 3. Build and run with Docker Compose
docker-compose up --build

# 4. Open your browser at http://localhost:5000
```

#### Docker Commands

```bash
# Start in background
docker-compose up -d

# Stop containers
docker-compose down

# View logs
docker-compose logs -f

# Rebuild after changes
docker-compose up --build

# Stop and remove all data
docker-compose down -v
```

### Option 2: Python (Local Development)

#### Prerequisites
Python 3.11 or higher

#### Setup

```bash
# 1. Clone the repository
git clone <repository_url> portfolio
cd portfolio

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Set environment variables
export SECRET_KEY=your_secret_key_here
export ADMIN_USERNAME=your_username
export ADMIN_EMAIL=your_email@example.com
export ADMIN_PASSWORD=your_secure_password

# 6. Run the application
python main.py

# 7. Open your browser at http://localhost:5000
```

## Environment Configuration

Create a `.env` file based on `.env.example`:

```env
# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=false
SECRET_KEY=your_secret_key_here

# Database
DATABASE_URL=sqlite:///instance/portfolio.db

# Server
PORT=5000
HOST=0.0.0.0

# Authentication (required for initial setup)
ADMIN_USERNAME=your_username
ADMIN_EMAIL=your_email@example.com
ADMIN_PASSWORD=your_secure_password
```

**Note**: All credentials must be set via environment variables. The application requires these values to be configured before the first run.

## Docker

### Build and Run

```bash
# Build and start
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Docker Environment Variables

Create a `.env` file with your configuration:

```env
SECRET_KEY=your_production_secret_key
ADMIN_USERNAME=your_username
ADMIN_PASSWORD=your_secure_password
ADMIN_EMAIL=your_email@example.com
```

### Data Persistence

Docker volumes ensure your data persists:
- `app_instance` : Database and uploads
- `app_static` : Static file uploads

### Reset Docker Data

```bash
# Stop and remove all data
docker-compose down -v

# Start fresh
docker-compose up --build
```

## Database

### Automatic Setup
The database is automatically created on first run and seeded with sample data including projects, blog posts, skills, and testimonials.

### Reset Database

**Python:**
```bash
rm instance/portfolio.db
python main.py
```

**Docker:**
```bash
docker-compose down -v
docker-compose up --build
```

## API Endpoints

### Public Routes
- `GET /` : Homepage
- `GET /projects` : All projects
- `GET /blog` : Blog posts
- `GET /blog/<slug>` : Individual blog post
- `GET /gallery` : Image gallery
- `GET /resume` : Resume page
- `POST /contact` : Submit contact form
- `POST /newsletter/subscribe` : Subscribe to newsletter

### REST API
- `GET /api/projects` : List all projects
- `GET /api/projects/<id>` : Get project details
- `POST /api/projects` : Create project (authenticated)
- `DELETE /api/projects/<id>` : Delete project (authenticated)
- `GET /api/skills` : List all skills
- `GET /api/blog` : List published blog posts
- `POST /api/contact` : Submit message via API
- `POST /api/newsletter` : Subscribe to newsletter
- `GET /api/health` : API health check

### Authentication Routes
- `GET/POST /login` : User login
- `GET /logout` : User logout
- `GET/POST /register` : User registration

### Dashboard Routes (Login Required)
- `GET /admin` : Dashboard
- `POST /admin/message/<id>/read` : Mark message as read
- `POST /admin/message/<id>/delete` : Delete message
- `GET/POST /admin/blog/new` : Create blog post
- `GET/POST /admin/blog/<id>/edit` : Edit blog post
- `POST /admin/blog/<id>/delete` : Delete blog post

### Example API Calls

```bash
# Get all projects
curl http://localhost:5000/api/projects

# Get health status
curl http://localhost:5000/api/health

# Submit a contact message
curl -X POST http://localhost:5000/api/contact \
  -H "Content-Type: application/json" \
  -d '{"name":"Jane","email":"jane@example.com","message":"Hello!"}'
```

## Deployment

### Docker Deployment (Recommended)

```bash
# Build production image
docker build -t portfolio:latest .

# Run container
docker run -d -p 5000:5000 \
  -e SECRET_KEY=your_secret_key \
  -e FLASK_ENV=production \
  -e ADMIN_USERNAME=your_username \
  -e ADMIN_EMAIL=your_email@example.com \
  -e ADMIN_PASSWORD=your_secure_password \
  -v portfolio_data:/app/instance \
  --name portfolio \
  portfolio:latest
```

### Traditional Server with Gunicorn

```bash
pip install gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 4 main:app
```

### Nginx Reverse Proxy

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

## Security Checklist

Before deploying to production:

- Set `SECRET_KEY` to a long random string
- Configure secure credentials
- Set `FLASK_DEBUG=false`
- Set `FLASK_ENV=production`
- Use HTTPS/SSL certificates
- Enable `SESSION_COOKIE_SECURE=true`

## Dependencies

- Flask 3.0.0 : Web framework
- Flask SQLAlchemy 3.1.1 : ORM
- Flask Login 0.6.3 : Authentication
- Flask WTF 1.2.1 : Forms and CSRF protection
- Werkzeug 3.0.1 : Security utilities
- Gunicorn 21.2.0 : Production server
- python dotenv 1.0.0 : Environment management

## License

MIT License. Feel free to use this as a template for your own portfolio.

## Contributing

Contributions are welcome. Please feel free to submit a Pull Request.

