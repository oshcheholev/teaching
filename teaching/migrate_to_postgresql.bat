@echo off
echo ========================================
echo SQLite to PostgreSQL Migration Script
echo ========================================
echo.

REM Check if we're in the right directory
if not exist "manage.py" (
    echo Error: manage.py not found. Please run this from the Django project root.
    pause
    exit /b 1
)

echo Step 1: Creating backup of SQLite data...
C:/projects/django/teaching/env/Scripts/python.exe manage.py dumpdata --indent=2 > sqlite_backup.json
if errorlevel 1 (
    echo Failed to create backup!
    pause
    exit /b 1
)
echo ✓ Backup created: sqlite_backup.json

echo.
echo Step 2: PostgreSQL Setup Required
echo Please make sure PostgreSQL is running and execute these commands in psql:
echo.
echo   CREATE DATABASE teaching_db;
echo   CREATE USER teaching_user WITH PASSWORD 'teaching_password';
echo   GRANT ALL PRIVILEGES ON DATABASE teaching_db TO teaching_user;
echo.
pause

echo Step 3: Running migrations on PostgreSQL...
C:/projects/django/teaching/env/Scripts/python.exe manage.py migrate --settings=teaching.settings_postgresql
if errorlevel 1 (
    echo Failed to run migrations!
    pause
    exit /b 1
)
echo ✓ Migrations completed

echo.
echo Step 4: Loading data into PostgreSQL...
C:/projects/django/teaching/env/Scripts/python.exe manage.py loaddata sqlite_backup.json --settings=teaching.settings_postgresql
if errorlevel 1 (
    echo Failed to load data!
    echo You may need to create a superuser first.
    echo Run: C:/projects/django/teaching/env/Scripts/python.exe manage.py createsuperuser --settings=teaching.settings_postgresql
    pause
    exit /b 1
)
echo ✓ Data loaded successfully

echo.
echo ========================================
echo Migration completed successfully!
echo ========================================
echo.
echo Next steps:
echo 1. Test your application with PostgreSQL settings
echo 2. Update your main settings.py if everything works
echo 3. Keep sqlite_backup.json as a backup
echo.
echo To test: C:/projects/django/teaching/env/Scripts/python.exe manage.py runserver --settings=teaching.settings_postgresql
echo.
pause
