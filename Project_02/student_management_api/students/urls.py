"""
students/urls.py - App-Level URL Routing
==========================================
This file maps URL patterns to view functions for the 'students' app.

URL PATTERN REFERENCE:
  path('students/', ...)         → matches /api/students/
  path('students/<int:pk>/', ...)→ matches /api/students/1/, /api/students/42/, etc.
  <int:pk> is a URL parameter — Django extracts the number and passes it to the view as 'pk'
"""

from django.urls import path
from . import views

# app_name creates a namespace for these URLs
# Useful for reversing URLs: reverse('students:student-list')
app_name = 'students'

urlpatterns = [
    # ---------------------------------------------------
    # HEALTH CHECK
    # GET /api/health/
    # ---------------------------------------------------
    path(
        'health/',
        views.HealthCheckView.as_view(),
        name='health-check'
    ),

    # ---------------------------------------------------
    # STUDENT LIST & CREATE
    # GET  /api/students/  → List all students
    # POST /api/students/  → Create new student
    # ---------------------------------------------------
    path(
        'students/',
        views.StudentListCreateView.as_view(),
        name='student-list-create'
    ),

    # ---------------------------------------------------
    # STUDENT SEARCH (BONUS)
    # Must come BEFORE the <int:pk> route to avoid conflicts
    # GET /api/students/search/?name=john
    # ---------------------------------------------------
    path(
        'students/search/',
        views.StudentSearchView.as_view(),
        name='student-search'
    ),

    # ---------------------------------------------------
    # STUDENT DETAIL (by ID)
    # GET    /api/students/1/  → Get student with ID 1
    # PUT    /api/students/1/  → Full update
    # PATCH  /api/students/1/  → Partial update
    # DELETE /api/students/1/  → Delete student
    # ---------------------------------------------------
    path(
        'students/<int:pk>/',
        views.StudentDetailView.as_view(),
        name='student-detail'
    ),
]
