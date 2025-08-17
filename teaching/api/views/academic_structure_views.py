"""
Academic Structure API Views
=============================

This module contains views for academic structure models including:
- StudyProgram, Department, Institute
- Semester, CurriculumSubject, StudySubject
- Curicculum (legacy)
"""

from rest_framework import generics
from rest_framework.permissions import AllowAny
from ..models import (
    StudyProgram, Department, Institute, Semester, 
    CurriculumSubject, StudySubject, Curicculum
)
from ..serializers import (
    StudyProgramSerializer, StudyProgramWriteSerializer,
    DepartmentSerializer, DepartmentWriteSerializer,
    InstituteSerializer, SemesterSerializer,
    CurriculumSubjectSerializer, CurriculumSubjectWriteSerializer,
    StudySubjectSerializer, StudySubjectWriteSerializer,
    CuricculumSerializer
)


# Study Program Views
class StudyProgramView(generics.ListAPIView):
    """List all study programs."""
    queryset = StudyProgram.objects.all()
    serializer_class = StudyProgramSerializer
    permission_classes = [AllowAny]


class StudyProgramCreateView(generics.CreateAPIView):
    """Create a new study program."""
    queryset = StudyProgram.objects.all()
    serializer_class = StudyProgramWriteSerializer
    permission_classes = [AllowAny]


class StudyProgramDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a specific study program."""
    queryset = StudyProgram.objects.all()
    serializer_class = StudyProgramSerializer
    permission_classes = [AllowAny]


class StudyProgramUpdateView(generics.UpdateAPIView):
    """Update a specific study program."""
    queryset = StudyProgram.objects.all()
    serializer_class = StudyProgramWriteSerializer
    permission_classes = [AllowAny]


class StudyProgramDeleteView(generics.DestroyAPIView):
    """Delete a specific study program."""
    queryset = StudyProgram.objects.all()
    serializer_class = StudyProgramSerializer
    permission_classes = [AllowAny]


# Department Views
class DepartmentView(generics.ListAPIView):
    """List all departments."""
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [AllowAny]


class DepartmentCreateView(generics.CreateAPIView):
    """Create a new department."""
    queryset = Department.objects.all()
    serializer_class = DepartmentWriteSerializer
    permission_classes = [AllowAny]


class DepartmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a specific department."""
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [AllowAny]


class DepartmentUpdateView(generics.UpdateAPIView):
    """Update a specific department."""
    queryset = Department.objects.all()
    serializer_class = DepartmentWriteSerializer
    permission_classes = [AllowAny]


class DepartmentDeleteView(generics.DestroyAPIView):
    """Delete a specific department."""
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [AllowAny]


# Institute Views
class InstituteView(generics.ListAPIView):
    """List all institutes."""
    queryset = Institute.objects.all()
    serializer_class = InstituteSerializer
    permission_classes = [AllowAny]


class InstituteCreateView(generics.CreateAPIView):
    """Create a new institute."""
    queryset = Institute.objects.all()
    serializer_class = InstituteSerializer
    permission_classes = [AllowAny]


class InstituteDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a specific institute."""
    queryset = Institute.objects.all()
    serializer_class = InstituteSerializer
    permission_classes = [AllowAny]


class InstituteUpdateView(generics.UpdateAPIView):
    """Update a specific institute."""
    queryset = Institute.objects.all()
    serializer_class = InstituteSerializer
    permission_classes = [AllowAny]


class InstituteDeleteView(generics.DestroyAPIView):
    """Delete a specific institute."""
    queryset = Institute.objects.all()
    serializer_class = InstituteSerializer
    permission_classes = [AllowAny]


# Semester Views
class SemesterListView(generics.ListAPIView):
    """
    List all semesters.
    
    Supports filtering by:
    - year: academic year
    - season: W (Winter) or S (Summer)
    - is_active: true/false
    """
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = Semester.objects.all()
        
        # Filter by year
        year = self.request.query_params.get('year', None)
        if year is not None:
            try:
                year_int = int(year)
                queryset = queryset.filter(year=year_int)
            except ValueError:
                pass
        
        # Filter by season
        season = self.request.query_params.get('season', None)
        if season in ['W', 'S']:
            queryset = queryset.filter(season=season)
        
        # Filter by active status
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            is_active_bool = is_active.lower() == 'true'
            queryset = queryset.filter(is_active=is_active_bool)
        
        return queryset


# CurriculumSubject Views
class CurriculumSubjectListView(generics.ListAPIView):
    """
    List curriculum subjects with filtering.
    
    Supports filtering by:
    - study_program: study program ID(s) - supports multiple
    """
    queryset = CurriculumSubject.objects.all()
    serializer_class = CurriculumSubjectSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = CurriculumSubject.objects.all()
        
        # Filter by study program
        study_program_ids = self.request.query_params.getlist('study_program')
        if study_program_ids:
            queryset = queryset.filter(study_program__id__in=study_program_ids)
            
        return queryset


class CurriculumSubjectCreateView(generics.CreateAPIView):
    """Create a new curriculum subject."""
    queryset = CurriculumSubject.objects.all()
    serializer_class = CurriculumSubjectWriteSerializer
    permission_classes = [AllowAny]


class CurriculumSubjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a specific curriculum subject."""
    queryset = CurriculumSubject.objects.all()
    serializer_class = CurriculumSubjectWriteSerializer
    permission_classes = [AllowAny]


# StudySubject Views
class StudySubjectListView(generics.ListAPIView):
    """
    List study subjects with filtering.
    
    Supports filtering by:
    - curriculum_subject: curriculum subject ID(s) - supports multiple
    """
    queryset = StudySubject.objects.all()
    serializer_class = StudySubjectSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = StudySubject.objects.all()
        
        # Filter by curriculum subject
        curriculum_subject_ids = self.request.query_params.getlist('curriculum_subject')
        if curriculum_subject_ids:
            queryset = queryset.filter(curriculum_subject__id__in=curriculum_subject_ids)
            
        return queryset


class StudySubjectCreateView(generics.CreateAPIView):
    """Create a new study subject."""
    queryset = StudySubject.objects.all()
    serializer_class = StudySubjectWriteSerializer
    permission_classes = [AllowAny]


class StudySubjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a specific study subject."""
    queryset = StudySubject.objects.all()
    serializer_class = StudySubjectWriteSerializer
    permission_classes = [AllowAny]
