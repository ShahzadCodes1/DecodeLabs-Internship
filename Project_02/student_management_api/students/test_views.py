"""
test_views.py - API Endpoint Tests
Run with: python manage.py test students
"""
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from students.models import Student


class StudentAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.student = Student.objects.create(
            name='Jane Smith',
            email='jane.smith@example.com',
            phone='+9876543210',
            course='Data Science',
        )
        self.valid_payload = {
            'name': 'Alice Johnson',
            'email': 'alice.johnson@example.com',
            'phone': '+1122334455',
            'course': 'Software Engineering',
        }

    def test_get_all_students(self):
        response = self.client.get('/api/students/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])

    def test_create_student_valid(self):
        response = self.client.post('/api/students/', self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['data']['name'], 'Alice Johnson')

    def test_create_student_missing_name(self):
        payload = self.valid_payload.copy()
        del payload['name']
        response = self.client.post('/api/students/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_student_duplicate_email(self):
        payload = self.valid_payload.copy()
        payload['email'] = self.student.email
        response = self.client.post('/api/students/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_student_by_id(self):
        response = self.client.get(f'/api/students/{self.student.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_student_not_found(self):
        response = self.client.get('/api/students/9999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_student_put(self):
        payload = {'name': 'Jane Updated', 'email': 'jane.upd@example.com', 'course': 'ML'}
        response = self.client.put(f'/api/students/{self.student.id}/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_student_patch(self):
        response = self.client.patch(f'/api/students/{self.student.id}/', {'name': 'Patched'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['name'], 'Patched')

    def test_delete_student(self):
        response = self.client.delete(f'/api/students/{self.student.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Student.objects.filter(id=self.student.id).exists())

    def test_search_by_name(self):
        response = self.client.get('/api/students/search/?name=jane')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data['count'], 1)

    def test_search_no_params_returns_400(self):
        response = self.client.get('/api/students/search/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_health_check(self):
        response = self.client.get('/api/health/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
