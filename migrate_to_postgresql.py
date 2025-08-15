#!/usr/bin/env python
"""
SQLite to PostgreSQL Migration Script for Teaching Platform
"""

import os
import sys
import django
import subprocess
import json
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).resolve().parent
sys.path.append(str(project_root))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teaching.settings')
django.setup()

from django.core.management import execute_from_command_line
from django.db import connection
from django.conf import settings

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔧 {description}")
    print(f"Running: {' '.join(command)}")
    
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"✅ Success: {description}")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {description}")
        print(f"Command failed: {e}")
        if e.stdout:
            print(f"STDOUT: {e.stdout}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        return False

def backup_sqlite_data():
    """Create a backup of SQLite data"""
    print("\n📦 Creating SQLite backup...")
    
    backup_file = project_root / "sqlite_backup.json"
    
    try:
        execute_from_command_line(['manage.py', 'dumpdata', '--indent=2', '--output', str(backup_file)])
        print(f"✅ SQLite data backed up to: {backup_file}")
        return backup_file
    except Exception as e:
        print(f"❌ Failed to backup SQLite data: {e}")
        return None

def setup_postgresql_settings():
    """Create PostgreSQL settings file"""
    print("\n⚙️ Setting up PostgreSQL configuration...")
    
    settings_content = '''"""
PostgreSQL settings for teaching project.
"""

import os
from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-4rn=(q3_7)@)m=z(o97*3=*klc7_wkw!uouofdy92+n#_07b1+')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True').lower() in ('true', '1', 'yes')

ALLOWED_HOSTS = ['*']

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'api',
    'rest_framework_simplejwt',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'teaching.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'teaching.wsgi.application'

# Database - PostgreSQL Configuration
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

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]

CORS_ALLOW_CREDENTIALS = True
'''
    
    settings_file = project_root / "teaching" / "settings_postgresql.py"
    with open(settings_file, 'w') as f:
        f.write(settings_content)
    
    print(f"✅ PostgreSQL settings created: {settings_file}")
    return settings_file

def migrate_to_postgresql():
    """Migrate data from SQLite to PostgreSQL"""
    print("\n🚀 Starting migration to PostgreSQL...")
    
    # Step 1: Backup SQLite data
    backup_file = backup_sqlite_data()
    if not backup_file:
        return False
    
    # Step 2: Create PostgreSQL settings
    setup_postgresql_settings()
    
    # Step 3: Set environment for PostgreSQL
    os.environ['DJANGO_SETTINGS_MODULE'] = 'teaching.settings_postgresql'
    
    print("\n📋 Migration Steps:")
    print("1. Make sure PostgreSQL is running on localhost:5432")
    print("2. Database: teaching_db")
    print("3. User: teaching_user")
    print("4. Password: teaching_password")
    print("\nTo create the database, run these PostgreSQL commands:")
    print("CREATE DATABASE teaching_db;")
    print("CREATE USER teaching_user WITH PASSWORD 'teaching_password';")
    print("GRANT ALL PRIVILEGES ON DATABASE teaching_db TO teaching_user;")
    print("\\q")
    
    input("\nPress Enter when PostgreSQL is ready...")
    
    # Step 4: Run migrations on PostgreSQL
    print("\n🔄 Running migrations on PostgreSQL...")
    if not run_command(['python', 'manage.py', 'migrate', '--settings=teaching.settings_postgresql'], 
                      "Running PostgreSQL migrations"):
        return False
    
    # Step 5: Load data into PostgreSQL
    print("\n📥 Loading data into PostgreSQL...")
    if not run_command(['python', 'manage.py', 'loaddata', str(backup_file), '--settings=teaching.settings_postgresql'], 
                      "Loading data into PostgreSQL"):
        return False
    
    print("\n✅ Migration completed successfully!")
    print(f"📊 Data migrated from SQLite to PostgreSQL")
    print(f"🗄️ Backup saved at: {backup_file}")
    
    return True

if __name__ == "__main__":
    print("🔄 SQLite to PostgreSQL Migration Tool")
    print("=====================================")
    
    # Check if we're in the right directory
    if not (project_root / "manage.py").exists():
        print("❌ Error: manage.py not found. Please run this script from the Django project root.")
        sys.exit(1)
    
    # Run migration
    success = migrate_to_postgresql()
    
    if success:
        print("\n🎉 Migration completed successfully!")
        print("\nNext steps:")
        print("1. Update your settings.py to use PostgreSQL")
        print("2. Test your application")
        print("3. Update environment variables for production")
    else:
        print("\n❌ Migration failed. Please check the errors above.")
        sys.exit(1)
