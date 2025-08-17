from django.urls import path, include
from . import views
from . import admin_views


urlpatterns = [
	# Authentication & Admin
	path('auth/register/', admin_views.CreateUserView.as_view(), name='register'),
	path('auth/admin-login/', admin_views.AdminLoginView.as_view(), name='admin-login'),
	path('auth/profile/', admin_views.UserProfileView.as_view(), name='user-profile'),
	path('auth/check-admin/', admin_views.check_admin_status, name='check-admin'),

	path('admin/users/', admin_views.AdminUserListView.as_view(), name='admin-users'),
	path('admin/users/<int:pk>/', admin_views.AdminUserDetailView.as_view(), name='admin-user-detail'),

	path('courses/', views.CourseListView.as_view(), name='course-list'),
	path('courses/<int:pk>/', views.CourseDetailView.as_view(), name='course-detail'),
	path('courses/add/', views.CourseCreateView.as_view(), name='course-create'),
	path('courses/<int:pk>/update/', views.CourseUpdateView.as_view(), name='course-update'),
	path('courses/<int:pk>/delete/', views.CourseDeleteView.as_view(), name='course-delete'),

	# Course Types
	path('course-types/', views.CourseTypeView.as_view(), name='course-type-list'),
	path('course-types/<int:pk>/', views.CourseTypeDetailView.as_view(), name='course-type-detail'),
	path('course-types/add/', views.CourseTypeCreateView.as_view(), name='course-type-create'),
	path('course-types/<int:pk>/update/', views.CourseTypeUpdateView.as_view(), name='course-type-update'),
	path('course-types/<int:pk>/delete/', views.CourseTypeDeleteView.as_view(), name='course-type-delete'),

	# Study Programs
	path('study-programs/', views.StudyProgramView.as_view(), name='study-program-list'),
	path('study-programs/<int:pk>/', views.StudyProgramDetailView.as_view(), name='study-program-detail'),
	path('study-programs/add/', views.StudyProgramCreateView.as_view(), name='study-program-create'),
	path('study-programs/<int:pk>/update/', views.StudyProgramUpdateView.as_view(), name='study-program-update'),
	path('study-programs/<int:pk>/delete/', views.StudyProgramDeleteView.as_view(), name='study-program-delete'),

	# Teachers
	path('teachers/', views.TeacherListView.as_view(), name='teacher-list'),
	path('teachers/<int:pk>/', views.TeacherDetailView.as_view(), name='teacher-detail'),
	path('teachers/add/', views.TeacherCreateView.as_view(), name='teacher-create'),
	path('teachers/<int:pk>/update/', views.TeacherUpdateView.as_view(), name='teacher-update'),
	path('teachers/<int:pk>/delete/', views.TeacherDeleteView.as_view(), name='teacher-delete'),

	# Departments
	path('departments/', views.DepartmentView.as_view(), name='department-list'),
	path('departments/<int:pk>/', views.DepartmentDetailView.as_view(), name='department-detail'),
	path('departments/add/', views.DepartmentCreateView.as_view(), name='department-create'),
	path('departments/<int:pk>/update/', views.DepartmentUpdateView.as_view(), name='department-update'),
	path('departments/<int:pk>/delete/', views.DepartmentDeleteView.as_view(), name='department-delete'),

	# Institutes
	path('institutes/', views.InstituteView.as_view(), name='institute-list'),
	path('institutes/<int:pk>/', views.InstituteDetailView.as_view(), name='institute-detail'),
	path('institutes/add/', views.InstituteCreateView.as_view(), name='institute-create'),
	path('institutes/<int:pk>/update/', views.InstituteUpdateView.as_view(), name='institute-update'),
	path('institutes/<int:pk>/delete/', views.InstituteDeleteView.as_view(), name='institute-delete'),

	# Semesters
	path('semesters/', views.SemesterListView.as_view(), name='semester-list'),
	path('semesters/<int:pk>/', views.SemesterDetailView.as_view(), name='semester-detail'),
	path('semesters/add/', views.SemesterCreateView.as_view(), name='semester-create'),
	path('semesters/<int:pk>/update/', views.SemesterUpdateView.as_view(), name='semester-update'),
	path('semesters/<int:pk>/delete/', views.SemesterDeleteView.as_view(), name='semester-delete'),


	# Curriculum Subjects
	path('curriculum-subjects/', views.CurriculumSubjectListView.as_view(), name='curriculum-subject-list'),
	path('curriculum-subjects/<int:pk>/', views.CurriculumSubjectDetailView.as_view(), name='curriculum-subject-detail'),
	path('curriculum-subjects/add/', views.CurriculumSubjectCreateView.as_view(), name='curriculum-subject-create'),
	path('curriculum-subjects/<int:pk>/update/', views.CurriculumSubjectUpdateView.as_view(), name='curriculum-subject-update'),
	path('curriculum-subjects/<int:pk>/delete/', views.CurriculumSubjectDeleteView.as_view(), name='curriculum-subject-delete'),

	# Study Subjects
	path('study-subjects/', views.StudySubjectListView.as_view(), name='study-subject-list'),
	path('study-subjects/<int:pk>/', views.StudySubjectDetailView.as_view(), name='study-subject-detail'),
	path('study-subjects/add/', views.StudySubjectCreateView.as_view(), name='study-subject-create'),
	path('study-subjects/<int:pk>/update/', views.StudySubjectUpdateView.as_view(), name='study-subject-update'),
	path('study-subjects/<int:pk>/delete/', views.StudySubjectDeleteView.as_view(), name='study-subject-delete'),
]

