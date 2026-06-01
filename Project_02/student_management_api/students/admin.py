"""
admin.py - Django Admin Panel Configuration
============================================
This registers our Student model with Django's built-in admin panel.
After running the server, visit http://127.0.0.1:8000/admin/
to manage students through a web interface.

You need a superuser account to log in:
  python manage.py createsuperuser
"""

from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """
    Customizes how Students appear and behave in the Django admin panel.
    """

    # Columns shown in the student list view
    list_display = ['id', 'name', 'email', 'course', 'phone', 'created_at']

    # Clickable fields (clicking opens the detail view)
    list_display_links = ['id', 'name']

    # Add a search box that searches these fields
    search_fields = ['name', 'email', 'course']

    # Add filter sidebar on the right
    list_filter = ['course', 'created_at']

    # Default ordering in admin
    ordering = ['-created_at']

    # Fields shown in the detail/edit view
    readonly_fields = ['id', 'created_at', 'updated_at']

    # How many records per page in admin list
    list_per_page = 25

    # Group fields in the detail view
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Academic Information', {
            'fields': ('course',)
        }),
        ('System Information', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',),  # Collapsible section
        }),
    )
