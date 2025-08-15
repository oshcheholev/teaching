# SQLite to PostgreSQL Migration Guide

This guide will help you migrate your existing SQLite database to PostgreSQL.

## Prerequisites

1. **Install PostgreSQL** (if not already installed):
   - Windows: Download from https://www.postgresql.org/download/windows/
   - Mac: `brew install postgresql`
   - Linux: `sudo apt-get install postgresql postgresql-contrib`

2. **Install required Python packages**:
   ```bash
   pip install psycopg2-binary dj-database-url
   ```

## Step 1: Backup Your SQLite Data

```bash
cd c:\projects\django\teaching\teaching
C:/projects/django/teaching/env/Scripts/python.exe manage.py dumpdata --indent=2 > sqlite_backup.json
```

## Step 2: Setup PostgreSQL Database

1. **Start PostgreSQL service**:
   - Windows: Use pgAdmin or start from Services
   - Mac/Linux: `sudo service postgresql start`

2. **Create database and user**:
   ```sql
   -- Connect as postgres user
   psql -U postgres

   -- Create database
   CREATE DATABASE teaching_db;

   -- Create user
   CREATE USER teaching_user WITH PASSWORD 'teaching_password';

   -- Grant privileges
   GRANT ALL PRIVILEGES ON DATABASE teaching_db TO teaching_user;

   -- Exit
   \q
   ```

## Step 3: Update Django Settings

Create a new settings file for PostgreSQL:

```python
# teaching/settings_postgresql.py
from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'teaching_db',
        'USER': 'teaching_user',
        'PASSWORD': 'teaching_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Step 4: Run Migrations

```bash
# Run migrations on PostgreSQL
C:/projects/django/teaching/env/Scripts/python.exe manage.py migrate --settings=teaching.settings_postgresql

# Load your data
C:/projects/django/teaching/env/Scripts/python.exe manage.py loaddata sqlite_backup.json --settings=teaching.settings_postgresql
```

## Step 5: Update Your Main Settings

Once everything works, update your main `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'teaching_db',
        'USER': 'teaching_user',
        'PASSWORD': 'teaching_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Step 6: Test Your Application

```bash
C:/projects/django/teaching/env/Scripts/python.exe manage.py runserver
```

## Environment Variables (Recommended)

For production, use environment variables:

```python
import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'teaching_db'),
        'USER': os.environ.get('DB_USER', 'teaching_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'teaching_password'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
```

## Troubleshooting

1. **Connection refused**: Make sure PostgreSQL is running
2. **Authentication failed**: Check username/password
3. **Database doesn't exist**: Make sure you created the database
4. **Permission denied**: Grant proper privileges to the user

## Docker Alternative

If you prefer using Docker for PostgreSQL:

```bash
# Start PostgreSQL container
docker run --name postgres-teaching -e POSTGRES_DB=teaching_db -e POSTGRES_USER=teaching_user -e POSTGRES_PASSWORD=teaching_password -p 5432:5432 -d postgres:15

# Then follow steps 4-6 above
```

## Rollback Plan

If something goes wrong, you can always go back to SQLite:

1. Restore your original `settings.py`
2. Your SQLite database is still at `teaching/db.sqlite3`
3. Your backup is at `sqlite_backup.json`
