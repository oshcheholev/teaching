# Multi-stage Dockerfile for both Frontend and Backend

# Stage 1: Build React Frontend
FROM node:18-alpine AS frontend-build
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# Stage 2: Django Backend with built frontend
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        python3-dev \
        sqlite3 \
        nginx \
        supervisor \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy Django project
COPY . /app/

# Copy built frontend from previous stage
COPY --from=frontend-build /app/frontend/dist /app/frontend/dist

# Set work directory to Django project
WORKDIR /app/teaching

# Set proper permissions for SQLite database
RUN chmod 664 /app/teaching/db.sqlite3

# Collect static files
RUN python manage.py collectstatic --noinput

# Create nginx configuration
RUN echo 'server { \
    listen 5173; \
    server_name localhost; \
    \
    # Frontend (React) \
    location / { \
        root /app/frontend/dist; \
        try_files $uri $uri/ /index.html; \
        index index.html; \
    } \
    \
    # Backend API proxy (for frontend to access backend) \
    location /api/ { \
        proxy_pass http://localhost:8000; \
        proxy_set_header Host $host; \
        proxy_set_header X-Real-IP $remote_addr; \
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; \
        proxy_set_header X-Forwarded-Proto $scheme; \
    } \
    \
    # Django admin proxy \
    location /admin/ { \
        proxy_pass http://localhost:8000; \
        proxy_set_header Host $host; \
        proxy_set_header X-Real-IP $remote_addr; \
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; \
        proxy_set_header X-Forwarded-Proto $scheme; \
    } \
    \
    # Django static files proxy \
    location /static/ { \
        proxy_pass http://localhost:8000; \
        proxy_set_header Host $host; \
    } \
}' > /etc/nginx/sites-available/default

# Create supervisor configuration
RUN echo '[supervisord]' > /etc/supervisor/conf.d/supervisord.conf && \
    echo 'nodaemon=true' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo '' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo '[program:django]' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo 'command=python manage.py runserver 0.0.0.0:8000' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo 'directory=/app/teaching' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo 'autostart=true' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo 'autorestart=true' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo 'stderr_logfile=/var/log/django.err.log' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo 'stdout_logfile=/var/log/django.out.log' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo '' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo '[program:nginx]' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo 'command=/usr/sbin/nginx -g "daemon off;"' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo 'autostart=true' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo 'autorestart=true' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo 'stderr_logfile=/var/log/nginx.err.log' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo 'stdout_logfile=/var/log/nginx.out.log' >> /etc/supervisor/conf.d/supervisord.conf

# Expose both ports: 8000 for Django backend, 5173 for frontend
EXPOSE 8000 5173

# Start supervisor (which starts both Django and Nginx)
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
