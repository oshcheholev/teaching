#!/bin/bash

# Docker Management Script for Teaching Project

set -e

case "$1" in
    "build")
        echo "Building Docker images..."
        docker-compose build
        ;;
    "up")
        echo "Starting services in production mode..."
        docker-compose up -d
        ;;
    "dev")
        echo "Starting services in development mode..."
        docker-compose -f docker-compose.dev.yml up
        ;;
    "dev-build")
        echo "Building and starting services in development mode..."
        docker-compose -f docker-compose.dev.yml up --build
        ;;
    "down")
        echo "Stopping all services..."
        docker-compose down
        docker-compose -f docker-compose.dev.yml down
        ;;
    "logs")
        if [ -z "$2" ]; then
            docker-compose logs -f
        else
            docker-compose logs -f "$2"
        fi
        ;;
    "shell")
        if [ "$2" = "backend" ]; then
            docker-compose exec backend bash
        elif [ "$2" = "frontend" ]; then
            docker-compose exec frontend sh
        else
            echo "Usage: $0 shell [backend|frontend]"
        fi
        ;;
    "migrate")
        echo "Running Django migrations..."
        docker-compose exec backend python manage.py migrate
        ;;
    "collectstatic")
        echo "Collecting static files..."
        docker-compose exec backend python manage.py collectstatic --noinput
        ;;
    "superuser")
        echo "Creating Django superuser..."
        docker-compose exec backend python manage.py createsuperuser
        ;;
    "clean")
        echo "Cleaning up Docker resources..."
        docker-compose down -v
        docker system prune -f
        ;;
    *)
        echo "Usage: $0 {build|up|dev|dev-build|down|logs|shell|migrate|collectstatic|superuser|clean}"
        echo ""
        echo "Commands:"
        echo "  build         - Build Docker images"
        echo "  up            - Start services in production mode"
        echo "  dev           - Start services in development mode"
        echo "  dev-build     - Build and start services in development mode"
        echo "  down          - Stop all services"
        echo "  logs [service] - Show logs (optionally for specific service)"
        echo "  shell [backend|frontend] - Open shell in container"
        echo "  migrate       - Run Django migrations"
        echo "  collectstatic - Collect Django static files"
        echo "  superuser     - Create Django superuser"
        echo "  clean         - Clean up Docker resources"
        exit 1
        ;;
esac
