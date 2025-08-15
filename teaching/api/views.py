from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Course, CourseType, StudyProgram, Teacher, Department, Curicculum, Institute
from api.serializers import CourseSerializer, CourseWriteSerializer, CourseTypeSerializer, StudyProgramSerializer, StudyProgramWriteSerializer, TeacherSerializer, TeacherWriteSerializer
from api.serializers import DepartmentSerializer, DepartmentWriteSerializer, CuricculumSerializer, InstituteSerializer, UserSerializer
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
		
		# Filter by teacher
		teacher_id = self.request.query_params.get('teacher', None)
		if teacher_id is not None:
			queryset = queryset.filter(teacher_id=teacher_id)
		
		# Filter by course type
		course_type_id = self.request.query_params.get('type', None)
		if course_type_id is not None:
			queryset = queryset.filter(type_id=course_type_id)
		
		# Filter by institute
		institute_id = self.request.query_params.get('institute', None)
		if institute_id is not None:
			queryset = queryset.filter(institute_id=institute_id)
		
		# Filter by department
		department_id = self.request.query_params.get('department', None)
		if department_id is not None:
			queryset = queryset.filter(department_id=department_id)
		
		# Filter by study program
		study_program_id = self.request.query_params.get('study_program', None)
		if study_program_id is not None:
			queryset = queryset.filter(study_program_id=study_program_id)
		
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
    