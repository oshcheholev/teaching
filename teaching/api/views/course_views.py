"""
Course-related API Views
========================

This module contains all views related to Course and CourseType models.
Includes list, create, detail, update, and delete operations.
"""

from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser
from ..models import Course, CourseType
from ..serializers import (
    CourseSerializer, CourseWriteSerializer, CourseTypeSerializer
)


class CourseListView(generics.ListAPIView):
    """
    List all courses with advanced filtering capabilities.
    
    Supported filters:
    - gender_diversity: true/false
    - semester_format: e.g., 2025W, 2026S
    - teacher: teacher ID(s) - supports multiple
    - type: course type ID(s) - supports multiple  
    - institute: institute ID(s) - supports multiple
    - department: department ID(s) - supports multiple
    - study_program: study program ID(s) - supports multiple
    - search: text search in course titles
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = Course.objects.all()
        
        # Filter by gender/diversity
        gender_diversity = self.request.query_params.get('gender_diversity', None)
        if gender_diversity is not None:
            gender_diversity = gender_diversity.lower() == 'true'
            queryset = queryset.filter(gender_diversity=gender_diversity)
        
        # Filter by semester format
        semester_format = self.request.query_params.get('semester_format', None)
        if semester_format is not None:
            queryset = queryset.filter(semester_format=semester_format)
        
        # Filter by teacher (can be multiple)
        teacher_ids = self.request.query_params.getlist('teacher')
        if teacher_ids:
            queryset = queryset.filter(teacher_id__in=teacher_ids)
        
        # Filter by course type (can be multiple)
        course_type_ids = self.request.query_params.getlist('type')
        if course_type_ids:
            queryset = queryset.filter(type_id__in=course_type_ids)
        
        # Filter by institute (can be multiple)
        institute_ids = self.request.query_params.getlist('institute')
        if institute_ids:
            queryset = queryset.filter(institute_id__in=institute_ids)
        
        # Filter by department (can be multiple)
        department_ids = self.request.query_params.getlist('department')
        if department_ids:
            queryset = queryset.filter(department_id__in=department_ids)
        
        # Filter by study program (can be multiple)
        study_program_ids = self.request.query_params.getlist('study_program')
        if study_program_ids:
            queryset = queryset.filter(study_program_id__in=study_program_ids)
        
        # Filter by semester (many-to-many relationship)
        semester_ids = self.request.query_params.getlist('semester')
        if semester_ids:
            queryset = queryset.filter(semesters__id__in=semester_ids).distinct()
        
        # Search by title
        search = self.request.query_params.get('search', None)
        if search is not None:
            queryset = queryset.filter(title__icontains=search)
        
        return queryset


class CourseCreateView(generics.CreateAPIView):
    """Create a new course."""
    queryset = Course.objects.all()
    serializer_class = CourseWriteSerializer
    permission_classes = [IsAdminUser]


class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a specific course."""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAdminUser]


class CourseUpdateView(generics.UpdateAPIView):
    """Update a specific course."""
    queryset = Course.objects.all()
    serializer_class = CourseWriteSerializer
    permission_classes = [IsAdminUser]


class CourseDeleteView(generics.DestroyAPIView):
    """Delete a specific course."""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAdminUser]


# CourseType Views
class CourseTypeView(generics.ListAPIView):
    """List all course types."""
    queryset = CourseType.objects.all()
    serializer_class = CourseTypeSerializer
    permission_classes = [AllowAny]


class CourseTypeCreateView(generics.CreateAPIView):
    """Create a new course type."""
    queryset = CourseType.objects.all()
    serializer_class = CourseTypeSerializer
    permission_classes = [IsAdminUser]


class CourseTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a specific course type."""
    queryset = CourseType.objects.all()
    serializer_class = CourseTypeSerializer
    permission_classes = [IsAdminUser]


class CourseTypeUpdateView(generics.UpdateAPIView):
    """Update a specific course type."""
    queryset = CourseType.objects.all()
    serializer_class = CourseTypeSerializer
    permission_classes = [IsAdminUser]


class CourseTypeDeleteView(generics.DestroyAPIView):
    """Delete a specific course type."""
    queryset = CourseType.objects.all()
    serializer_class = CourseTypeSerializer
    permission_classes = [IsAdminUser]
