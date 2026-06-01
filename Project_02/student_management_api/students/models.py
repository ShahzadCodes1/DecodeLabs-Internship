"""
models.py - Student Database Model
===================================
This file defines the Student database table structure.
Django uses this class to create the actual database table automatically.

Think of it like a blueprint: every field here becomes a column in the database.
"""

from django.db import models


class Student(models.Model):
    """
    Student Model - Represents a student record in the database.

    Each field maps to a column in the 'students' table.
    Django creates this table automatically when you run migrations.
    """

    # CharField = text field with a max length
    name = models.CharField(
        max_length=100,
        blank=False,   # Cannot be an empty string
        null=False,    # Cannot be NULL in the database
        help_text="Full name of the student"
    )

    # EmailField = special CharField that validates email format
    email = models.EmailField(
        max_length=255,
        unique=True,   # No two students can have the same email
        blank=False,
        null=False,
        help_text="Unique email address of the student"
    )

    # Phone is optional (blank=True, null=True)
    phone = models.CharField(
        max_length=20,
        blank=True,    # Can be an empty string
        null=True,     # Can be NULL in the database
        help_text="Contact phone number (optional)"
    )

    # Course the student is enrolled in
    course = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text="Course or program the student is enrolled in"
    )

    # auto_now_add=True means this is set ONCE when the record is created
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the student record was created"
    )

    # auto_now=True updates every time the record is saved
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the student record was last updated"
    )

    class Meta:
        db_table = 'students'
        ordering = ['-created_at']
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return f"{self.name} ({self.email})"
