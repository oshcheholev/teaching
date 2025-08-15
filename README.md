# Teaching App

University course management system built with Django (backend) and React (frontend), containerized with Docker.

## 🚀 Quick Start

### Prerequisites
- Docker installed on your system
- Git (for cloning the repository)

### Running the Application

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd teaching
   ```

2. **Build and run with Docker:**
   ```bash
   # Windows (PowerShell)
   .\rebuild-docker.ps1
   
   # Linux/Mac
   ./rebuild-docker.sh
   ```

3. **Access the application:**
   - **Frontend**: http://localhost:5173
   - **Backend API**: http://localhost:8000
   - **Admin Panel**: http://localhost:8000/admin

### Manual Docker Commands

If you prefer to run commands manually:

```bash
# Build the unified image
docker build -t teaching-fullstack .

# Run the container
docker run -d --name teaching-app -p 8000:8000 -p 5173:5173 -v $(pwd)/teaching/db.sqlite3:/app/teaching/db.sqlite3 teaching-fullstack

# View logs
docker logs teaching-app

# Stop and remove
docker stop teaching-app
docker rm teaching-app
```

## 🏗️ Architecture

- **Frontend**: React + Vite (served on port 5173)
- **Backend**: Django REST Framework (served on port 8000)
- **Database**: SQLite (persisted via Docker volume)
- **Web Server**: Nginx (proxies frontend and API requests)
- **Process Management**: Supervisor (manages Django and Nginx)

## 📁 Project Structure

```
teaching/
├── Dockerfile              # Unified Docker configuration
├── requirements.txt         # Python dependencies
├── rebuild-docker.ps1       # Windows rebuild script
├── rebuild-docker.sh        # Linux/Mac rebuild script
├── frontend/               # React frontend
│   ├── package.json
│   ├── src/
│   └── ...
└── teaching/               # Django backend
    ├── manage.py
    ├── api/
    └── ...
```

## 🔧 Development

### Making Code Changes

After making changes to your code, rebuild and restart the container:

```bash
# Windows
.\rebuild-docker.ps1

# Linux/Mac  
./rebuild-docker.sh
```

### Database Management

The SQLite database is persisted using Docker volumes. To reset the database:

```bash
docker stop teaching-app
docker rm teaching-app
# Delete the database file if needed
docker run -d --name teaching-app -p 8000:8000 -p 5173:5173 -v $(pwd)/teaching/db.sqlite3:/app/teaching/db.sqlite3 teaching-fullstack
```

## 📚 API Documentation

See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for detailed API endpoint documentation.

## 🐛 Troubleshooting

### Container won't start
```bash
# Check logs
docker logs teaching-app

# Rebuild without cache
docker build --no-cache -t teaching-fullstack .
```

### Port conflicts
```bash
# Check what's using the ports
netstat -an | grep :8000
netstat -an | grep :5173

# Use different ports if needed
docker run -d --name teaching-app -p 8001:8000 -p 5174:5173 -v $(pwd)/teaching/db.sqlite3:/app/teaching/db.sqlite3 teaching-fullstack
```

### Database issues
```bash
# Enter the container to debug
docker exec -it teaching-app bash

# Check Django management commands
docker exec -it teaching-app python manage.py shell
```

## 📄 License

MIT License
