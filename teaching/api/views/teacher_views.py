"""
Teacher-related API Views
=========================

This module contains all views related to Teacher model.
Includes list, create, detail, update, and delete operations.
"""

from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser
from ..models import Teacher
from ..serializers import TeacherSerializer, TeacherWriteSerializer


class TeacherListView(generics.ListAPIView):
    """
    List all teachers with filtering capabilities.
    
    Supported filters:
    - subject: filter by subject (case-insensitive contains search)
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Teacher.objects.all()
        
        # Filter by subject
        subject = self.request.query_params.get('subject', None)
        if subject is not None:
            queryset = queryset.filter(subject__icontains=subject)
        
        # Search by name
        search = self.request.query_params.get('search', None)
        if search is not None:
            queryset = queryset.filter(name__icontains=search)
        
        return queryset


class TeacherView(generics.RetrieveUpdateDestroyAPIView):
    """Legacy view - kept for backward compatibility."""
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAdminUser]


class TeacherCreateView(generics.CreateAPIView):
    """Create a new teacher."""
    queryset = Teacher.objects.all()
    serializer_class = TeacherWriteSerializer
    permission_classes = [IsAdminUser]


class TeacherDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a specific teacher."""
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAdminUser]


class TeacherUpdateView(generics.UpdateAPIView):
    """Update a specific teacher."""
    queryset = Teacher.objects.all()
    serializer_class = TeacherWriteSerializer
    permission_classes = [IsAdminUser]


class TeacherDeleteView(generics.DestroyAPIView):
    """Delete a specific teacher."""
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAdminUser]
