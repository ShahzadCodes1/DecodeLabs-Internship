# 🎓 Student Management System API

A production-ready RESTful API built with **Python Django REST Framework** for managing student records. Demonstrates complete CRUD operations, data validation, error handling, pagination, search, and filtering.

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Running the Server](#running-the-server)
- [API Endpoints](#api-endpoints)
- [Example Requests & Responses](#example-requests--responses)
- [Validation Rules](#validation-rules)
- [Error Handling](#error-handling)
- [HTTP Status Codes](#http-status-codes)
- [Testing](#testing)
- [Postman Testing Guide](#postman-testing-guide)
- [GitHub Repository Structure](#github-repository-structure)

---

## 📖 Project Overview

The Student Management System API allows you to:
- Create, read, update, and delete student records
- Search students by name, email, or course
- Filter students by course
- Paginate results for large datasets
- Validate all incoming data with meaningful error messages

**Base URL:** `http://127.0.0.1:8000`  
**API Prefix:** `/api/`

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **CRUD Operations** | Create, Read, Update, Delete students |
| **Partial Updates** | PATCH endpoint updates only provided fields |
| **Data Validation** | Name, email (unique), phone format, course required |
| **Error Handling** | 400, 404, 500 with descriptive messages |
| **Pagination** | Configurable page size via query params |
| **Search** | Search across name, email, and course |
| **Filtering** | Filter list by course name |
| **Logging** | Console and file logging for all actions |
| **Django Admin** | Web-based admin panel for data management |
| **Automated Tests** | 16 test cases covering all endpoints |

---

## 🛠 Technologies Used

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.12+ | Programming language |
| Django | 5.0.6 | Web framework |
| Django REST Framework | 3.15.2 | REST API toolkit |
| django-filter | 24.2 | Query filtering |
| SQLite | Built-in | Database (development) |

---

## 📁 Project Structure

```
student_management_api/              ← Root project folder
│
├── manage.py                        ← Django management CLI tool
├── requirements.txt                 ← Python dependencies
├── .gitignore                       ← Git ignore rules
├── README.md                        ← This file
├── db.sqlite3                       ← SQLite database (auto-created)
│
├── student_management_api/          ← Django project config package
│   ├── __init__.py
│   ├── settings.py                  ← All project settings
│   ├── urls.py                      ← Main URL router
│   ├── wsgi.py                      ← WSGI entry point (production)
│   └── asgi.py                      ← ASGI entry point (async)
│
└── students/                        ← Students app
    ├── __init__.py
    ├── apps.py                      ← App configuration
    ├── models.py                    ← Student database model
    ├── serializers.py               ← Data validation & serialization
    ├── views.py                     ← API view logic
    ├── urls.py                      ← App URL routes
    ├── admin.py                     ← Admin panel config
    ├── test_models.py               ← Model unit tests
    ├── test_views.py                ← API endpoint tests
    └── migrations/                  ← Database migration files
        ├── __init__.py
        └── 0001_initial.py          ← Initial schema migration
```

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/student-management-api.git
cd student-management-api
```

### Step 2: Create a Virtual Environment

A virtual environment isolates your project's dependencies from other Python projects.

```bash
# Create the virtual environment
python -m venv venv

# Activate it:
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

# You'll see (venv) in your terminal prompt when it's active
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Apply Database Migrations

Migrations create the database tables based on your models.

```bash
python manage.py makemigrations
python manage.py migrate
```

Expected output:
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, students
Running migrations:
  Applying students.0001_initial... OK
```

### Step 5: Create a Superuser (Optional)

This allows you to access the Django admin panel at `/admin/`.

```bash
python manage.py createsuperuser
# Follow the prompts to set username, email, and password
```

---

## 🚀 Running the Server

```bash
python manage.py runserver
```

Server will start at: **http://127.0.0.1:8000**

You'll see:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health/` | API health check |
| `GET` | `/api/students/` | Get all students (paginated) |
| `POST` | `/api/students/` | Create a new student |
| `GET` | `/api/students/<id>/` | Get student by ID |
| `PUT` | `/api/students/<id>/` | Full update of a student |
| `PATCH` | `/api/students/<id>/` | Partial update of a student |
| `DELETE` | `/api/students/<id>/` | Delete a student |
| `GET` | `/api/students/search/` | Search students |

### Query Parameters

| Endpoint | Parameter | Example | Description |
|----------|-----------|---------|-------------|
| `/api/students/` | `search` | `?search=john` | Search across name, email, course |
| `/api/students/` | `course` | `?course=Engineering` | Filter by course |
| `/api/students/` | `page` | `?page=2` | Go to page 2 |
| `/api/students/` | `page_size` | `?page_size=5` | 5 results per page |
| `/api/students/search/` | `name` | `?name=alice` | Search by name |
| `/api/students/search/` | `course` | `?course=CS` | Search by course |
| `/api/students/search/` | `email` | `?email=@gmail` | Search by email |

---

## 📝 Example Requests & Responses

### 1. Health Check

**Request:**
```
GET http://127.0.0.1:8000/api/health/
```

**Response (200 OK):**
```json
{
    "success": true,
    "message": "Student Management API is running.",
    "version": "1.0.0",
    "endpoints": {
        "list_students": "GET /api/students/",
        "create_student": "POST /api/students/",
        "get_student": "GET /api/students/<id>/",
        "update_student": "PUT /api/students/<id>/",
        "partial_update": "PATCH /api/students/<id>/",
        "delete_student": "DELETE /api/students/<id>/",
        "search_students": "GET /api/students/search/",
        "health_check": "GET /api/health/"
    }
}
```

---

### 2. Create a Student

**Request:**
```
POST http://127.0.0.1:8000/api/students/
Content-Type: application/json

{
    "name": "Alice Johnson",
    "email": "alice.johnson@example.com",
    "phone": "+1234567890",
    "course": "Computer Science"
}
```

**Response (201 Created):**
```json
{
    "success": true,
    "message": "Student created successfully.",
    "data": {
        "id": 1,
        "name": "Alice Johnson",
        "email": "alice.johnson@example.com",
        "phone": "+1234567890",
        "course": "Computer Science",
        "created_at": "2024-01-15T10:30:00.123456Z",
        "updated_at": "2024-01-15T10:30:00.123456Z"
    }
}
```

---

### 3. Get All Students

**Request:**
```
GET http://127.0.0.1:8000/api/students/
```

**Response (200 OK):**
```json
{
    "success": true,
    "message": "Students retrieved successfully.",
    "count": 25,
    "total_pages": 3,
    "current_page": 1,
    "next": "http://127.0.0.1:8000/api/students/?page=2",
    "previous": null,
    "data": [
        {
            "id": 1,
            "name": "Alice Johnson",
            "email": "alice.johnson@example.com",
            "course": "Computer Science",
            "created_at": "2024-01-15T10:30:00.123456Z"
        }
    ]
}
```

---

### 4. Get Student by ID

**Request:**
```
GET http://127.0.0.1:8000/api/students/1/
```

**Response (200 OK):**
```json
{
    "success": true,
    "message": "Student retrieved successfully.",
    "data": {
        "id": 1,
        "name": "Alice Johnson",
        "email": "alice.johnson@example.com",
        "phone": "+1234567890",
        "course": "Computer Science",
        "created_at": "2024-01-15T10:30:00.123456Z",
        "updated_at": "2024-01-15T10:30:00.123456Z"
    }
}
```

---

### 5. Full Update (PUT)

**Request:**
```
PUT http://127.0.0.1:8000/api/students/1/
Content-Type: application/json

{
    "name": "Alice Smith",
    "email": "alice.smith@example.com",
    "phone": "+9876543210",
    "course": "Data Science"
}
```

**Response (200 OK):**
```json
{
    "success": true,
    "message": "Student updated successfully.",
    "data": {
        "id": 1,
        "name": "Alice Smith",
        "email": "alice.smith@example.com",
        "phone": "+9876543210",
        "course": "Data Science",
        "created_at": "2024-01-15T10:30:00.123456Z",
        "updated_at": "2024-01-15T11:00:00.654321Z"
    }
}
```

---

### 6. Partial Update (PATCH)

**Request:**
```
PATCH http://127.0.0.1:8000/api/students/1/
Content-Type: application/json

{
    "course": "Machine Learning"
}
```

**Response (200 OK):**
```json
{
    "success": true,
    "message": "Student partially updated successfully.",
    "data": {
        "id": 1,
        "name": "Alice Smith",
        "email": "alice.smith@example.com",
        "phone": "+9876543210",
        "course": "Machine Learning",
        "created_at": "2024-01-15T10:30:00.123456Z",
        "updated_at": "2024-01-15T11:15:00.789012Z"
    }
}
```

---

### 7. Delete a Student

**Request:**
```
DELETE http://127.0.0.1:8000/api/students/1/
```

**Response (200 OK):**
```json
{
    "success": true,
    "message": "Student 'Alice Smith' (ID: 1) deleted successfully.",
    "data": null
}
```

---

### 8. Search Students (BONUS)

**Request:**
```
GET http://127.0.0.1:8000/api/students/search/?name=alice&course=science
```

**Response (200 OK):**
```json
{
    "success": true,
    "message": "Found 2 student(s) matching your search.",
    "count": 2,
    "total_pages": 1,
    "current_page": 1,
    "next": null,
    "previous": null,
    "data": [...]
}
```

---

## ✅ Validation Rules

| Field | Required | Rules |
|-------|----------|-------|
| `name` | ✅ Yes | Min 2 chars, max 100. Letters, spaces, hyphens, apostrophes only. |
| `email` | ✅ Yes | Valid email format. Must be unique across all students. |
| `phone` | ❌ No | If provided: 7-15 digits, can start with +. |
| `course` | ✅ Yes | Min 2 chars, max 100. |

---

## ❌ Error Handling Examples

### 400 Bad Request — Validation Error

```json
{
    "success": false,
    "error": "Validation Error",
    "message": "Please fix the errors below.",
    "errors": {
        "name": ["Name cannot be empty or whitespace."],
        "email": ["A student with this email address already exists."]
    },
    "data": null
}
```

### 404 Not Found

```json
{
    "success": false,
    "error": "Not Found",
    "message": "Student with ID 9999 does not exist.",
    "data": null
}
```

### 500 Internal Server Error

```json
{
    "success": false,
    "error": "Internal Server Error",
    "message": "An unexpected error occurred while retrieving students.",
    "data": null
}
```

---

## 📊 HTTP Status Codes Used

| Code | Meaning | When Used |
|------|---------|-----------|
| `200 OK` | Success | GET, PUT, PATCH, DELETE |
| `201 Created` | Resource created | POST (create student) |
| `400 Bad Request` | Validation error | Invalid/missing data |
| `404 Not Found` | Resource missing | Student ID doesn't exist |
| `500 Internal Server Error` | Server error | Unexpected exceptions |

---

## 🧪 Testing

Run all tests:
```bash
python manage.py test students
```

Run specific test file:
```bash
python manage.py test students.test_views
python manage.py test students.test_models
```

Expected output:
```
Found 16 test(s).
......
Ran 16 tests in 0.084s
OK
```

---

## 🔬 Postman Testing Guide

### Setup

1. Download and install [Postman](https://www.postman.com/downloads/)
2. Make sure your Django server is running: `python manage.py runserver`
3. Open Postman and create a new Collection called "Student Management API"

### How to Set Headers

For POST, PUT, PATCH requests, always set:
- **Header:** `Content-Type` → `application/json`

### Test Sequence

Follow this order to test all endpoints:

#### Step 1: Health Check
- **Method:** GET
- **URL:** `http://127.0.0.1:8000/api/health/`
- **Expected:** 200 OK

#### Step 2: Create Students (run 3-4 times with different data)
- **Method:** POST
- **URL:** `http://127.0.0.1:8000/api/students/`
- **Body (raw JSON):**
```json
{
    "name": "John Doe",
    "email": "john.doe@example.com",
    "phone": "+1234567890",
    "course": "Computer Science"
}
```
- **Expected:** 201 Created

#### Step 3: Get All Students
- **Method:** GET
- **URL:** `http://127.0.0.1:8000/api/students/`
- **Expected:** 200 OK with list

#### Step 4: Get Student by ID
- **Method:** GET
- **URL:** `http://127.0.0.1:8000/api/students/1/`
- **Expected:** 200 OK

#### Step 5: Update Student (Full)
- **Method:** PUT
- **URL:** `http://127.0.0.1:8000/api/students/1/`
- **Body:**
```json
{
    "name": "John Updated",
    "email": "john.updated@example.com",
    "course": "Data Science"
}
```
- **Expected:** 200 OK

#### Step 6: Update Student (Partial)
- **Method:** PATCH
- **URL:** `http://127.0.0.1:8000/api/students/1/`
- **Body:**
```json
{
    "course": "Machine Learning"
}
```
- **Expected:** 200 OK

#### Step 7: Test Validation Error
- **Method:** POST
- **URL:** `http://127.0.0.1:8000/api/students/`
- **Body:** (send same email as an existing student)
```json
{
    "name": "Duplicate",
    "email": "john.updated@example.com",
    "course": "Any Course"
}
```
- **Expected:** 400 Bad Request

#### Step 8: Test 404 Not Found
- **Method:** GET
- **URL:** `http://127.0.0.1:8000/api/students/9999/`
- **Expected:** 404 Not Found

#### Step 9: Search Students
- **Method:** GET
- **URL:** `http://127.0.0.1:8000/api/students/search/?name=john`
- **Expected:** 200 OK with filtered results

#### Step 10: Pagination
- **Method:** GET
- **URL:** `http://127.0.0.1:8000/api/students/?page=1&page_size=2`
- **Expected:** 200 OK with max 2 results

#### Step 11: Delete Student
- **Method:** DELETE
- **URL:** `http://127.0.0.1:8000/api/students/1/`
- **Expected:** 200 OK

#### Step 12: Verify Deletion
- **Method:** GET
- **URL:** `http://127.0.0.1:8000/api/students/1/`
- **Expected:** 404 Not Found ✅

---

## 📦 GitHub Repository Structure

When you push to GitHub, your repository will look like this:

```
📁 student-management-api
├── 📄 README.md          ← Main documentation
├── 📄 requirements.txt   ← Dependencies
├── 📄 .gitignore         ← Ignored files
├── 📄 manage.py          ← Django CLI
│
├── 📁 student_management_api/
│   ├── 📄 settings.py
│   ├── 📄 urls.py
│   ├── 📄 wsgi.py
│   └── 📄 asgi.py
│
└── 📁 students/
    ├── 📄 models.py
    ├── 📄 serializers.py
    ├── 📄 views.py
    ├── 📄 urls.py
    ├── 📄 admin.py
    ├── 📄 apps.py
    ├── 📄 test_models.py
    ├── 📄 test_views.py
    └── 📁 migrations/
        └── 📄 0001_initial.py
```

### Git Commands to Upload

```bash
# Initialize git repo (in project root)
git init

# Add all files
git add .

# First commit
git commit -m "Initial commit: Student Management System API"

# Add your GitHub remote
git remote add origin https://github.com/YOUR_USERNAME/student-management-api.git

# Push to GitHub
git push -u origin main
```

---

## 🔧 From Scratch: Django Commands Reference

If you ever need to recreate this project from scratch:

```bash
# 1. Install dependencies
pip install django djangorestframework django-filter

# 2. Create Django project
django-admin startproject student_management_api

# 3. Navigate into project
cd student_management_api

# 4. Create the students app
python manage.py startapp students

# 5. Add 'rest_framework' and 'students' to INSTALLED_APPS in settings.py

# 6. Create migrations after writing models.py
python manage.py makemigrations

# 7. Apply migrations to create database tables
python manage.py migrate

# 8. Create admin user
python manage.py createsuperuser

# 9. Run the development server
python manage.py runserver

# 10. Run tests
python manage.py test students
```

---

*Built with ❤️ using Django REST Framework*
