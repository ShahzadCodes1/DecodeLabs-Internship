"""
serializers.py - Data Serialization & Validation
==================================================
Serializers do TWO important jobs:

1. SERIALIZATION: Convert Python objects (from database) → JSON (for API responses)
2. DESERIALIZATION + VALIDATION: Convert JSON (from requests) → Python objects
   AND validate that the data is correct before saving.

Think of it as a strict gatekeeper that checks data in both directions.
"""

import re
from rest_framework import serializers
from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    """
    Main serializer for the Student model.

    ModelSerializer automatically generates fields based on the model,
    so you don't have to manually define every field.
    """

    class Meta:
        # Tell it which model to serialize
        model = Student

        # Which fields to include in API responses/requests
        # '__all__' would include everything, but being explicit is better practice
        fields = [
            'id',
            'name',
            'email',
            'phone',
            'course',
            'created_at',
            'updated_at',
        ]

        # Read-only fields cannot be changed via POST/PUT requests
        # 'id' is auto-generated, 'created_at' and 'updated_at' are auto-set
        read_only_fields = ['id', 'created_at', 'updated_at']

    # -------------------------------------------------------
    # FIELD-LEVEL VALIDATION METHODS
    # Django REST Framework calls validate_<fieldname> automatically
    # -------------------------------------------------------

    def validate_name(self, value):
        """
        Validate the 'name' field.
        - Must not be empty or just whitespace
        - Must be at least 2 characters
        - Must be at most 100 characters
        - Should only contain letters, spaces, hyphens, apostrophes
        """
        # Strip leading/trailing whitespace
        value = value.strip()

        if not value:
            raise serializers.ValidationError("Name cannot be empty or whitespace.")

        if len(value) < 2:
            raise serializers.ValidationError("Name must be at least 2 characters long.")

        if len(value) > 100:
            raise serializers.ValidationError("Name cannot exceed 100 characters.")

        # Allow letters (including unicode for international names), spaces, hyphens, apostrophes
        if not re.match(r"^[\w\s'\-\.]+$", value, re.UNICODE):
            raise serializers.ValidationError(
                "Name can only contain letters, spaces, hyphens, apostrophes, and dots."
            )

        return value

    def validate_email(self, value):
        """
        Validate the 'email' field.
        - Django's EmailField already checks format
        - We add: uniqueness check (excluding current instance on updates)
        - Convert to lowercase for consistency
        """
        value = value.strip().lower()

        # Check for uniqueness
        # self.instance is the existing object (set during UPDATE, None during CREATE)
        queryset = Student.objects.filter(email=value)

        if self.instance:
            # On UPDATE: exclude the current student from uniqueness check
            # (a student can keep their own email)
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError(
                "A student with this email address already exists."
            )

        return value

    def validate_phone(self, value):
        """
        Validate the 'phone' field.
        - Phone is optional, so empty/None is allowed
        - If provided, must match a basic phone pattern
        """
        if not value:
            return value  # Optional field, skip validation if empty

        # Remove spaces and dashes for validation
        cleaned = re.sub(r'[\s\-\(\)]', '', value)

        # Allow +, digits, and basic phone characters
        if not re.match(r'^\+?[\d]{7,15}$', cleaned):
            raise serializers.ValidationError(
                "Enter a valid phone number (7-15 digits, optionally starting with +)."
            )

        return value

    def validate_course(self, value):
        """
        Validate the 'course' field.
        - Must not be empty
        - Minimum 2 characters
        """
        value = value.strip()

        if not value:
            raise serializers.ValidationError("Course cannot be empty.")

        if len(value) < 2:
            raise serializers.ValidationError("Course name must be at least 2 characters.")

        return value

    def validate(self, data):
        """
        Object-level validation (runs AFTER all field-level validations).
        Use this when validation depends on MULTIPLE fields together.

        Example: you could check that the combination of name + course is unique.
        For now, we just pass through, but this is the right place for cross-field logic.
        """
        return data


class StudentListSerializer(serializers.ModelSerializer):
    """
    A lighter serializer for list views.
    When returning many students, we might not need every field.
    This improves performance on large datasets.
    """

    class Meta:
        model = Student
        fields = ['id', 'name', 'email', 'course', 'created_at']
        read_only_fields = ['id', 'created_at']
