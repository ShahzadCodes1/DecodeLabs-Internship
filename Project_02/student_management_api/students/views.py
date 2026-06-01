"""
views.py - API View Logic (The Controllers)
============================================
Views contain the actual business logic for each API endpoint.

When a request hits an endpoint:
  URL → urls.py routes it → views.py handles it → returns JSON response

We use TWO styles of views here for learning purposes:
  1. Class-Based Views (CBV) with APIView — more explicit, great for learning
  2. A custom search view to demonstrate filtering

HTTP Methods → CRUD Operations:
  GET    → Read   (get students)
  POST   → Create (add student)
  PUT    → Update (replace entire student)
  PATCH  → Update (update some fields)
  DELETE → Delete (remove student)
"""

import logging
from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .models import Student
from .serializers import StudentSerializer, StudentListSerializer

# Set up logging — good practice for production APIs
logger = logging.getLogger(__name__)


# ===================================================================
# PAGINATION
# ===================================================================

class StudentPagination(PageNumberPagination):
    """
    Controls how many results are returned per page.

    Usage: GET /api/students/?page=1&page_size=5
    """
    page_size = 10              # Default: 10 students per page
    page_size_query_param = 'page_size'  # Allow client to override with ?page_size=5
    max_page_size = 100         # Never return more than 100 at once


# ===================================================================
# HELPER FUNCTION
# ===================================================================

def get_student_or_404(pk):
    """
    Helper function to get a student by ID or return None.
    Centralizes the 'does this student exist?' logic.

    Returns: (student_object, error_response) tuple
    - If found: (student, None)
    - If not found: (None, Response with 404)
    """
    try:
        student = Student.objects.get(pk=pk)
        return student, None
    except Student.DoesNotExist:
        error_response = Response(
            {
                "success": False,
                "error": "Not Found",
                "message": f"Student with ID {pk} does not exist.",
                "data": None
            },
            status=status.HTTP_404_NOT_FOUND
        )
        return None, error_response


# ===================================================================
# VIEW 1: StudentListCreateView
# Handles: GET /api/students/ and POST /api/students/
# ===================================================================

