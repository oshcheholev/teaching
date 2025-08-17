"""
API Views Package - Organized by Domain/Model
==============================================

This package contains all API views organized by functional domain.
Each module handles views for related models.
"""

# Import all views for easy access
from .course_views import *
from .teacher_views import *
from .academic_structure_views import *
from .user_views import *

__all__ = [
    # Course related views
    'CourseListView', 'CourseCreateView', 'CourseDetailView', 
    'CourseUpdateView', 'CourseDeleteView',
    'CourseTypeView', 'CourseTypeCreateView', 'CourseTypeDetailView',
    'CourseTypeUpdateView', 'CourseTypeDeleteView',
    
    # Teacher related views
    'TeacherListView', 'TeacherView', 'TeacherCreateView', 
    'TeacherDetailView', 'TeacherUpdateView', 'TeacherDeleteView',
    
    # Academic structure views
    'StudyProgramView', 'StudyProgramCreateView', 'StudyProgramDetailView',
    'StudyProgramUpdateView', 'StudyProgramDeleteView',
    'DepartmentView', 'DepartmentCreateView', 'DepartmentDetailView',
    'DepartmentUpdateView', 'DepartmentDeleteView',
    'InstituteView', 'InstituteCreateView', 'InstituteDetailView',
    'InstituteUpdateView', 'InstituteDeleteView',
    'SemesterListView',
    'CurriculumSubjectListView', 'CurriculumSubjectCreateView', 'CurriculumSubjectDetailView',
    'StudySubjectListView', 'StudySubjectCreateView', 'StudySubjectDetailView',
    
    # User views
    'CreateUserView',
]
