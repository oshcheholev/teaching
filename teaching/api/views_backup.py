from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Course, CourseType, StudyProgram, Teacher, Department, Curicculum, Institute, Semester, CurriculumSubject, StudySubject
from api.serializers import CourseSerializer, CourseWriteSerializer, CourseTypeSerializer, StudyProgramSerializer, StudyProgramWriteSerializer, TeacherSerializer, TeacherWriteSerializer
from api.serializers import DepartmentSerializer, DepartmentWriteSerializer, CuricculumSerializer, InstituteSerializer, UserSerializer, SemesterSerializer, CurriculumSubjectSerializer, CurriculumSubjectWriteSerializer, StudySubjectSerializer, StudySubjectWriteSerializer
# Create your views here.
# class CourseView(generics.ListCreateAPIView):
# 	queryset = Course.objects.all()
# 	serializer_class = CourseSerializer
# 	permission_classes = [AllowAny]

class CourseListView(generics.ListAPIView):
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
		
		# Search by title
		search = self.request.query_params.get('search', None)
		if search is not None:
			queryset = queryset.filter(title__icontains=search)
		
		return queryset

class CourseUpdateView(generics.UpdateAPIView):
	queryset = Course.objects.all()
	serializer_class = CourseWriteSerializer
	permission_classes = [AllowAny]

class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset = Course.objects.all()
	serializer_class = CourseSerializer
	permission_classes = [AllowAny]

class CourseCreateView(generics.CreateAPIView):
	queryset = Course.objects.all()
	serializer_class = CourseWriteSerializer
	permission_classes = [AllowAny]

class CourseDeleteView(generics.DestroyAPIView):
	queryset = Course.objects.all()
	serializer_class = CourseSerializer
	permission_classes = [AllowAny]

# Course Type Views
class CourseTypeView(generics.ListAPIView):
	queryset = CourseType.objects.all()
	serializer_class = CourseTypeSerializer
	permission_classes = [AllowAny]

class CourseTypeCreateView(generics.CreateAPIView):
	queryset = CourseType.objects.all()
	serializer_class = CourseTypeSerializer
	permission_classes = [AllowAny]

class CourseTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset = CourseType.objects.all()
	serializer_class = CourseTypeSerializer
	permission_classes = [AllowAny]



#Teacher Views
class TeacherListView(generics.ListAPIView):
	queryset = Teacher.objects.all()
	serializer_class = TeacherSerializer
	permission_classes = [AllowAny]

	def get_queryset(self):
		queryset = Teacher.objects.all()
		
		# Filter by subject
		subject = self.request.query_params.get('subject', None)
		if subject is not None:
			queryset = queryset.filter(subject__icontains=subject)
		
		return queryset
class TeacherView(generics.RetrieveUpdateDestroyAPIView):
	queryset = Teacher.objects.all()
	serializer_class = TeacherSerializer
	permission_classes = [AllowAny]

class TeacherCreateView(generics.CreateAPIView):
	queryset = Teacher.objects.all()
	serializer_class = TeacherWriteSerializer
	permission_classes = [AllowAny]

class TeacherDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset = Teacher.objects.all()
	serializer_class = TeacherSerializer
	permission_classes = [AllowAny]

class TeacherUpdateView(generics.UpdateAPIView):
	queryset = Teacher.objects.all()
	serializer_class = TeacherWriteSerializer
	permission_classes = [AllowAny]

class TeacherDeleteView(generics.DestroyAPIView):
	queryset = Teacher.objects.all()
	serializer_class = TeacherSerializer
	permission_classes = [AllowAny]

# Study Program Views
class StudyProgramView(generics.ListAPIView):
	queryset = StudyProgram.objects.all()
	serializer_class = StudyProgramSerializer
	permission_classes = [AllowAny]

class StudyProgramCreateView(generics.CreateAPIView):
	queryset = StudyProgram.objects.all()
	serializer_class = StudyProgramWriteSerializer
	permission_classes = [AllowAny]

class StudyProgramDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset = StudyProgram.objects.all()
	serializer_class = StudyProgramSerializer
	permission_classes = [AllowAny]

class StudyProgramUpdateView(generics.UpdateAPIView):
	queryset = StudyProgram.objects.all()
	serializer_class = StudyProgramWriteSerializer
	permission_classes = [AllowAny]

class StudyProgramDeleteView(generics.DestroyAPIView):
	queryset = StudyProgram.objects.all()
	serializer_class = StudyProgramSerializer
	permission_classes = [AllowAny]

# Department Views
class DepartmentView(generics.ListAPIView):
	queryset = Department.objects.all()
	serializer_class = DepartmentSerializer
	permission_classes = [AllowAny]

class DepartmentCreateView(generics.CreateAPIView):
	queryset = Department.objects.all()
	serializer_class = DepartmentWriteSerializer
	permission_classes = [AllowAny]

class DepartmentDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset = Department.objects.all()
	serializer_class = DepartmentSerializer
	permission_classes = [AllowAny]

class DepartmentUpdateView(generics.UpdateAPIView):
	queryset = Department.objects.all()
	serializer_class = DepartmentWriteSerializer
	permission_classes = [AllowAny]

class DepartmentDeleteView(generics.DestroyAPIView):
	queryset = Department.objects.all()
	serializer_class = DepartmentSerializer
	permission_classes = [AllowAny]

# Institute Views
class InstituteView(generics.ListAPIView):
	queryset = Institute.objects.all()
	serializer_class = InstituteSerializer
	permission_classes = [AllowAny]

class InstituteCreateView(generics.CreateAPIView):
	queryset = Institute.objects.all()
	serializer_class = InstituteSerializer
	permission_classes = [AllowAny]

class InstituteDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset = Institute.objects.all()
	serializer_class = InstituteSerializer
	permission_classes = [AllowAny]

class InstituteUpdateView(generics.UpdateAPIView):
	queryset = Institute.objects.all()
	serializer_class = InstituteSerializer
	permission_classes = [AllowAny]

class InstituteDeleteView(generics.DestroyAPIView):
	queryset = Institute.objects.all()
	serializer_class = InstituteSerializer
	permission_classes = [AllowAny]

# Course Type Views - Additional missing views
class CourseTypeUpdateView(generics.UpdateAPIView):
	queryset = CourseType.objects.all()
	serializer_class = CourseTypeSerializer
	permission_classes = [AllowAny]

class CourseTypeDeleteView(generics.DestroyAPIView):
	queryset = CourseType.objects.all()
	serializer_class = CourseTypeSerializer
	permission_classes = [AllowAny]


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

# Semester Views
class SemesterListView(generics.ListAPIView):
	queryset = Semester.objects.all()
	serializer_class = SemesterSerializer
	permission_classes = [AllowAny]

# CurriculumSubject Views
class CurriculumSubjectListView(generics.ListAPIView):
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
	queryset = CurriculumSubject.objects.all()
	serializer_class = CurriculumSubjectWriteSerializer
	permission_classes = [AllowAny]

class CurriculumSubjectDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset = CurriculumSubject.objects.all()
	serializer_class = CurriculumSubjectWriteSerializer
	permission_classes = [AllowAny]

# StudySubject Views
class StudySubjectListView(generics.ListAPIView):
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
	queryset = StudySubject.objects.all()
	serializer_class = StudySubjectWriteSerializer
	permission_classes = [AllowAny]

class StudySubjectDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset = StudySubject.objects.all()
	serializer_class = StudySubjectWriteSerializer
	permission_classes = [AllowAny]
    