class StudentListCreateView(APIView):
    """
    GET  /api/students/  → List all students (with pagination & filtering)
    POST /api/students/  → Create a new student
    """

    def get(self, request):
        """
        GET /api/students/
        Returns a paginated list of all students.

        Optional query parameters:
          ?search=john          → Search by name, email, or course
          ?course=Engineering   → Filter by exact course
          ?page=2               → Go to page 2
          ?page_size=5          → Show 5 per page
        """
        try:
            # Start with ALL students
            queryset = Student.objects.all()

            # --- FILTERING ---
            # Filter by course if provided: ?course=Computer Science
            course_filter = request.query_params.get('course', None)
            if course_filter:
                queryset = queryset.filter(course__icontains=course_filter)

            # --- SEARCHING ---
            # Search across name, email, course: ?search=john
            search_query = request.query_params.get('search', None)
            if search_query:
                # Q objects allow OR conditions in database queries
                queryset = queryset.filter(
                    Q(name__icontains=search_query) |
                    Q(email__icontains=search_query) |
                    Q(course__icontains=search_query)
                )

            # --- PAGINATION ---
            paginator = StudentPagination()
            paginated_queryset = paginator.paginate_queryset(queryset, request)

            # Serialize the data (convert Python objects → JSON-ready dicts)
            serializer = StudentListSerializer(paginated_queryset, many=True)

            # Build a custom response with metadata
            return Response(
                {
                    "success": True,
                    "message": "Students retrieved successfully.",
                    "count": paginator.page.paginator.count,
                    "total_pages": paginator.page.paginator.num_pages,
                    "current_page": paginator.page.number,
                    "next": paginator.get_next_link(),
                    "previous": paginator.get_previous_link(),
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            # Log the error for debugging
            logger.error(f"Error retrieving students: {str(e)}", exc_info=True)
            return Response(
                {
                    "success": False,
                    "error": "Internal Server Error",
                    "message": "An unexpected error occurred while retrieving students.",
                    "data": None
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        """
        POST /api/students/
        Creates a new student record.

        Request body (JSON):
        {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "+1234567890",   ← optional
            "course": "Computer Science"
        }
        """
        try:
            # Pass the incoming data to the serializer for validation
            # request.data contains the parsed JSON body
            serializer = StudentSerializer(data=request.data)

            if serializer.is_valid():
                # Data passed all validations — save to database
                student = serializer.save()

                logger.info(f"New student created: {student.name} (ID: {student.id})")

                return Response(
                    {
                        "success": True,
                        "message": "Student created successfully.",
                        "data": serializer.data
                    },
                    status=status.HTTP_201_CREATED  # 201 = Created (not 200)
                )
            else:
                # Validation failed — return the errors
                return Response(
                    {
                        "success": False,
                        "error": "Validation Error",
                        "message": "Please fix the errors below.",
                        "errors": serializer.errors,
                        "data": None
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:
            logger.error(f"Error creating student: {str(e)}", exc_info=True)
            return Response(
                {
                    "success": False,
                    "error": "Internal Server Error",
                    "message": "An unexpected error occurred while creating the student.",
                    "data": None
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# ===================================================================
# VIEW 2: StudentDetailView
# Handles: GET, PUT, PATCH, DELETE /api/students/<id>/
# ===================================================================

class StudentDetailView(APIView):
    """
    GET    /api/students/<id>/  → Get one student by ID
    PUT    /api/students/<id>/  → Update ALL fields of a student
    PATCH  /api/students/<id>/  → Update SOME fields of a student
    DELETE /api/students/<id>/  → Delete a student
    """

    def get(self, request, pk):
        """
        GET /api/students/<id>/
        Returns a single student by their ID.
        """
        student, error = get_student_or_404(pk)
        if error:
            return error  # Returns 404 if not found

        serializer = StudentSerializer(student)

        return Response(
            {
                "success": True,
                "message": "Student retrieved successfully.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

    def put(self, request, pk):
        """
        PUT /api/students/<id>/
        Full update: ALL required fields must be provided.
        Missing fields will be set to their defaults or cause a validation error.
        """
        student, error = get_student_or_404(pk)
        if error:
            return error

        try:
            # partial=False means ALL required fields must be present
            serializer = StudentSerializer(student, data=request.data, partial=False)

            if serializer.is_valid():
                serializer.save()
                logger.info(f"Student updated (full): ID {pk}")

                return Response(
                    {
                        "success": True,
                        "message": "Student updated successfully.",
                        "data": serializer.data
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        "success": False,
                        "error": "Validation Error",
                        "message": "Please fix the errors below.",
                        "errors": serializer.errors,
                        "data": None
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:
            logger.error(f"Error updating student {pk}: {str(e)}", exc_info=True)
            return Response(
                {
                    "success": False,
                    "error": "Internal Server Error",
                    "message": "An unexpected error occurred while updating the student.",
                    "data": None
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def patch(self, request, pk):
        """
        PATCH /api/students/<id>/
        Partial update: Only send the fields you want to change.
        Other fields remain unchanged.
        """
        student, error = get_student_or_404(pk)
        if error:
            return error

        try:
            # partial=True means only provided fields are updated
            serializer = StudentSerializer(student, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                logger.info(f"Student updated (partial): ID {pk}")

                return Response(
                    {
                        "success": True,
                        "message": "Student partially updated successfully.",
                        "data": serializer.data
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        "success": False,
                        "error": "Validation Error",
                        "message": "Please fix the errors below.",
                        "errors": serializer.errors,
                        "data": None
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:
            logger.error(f"Error patching student {pk}: {str(e)}", exc_info=True)
            return Response(
                {
                    "success": False,
                    "error": "Internal Server Error",
                    "message": "An unexpected error occurred.",
                    "data": None
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, pk):
        """
        DELETE /api/students/<id>/
        Permanently removes the student from the database.
        Returns 200 with confirmation (some APIs return 204 No Content).
        """
        student, error = get_student_or_404(pk)
        if error:
            return error

        try:
            student_name = student.name
            student_id = student.id
            student.delete()

            logger.info(f"Student deleted: {student_name} (ID: {student_id})")

            return Response(
                {
                    "success": True,
                    "message": f"Student '{student_name}' (ID: {student_id}) deleted successfully.",
                    "data": None
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            logger.error(f"Error deleting student {pk}: {str(e)}", exc_info=True)
            return Response(
                {
                    "success": False,
                    "error": "Internal Server Error",
                    "message": "An unexpected error occurred while deleting the student.",
                    "data": None
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# ===================================================================
# VIEW 3: StudentSearchView (BONUS)
# Handles: GET /api/students/search/?name=john
# ===================================================================

class StudentSearchView(APIView):
    """
    BONUS: Dedicated search endpoint.
    GET /api/students/search/?name=john
    GET /api/students/search/?course=Engineering
    GET /api/students/search/?name=john&course=CS

    This provides more targeted search than the general list endpoint.
    """

    def get(self, request):
        """
        Search students by name and/or course.
        """
        try:
            name_query = request.query_params.get('name', '').strip()
            course_query = request.query_params.get('course', '').strip()
            email_query = request.query_params.get('email', '').strip()

            # Must provide at least one search parameter
            if not any([name_query, course_query, email_query]):
                return Response(
                    {
                        "success": False,
                        "error": "Bad Request",
                        "message": "Please provide at least one search parameter: name, course, or email.",
                        "data": None
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            queryset = Student.objects.all()

            if name_query:
                queryset = queryset.filter(name__icontains=name_query)

            if course_query:
                queryset = queryset.filter(course__icontains=course_query)

            if email_query:
                queryset = queryset.filter(email__icontains=email_query)

            # Paginate the search results
            paginator = StudentPagination()
            paginated = paginator.paginate_queryset(queryset, request)

            serializer = StudentSerializer(paginated, many=True)

            return Response(
                {
                    "success": True,
                    "message": f"Found {queryset.count()} student(s) matching your search.",
                    "count": queryset.count(),
                    "total_pages": paginator.page.paginator.num_pages,
                    "current_page": paginator.page.number,
                    "next": paginator.get_next_link(),
                    "previous": paginator.get_previous_link(),
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            logger.error(f"Error searching students: {str(e)}", exc_info=True)
            return Response(
                {
                    "success": False,
                    "error": "Internal Server Error",
                    "message": "An unexpected error occurred during search.",
                    "data": None
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# ===================================================================
# VIEW 4: API Health Check
# Handles: GET /api/health/
# ===================================================================

class HealthCheckView(APIView):
    """
    Simple health check endpoint.
    Useful for monitoring — tells you the API is alive and responding.

    GET /api/health/
    """

    def get(self, request):
        return Response(
            {
                "success": True,
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
                    "health_check": "GET /api/health/",
                }
            },
            status=status.HTTP_200_OK
        )
