@echo off
REM Docker Management Script for Teaching Project (Windows)

if "%1"=="build" (
    echo Building Docker images...
    docker-compose build
) else if "%1"=="up" (
    echo Starting services in production mode...
    docker-compose up -d
) else if "%1"=="dev" (
    echo Starting services in development mode...
    docker-compose -f docker-compose.dev.yml up
) else if "%1"=="dev-build" (
    echo Building and starting services in development mode...
    docker-compose -f docker-compose.dev.yml up --build
) else if "%1"=="down" (
    echo Stopping all services...
    docker-compose down
    docker-compose -f docker-compose.dev.yml down
) else if "%1"=="logs" (
    if "%2"=="" (
        docker-compose logs -f
    ) else (
        docker-compose logs -f %2
    )
) else if "%1"=="shell" (
    if "%2"=="backend" (
        docker-compose exec backend bash
    ) else if "%2"=="frontend" (
        docker-compose exec frontend sh
    ) else (
        echo Usage: %0 shell [backend^|frontend]
    )
) else if "%1"=="migrate" (
    echo Running Django migrations...
    docker-compose exec backend python manage.py migrate
) else if "%1"=="collectstatic" (
    echo Collecting static files...
    docker-compose exec backend python manage.py collectstatic --noinput
) else if "%1"=="superuser" (
    echo Creating Django superuser...
    docker-compose exec backend python manage.py createsuperuser
) else if "%1"=="clean" (
    echo Cleaning up Docker resources...
    docker-compose down -v
    docker system prune -f
) else (
    echo Usage: %0 {build^|up^|dev^|dev-build^|down^|logs^|shell^|migrate^|collectstatic^|superuser^|clean}
    echo.
    echo Commands:
    echo   build         - Build Docker images
    echo   up            - Start services in production mode
    echo   dev           - Start services in development mode
    echo   dev-build     - Build and start services in development mode
    echo   down          - Stop all services
    echo   logs [service] - Show logs (optionally for specific service)
    echo   shell [backend^|frontend] - Open shell in container
    echo   migrate       - Run Django migrations
    echo   collectstatic - Collect Django static files
    echo   superuser     - Create Django superuser
    echo   clean         - Clean up Docker resources
)
