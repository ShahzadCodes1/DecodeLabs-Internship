"""
test_models.py - Unit Tests for the Student Model
Run with: python manage.py test students
"""
from django.test import TestCase
from students.models import Student


class StudentModelTest(TestCase):

    def setUp(self):
        self.student_data = {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'phone': '+1234567890',
            'course': 'Computer Science',
        }

    def test_create_student_success(self):
        student = Student.objects.create(**self.student_data)
        self.assertIsNotNone(student.id)
        self.assertEqual(student.name, 'John Doe')
        self.assertIsNotNone(student.created_at)

    def test_student_str_representation(self):
        student = Student.objects.create(**self.student_data)
        self.assertEqual(str(student), "John Doe (john.doe@example.com)")

    def test_email_must_be_unique(self):
        Student.objects.create(**self.student_data)
        with self.assertRaises(Exception):
            Student.objects.create(**self.student_data)

    def test_phone_is_optional(self):
        data = self.student_data.copy()
        data['phone'] = None
        data['email'] = 'nophone@example.com'
        student = Student.objects.create(**data)
        self.assertIsNone(student.phone)
