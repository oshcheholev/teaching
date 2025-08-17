# Teaching Platform API Documentation

## Overview

This is the test implementation of Teaching App of University of Applied Arts Vienna
The Teaching Platform API provides comprehensive access to course management functionality for the University of Applied Arts Vienna. This RESTful API supports both public course browsing and administrative operations.

**Base URL:** `http://localhost:8000/api/`  
**Version:** 1.0  
**Authentication:** JWT Bearer Token (for admin endpoints)  

## Table of Contents

1. [Authentication](#authentication)
2. [Course Management](#course-management)
3. [Teacher Management](#teacher-management)
4. [Course Types](#course-types)
5. [Study Programs](#study-programs)
6. [Departments](#departments)
7. [Institutes](#institutes)
8. [Admin Management](#admin-management)
9. [Data Models](#data-models)
10. [Error Handling](#error-handling)
11. [Rate Limiting](#rate-limiting)

## Authentication

### Admin Login
```http
POST /api/auth/admin-login/
```

**Request Body:**
```json
{
    "username": "admin_username",
    "password": "admin_password"
}
```

**Success Response (200):**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com",
        "is_staff": true,
        "is_superuser": true
    }
}
```

### User Registration
```http
POST /api/auth/register/
```

**Request Body:**
```json
{
    "username": "new_user",
    "email": "user@example.com",
    "password": "secure_password"
}
```

### Check Admin Status
```http
GET /api/auth/check-admin/
Authorization: Bearer {access_token}
```

### User Profile
```http
GET /api/auth/profile/
Authorization: Bearer {access_token}
```

## Course Management

### List Courses
```http
GET /api/courses/
```

**Query Parameters:**
- `gender_diversity` (boolean): Filter by gender diversity (true/false)
- `teacher` (integer): Filter by teacher ID
- `type` (integer): Filter by course type ID
- `institute` (integer): Filter by institute ID
- `department` (integer): Filter by department ID
- `study_program` (integer): Filter by study program ID

**Example:**
```http
GET /api/courses/?gender_diversity=true&teacher=1&type=2
```

**Success Response (200):**
```json
[
    {
        "id": 1,
        "title": "Advanced Digital Media",
        "description": "Comprehensive course on digital media techniques...",
        "type": {
            "id": 2,
            "name": "Practical Course",
            "description": "Hands-on practical training"
        },
        "semester": "WS",
        "year": 2024,
        "start_date": "2024-10-01",
        "end_date": "2025-01-31",
        "teacher": {
            "id": 1,
            "name": "Prof. Maria Schmidt",
            "email": "m.schmidt@uni-ak.ac.at",
            "subject": "Digital Media"
        },
        "credits": 6,
        "gender_diversity": true,
        "institute": {
            "id": 1,
            "name": "Institute for Applied Arts",
            "description": "Primary institute for applied arts education"
        },
        "department": {
            "id": 1,
            "name": "Digital Arts",
            "institute": 1
        },
        "study_program": {
            "id": 1,
            "name": "Digital Arts Bachelor",
            "description": "Bachelor program in digital arts",
            "department": 1,
            "year": 3
        }
    }
]
```

### Get Course Details
```http
GET /api/courses/{id}/
```

### Create Course (Admin Only)
```http
POST /api/courses/add/
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
    "title": "New Course Title",
    "description": "Course description",
    "type": 1,
    "semester": "WS",
    "year": 2024,
    "start_date": "2024-10-01",
    "end_date": "2025-01-31",
    "teacher": 1,
    "credits": 6,
    "gender_diversity": false,
    "institute": 1,
    "department": 1,
    "study_program": 1
}
```

### Update Course (Admin Only)
```http
PUT /api/courses/{id}/update/
Authorization: Bearer {access_token}
```

### Delete Course (Admin Only)
```http
DELETE /api/courses/{id}/delete/
Authorization: Bearer {access_token}
```

## Teacher Management

### List Teachers
```http
GET /api/teachers/
```

**Query Parameters:**
- `subject` (string): Filter by subject (case-insensitive partial match)

**Example:**
```http
GET /api/teachers/?subject=digital
```

**Success Response (200):**
```json
[
    {
        "id": 1,
        "name": "Prof. Maria Schmidt",
        "email": "m.schmidt@uni-ak.ac.at",
        "subject": "Digital Media"
    }
]
```

### Get Teacher Details
```http
GET /api/teachers/{id}/
```

### Create Teacher (Admin Only)
```http
POST /api/teachers/add/
Authorization: Bearer {access_token}
```

### Update Teacher (Admin Only)
```http
PUT /api/teachers/{id}/update/
Authorization: Bearer {access_token}
```

### Delete Teacher (Admin Only)
```http
DELETE /api/teachers/{id}/delete/
Authorization: Bearer {access_token}
```

## Course Types

### List Course Types
```http
GET /api/course-types/
```

**Success Response (200):**
```json
[
    {
        "id": 1,
        "name": "Lecture",
        "description": "Traditional lecture format"
    },
    {
        "id": 2,
        "name": "Practical Course",
        "description": "Hands-on practical training"
    }
]
```

### CRUD Operations (Admin Only)
- `GET /api/course-types/{id}/` - Get details
- `POST /api/course-types/add/` - Create
- `PUT /api/course-types/{id}/update/` - Update
- `DELETE /api/course-types/{id}/delete/` - Delete

## Study Programs

### List Study Programs
```http
GET /api/study-programs/
```

**Success Response (200):**
```json
[
    {
        "id": 1,
        "name": "Digital Arts Bachelor",
        "description": "Bachelor program in digital arts",
        "department": {
            "id": 1,
            "name": "Digital Arts",
            "institute": {
                "id": 1,
                "name": "Institute for Applied Arts"
            }
        },
        "year": 3
    }
]
```

### CRUD Operations (Admin Only)
- `GET /api/study-programs/{id}/` - Get details
- `POST /api/study-programs/add/` - Create
- `PUT /api/study-programs/{id}/update/` - Update
- `DELETE /api/study-programs/{id}/delete/` - Delete

## Departments

### List Departments
```http
GET /api/departments/
```

**Success Response (200):**
```json
[
    {
        "id": 1,
        "name": "Digital Arts",
        "institute": {
            "id": 1,
            "name": "Institute for Applied Arts",
            "description": "Primary institute for applied arts education"
        }
    }
]
```

### CRUD Operations (Admin Only)
- `GET /api/departments/{id}/` - Get details
- `POST /api/departments/add/` - Create
- `PUT /api/departments/{id}/update/` - Update
- `DELETE /api/departments/{id}/delete/` - Delete

## Institutes

### List Institutes
```http
GET /api/institutes/
```

**Success Response (200):**
```json
[
    {
        "id": 1,
        "name": "Institute for Applied Arts",
        "description": "Primary institute for applied arts education"
    }
]
```

### CRUD Operations (Admin Only)
- `GET /api/institutes/{id}/` - Get details
- `POST /api/institutes/add/` - Create
- `PUT /api/institutes/{id}/update/` - Update
- `DELETE /api/institutes/{id}/delete/` - Delete

## Admin Management

### List Users (Admin Only)
```http
GET /api/admin/users/
Authorization: Bearer {access_token}
```

### User Details (Admin Only)
```http
GET /api/admin/users/{id}/
Authorization: Bearer {access_token}
```

## Data Models

### Course Model
```json
{
    "id": "integer (auto-generated)",
    "title": "string (max 100 chars) - required",
    "description": "text - required",
    "type": "foreign key to CourseType - optional",
    "semester": "string (max 20 chars) - required",
    "year": "integer - required",
    "start_date": "date (YYYY-MM-DD) - required",
    "end_date": "date (YYYY-MM-DD) - required",
    "teacher": "foreign key to Teacher - optional",
    "credits": "integer - required",
    "gender_diversity": "boolean (default: false)",
    "institute": "foreign key to Institute - optional",
    "department": "foreign key to Department - optional",
    "study_program": "foreign key to StudyProgram - optional"
}
```

### Teacher Model
```json
{
    "id": "integer (auto-generated)",
    "name": "string (max 100 chars) - required",
    "email": "email (unique) - required",
    "subject": "string (max 100 chars) - required"
}
```

### CourseType Model
```json
{
    "id": "integer (auto-generated)",
    "name": "string (max 50 chars) - required",
    "description": "text - required"
}
```

### StudyProgram Model
```json
{
    "id": "integer (auto-generated)",
    "name": "string (max 100 chars) - required",
    "description": "text - required",
    "department": "foreign key to Department - required",
    "year": "integer - required"
}
```

### Department Model
```json
{
    "id": "integer (auto-generated)",
    "name": "string (max 100 chars) - required",
    "institute": "foreign key to Institute - required"
}
```

### Institute Model
```json
{
    "id": "integer (auto-generated)",
    "name": "string (max 100 chars) - required",
    "description": "text - required"
}
```

## Error Handling

### Standard HTTP Status Codes

- **200 OK** - Request successful
- **201 Created** - Resource created successfully
- **400 Bad Request** - Invalid request data
- **401 Unauthorized** - Authentication required or invalid
- **403 Forbidden** - Insufficient permissions
- **404 Not Found** - Resource not found
- **405 Method Not Allowed** - HTTP method not supported
- **500 Internal Server Error** - Server error

### Error Response Format

```json
{
    "error": "Error message description",
    "detail": "Detailed error information",
    "field_errors": {
        "field_name": ["Field-specific error message"]
    }
}
```

### Common Error Examples

**400 Bad Request - Field Validation:**
```json
{
    "title": ["This field is required."],
    "year": ["Ensure this value is greater than 1900."],
    "email": ["Enter a valid email address."]
}
```

**401 Unauthorized:**
```json
{
    "detail": "Given token not valid for any token type",
    "code": "token_not_valid",
    "messages": [
        {
            "token_class": "AccessToken",
            "token_type": "access",
            "message": "Token is invalid or expired"
        }
    ]
}
```

## Rate Limiting

Currently, no rate limiting is implemented. For production deployment, consider implementing rate limiting based on:
- IP address for public endpoints
- User account for authenticated endpoints
- Stricter limits for admin operations

## Authentication Headers

For protected endpoints, include the JWT token in the Authorization header:

```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

## Filtering and Search

### Course Filtering
Combine multiple query parameters for complex filtering:

```http
GET /api/courses/?gender_diversity=true&year=2024&institute=1&department=2
```

### Teacher Search
Search teachers by subject (case-insensitive):

```http
GET /api/teachers/?subject=digital
```

## Data Relationships

### Hierarchical Structure
```
Institute
└── Department
    ├── StudyProgram
    └── Course (via department)
        ├── Teacher
        └── CourseType
```

### Foreign Key Relationships
- **Course** can belong to Institute, Department, StudyProgram, Teacher, CourseType
- **StudyProgram** belongs to Department
- **Department** belongs to Institute
- **Teacher** is independent but can teach multiple courses

## Sample Data

The API includes real course data from the University of Applied Arts Vienna, including:
- 20+ actual courses from various departments
- Real teacher profiles
- Authentic institute and department structure
- Diverse course types (Lectures, Practical Courses, Seminars, etc.)

## Development Notes

### Database
- **Development:** SQLite (db.sqlite3)
- **Production:** PostgreSQL (migration tools provided)

### Authentication
- **JWT tokens** with 60-minute access token lifetime
- **Refresh tokens** with 1-day lifetime
- **Admin-only endpoints** require `is_staff=True`

### CORS
- Configured for frontend development on `localhost:3000`
- Adjust `CORS_ALLOWED_ORIGINS` for production

## Support

For API support or questions, contact the development team or refer to the Django admin interface at `/admin/` for data management.
