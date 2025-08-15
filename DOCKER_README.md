# Teaching Platform - Docker Setup

A comprehensive course management platform built with Django and React, now fully containerized with Docker.

## 🐳 Docker Quick Start

### Prerequisites
- Docker Desktop installed and running
- Git (to clone the repository)

### Quick Setup (Recommended)

1. **Clone and navigate to the project:**
   ```bash
   git clone <your-repo-url>
   cd teaching
   ```

2. **Start in development mode:**
   ```bash
   # Linux/Mac
   ./docker.sh dev-build
   
   # Windows
   docker.bat dev-build
   ```

3. **Access the application:**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - Database: localhost:5432

### Production Setup

1. **Build and start production containers:**
   ```bash
   # Linux/Mac
   ./docker.sh build
   ./docker.sh up
   
   # Windows
   docker.bat build
   docker.bat up
   ```

2. **Access the application:**
   - Frontend: http://localhost
   - Backend API: http://localhost:8000

## 🛠️ Available Commands

### Using the Helper Scripts

**Linux/Mac:**
```bash
./docker.sh <command>
```

**Windows:**
```bash
docker.bat <command>
```

### Commands:

| Command | Description |
|---------|-------------|
| `build` | Build Docker images |
| `up` | Start services in production mode |
| `dev` | Start services in development mode |
| `dev-build` | Build and start services in development mode |
| `down` | Stop all services |
| `logs [service]` | Show logs (optionally for specific service) |
| `shell [backend\|frontend]` | Open shell in container |
| `migrate` | Run Django migrations |
| `collectstatic` | Collect Django static files |
| `superuser` | Create Django superuser |
| `clean` | Clean up Docker resources |

### Manual Docker Commands

If you prefer using Docker commands directly:

```bash
# Development
docker-compose -f docker-compose.dev.yml up --build

# Production
docker-compose up --build -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Run migrations
docker-compose exec backend python manage.py migrate

# Create superuser
docker-compose exec backend python manage.py createsuperuser
```

## 📁 Project Structure

```
teaching/
├── docker-compose.yml          # Production Docker setup
├── docker-compose.dev.yml      # Development Docker setup
├── Dockerfile                  # Django backend container
├── docker.sh                   # Helper script (Linux/Mac)
├── docker.bat                  # Helper script (Windows)
├── .dockerignore               # Docker ignore file
├── requirements.txt            # Python dependencies
├── frontend/
│   ├── Dockerfile              # React production container
│   ├── Dockerfile.dev          # React development container
│   ├── nginx.conf              # Nginx configuration
│   └── .dockerignore           # Frontend Docker ignore
└── teaching/
    ├── settings.py             # Original Django settings
    └── settings_docker.py      # Docker-optimized settings
```

## 🔧 Configuration

### Environment Variables

The application supports the following environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `DEBUG` | `True` | Django debug mode |
| `SECRET_KEY` | `django-insecure-...` | Django secret key |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Allowed hosts |
| `DATABASE_URL` | SQLite | PostgreSQL connection string |
| `VITE_API_URL` | `http://localhost:8000` | Frontend API URL |

### Database

- **Development:** PostgreSQL container with persistent data
- **Production:** PostgreSQL container with persistent data
- **Fallback:** SQLite (if DATABASE_URL not provided)

### Services

- **Backend (Django):** Port 8000
- **Frontend (React):** Port 5173 (dev) / Port 80 (prod)
- **Database (PostgreSQL):** Port 5432
- **Redis (optional):** Port 6379

## 🚀 Development Workflow

1. **Start development environment:**
   ```bash
   ./docker.sh dev-build
   ```

2. **Make code changes** - Changes are automatically reloaded

3. **Run migrations when needed:**
   ```bash
   ./docker.sh migrate
   ```

4. **View logs:**
   ```bash
   ./docker.sh logs backend  # Backend logs
   ./docker.sh logs frontend # Frontend logs
   ```

5. **Stop development environment:**
   ```bash
   ./docker.sh down
   ```

## 🎯 Features Included

- ✅ Multi-filter course search system
- ✅ Complete REST API with proper relationships
- ✅ Professional UI with navigation
- ✅ Responsive design
- ✅ PostgreSQL database with persistent storage
- ✅ Nginx reverse proxy for production
- ✅ Hot reload for development
- ✅ Static file serving
- ✅ CORS configuration
- ✅ Security settings for production

## 🔍 Troubleshooting

### Common Issues

1. **Port conflicts:**
   ```bash
   # Check what's using the ports
   netstat -tulpn | grep :8000
   netstat -tulpn | grep :5173
   ```

2. **Permission issues (Linux/Mac):**
   ```bash
   chmod +x docker.sh
   ```

3. **Database connection issues:**
   ```bash
   # Reset the database
   ./docker.sh down
   docker volume prune
   ./docker.sh up
   ```

4. **Clean start:**
   ```bash
   ./docker.sh clean
   ./docker.sh dev-build
   ```

### Useful Commands

```bash
# Check running containers
docker ps

# Check Docker images
docker images

# Check Docker volumes
docker volume ls

# Clean up everything
docker system prune -a --volumes
```

## 📝 Notes

- The development setup includes hot reload for both frontend and backend
- Database data persists between container restarts
- Static files are automatically collected and served
- CORS is configured for local development
- Production setup uses Nginx for serving static files and reverse proxy

For more information, see the individual Dockerfile configurations and docker-compose files.
