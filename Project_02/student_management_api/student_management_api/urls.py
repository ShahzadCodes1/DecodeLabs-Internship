"""
student_management_api/urls.py - Project-Level URL Configuration
=================================================================
This is the MAIN URL configuration file for the entire Django project.

Think of it as the "main router" that delegates to app-level routers.

All our API endpoints are prefixed with 'api/' so:
  /api/students/     → handled by students app
  /api/health/       → handled by students app
  /admin/            → Django built-in admin panel
"""

from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def api_root(request):
    """
    Root endpoint - shows available API routes.
    GET / → Welcome message with links
    """
    return JsonResponse({
        "message": "Welcome to the Student Management System API",
        "version": "1.0.0",
        "documentation": "See README.md for full API documentation",
        "endpoints": {
            "api_root": "/api/",
            "health_check": "/api/health/",
            "students": "/api/students/",
            "search": "/api/students/search/",
            "admin": "/admin/",
        }
    })


urlpatterns = [
    # Django admin panel (comes built-in with Django)
    path('admin/', admin.site.urls),

    # Root URL — helpful welcome message
    path('', api_root, name='api-root'),

    # All student API routes are prefixed with 'api/'
    # include() delegates matching to the students app's urls.py
    path('api/', include('students.urls', namespace='students')),
]
