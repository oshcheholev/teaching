from django.contrib import admin
from .models import Course, CourseType, StudyProgram, Teacher, Department, Curicculum, Institute, Semester, CurriculumSubject, StudySubject

# Register your models here.

@admin.register(CourseType)
class CourseTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']
    ordering = ['name']

@admin.register(Institute)
class InstituteAdmin(admin.ModelAdmin):
	list_display = ['name', 'description']
	search_fields = ['name']
	ordering = ['name']
     
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'institute']
    search_fields = ['name']
    ordering = ['name']

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject']
    search_fields = ['name', 'email', 'subject']
    list_filter = ['subject']
    ordering = ['name']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['course_code', 'title', 'type', 'teacher', 'institute', 'department', 'study_program', 'get_semesters', 'year', 'credits', 'gender_diversity']
    list_filter = ['type', 'teacher', 'institute', 'department', 'study_program', 'semesters', 'year', 'gender_diversity']
    search_fields = ['course_code', 'title', 'description']
    date_hierarchy = 'start_date'
    ordering = ['course_code', 'title']
    filter_horizontal = ['semesters']  # For many-to-many semester relationship
    
    def get_semesters(self, obj):
        """Display all semesters for this course"""
        return ", ".join([semester.name for semester in obj.semesters.all()])
    get_semesters.short_description = 'Semesters'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('course_code', 'title', 'description', 'type', 'credits')
        }),
        ('Schedule', {
            'fields': ('semesters', 'year', 'semester_format', 'start_date', 'end_date')
        }),
        ('Assignment', {
            'fields': ('teacher', 'institute', 'department', 'study_program')
        }),
        ('Academic Structure', {
            'fields': ('curriculum_subject', 'study_subject')
        }),
        ('Options', {
            'fields': ('gender_diversity',)
        }),
    )

@admin.register(StudyProgram)
class StudyProgramAdmin(admin.ModelAdmin):
    list_display = ['name', 'department', 'year']
    list_filter = ['department', 'year']
    search_fields = ['name', 'description']
    ordering = ['-year', 'name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'department', 'year')
        }),
    )

@admin.register(Curicculum)
class CuricculumAdmin(admin.ModelAdmin):
    list_display = ['name', 'department', 'year']
    list_filter = ['department', 'year']
    search_fields = ['name', 'description']
    filter_horizontal = ['courses']  # For many-to-many fields
    ordering = ['-year', 'name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'department', 'year')
        }),
        ('Courses', {
            'fields': ('courses',)
        }),
    )

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ['name', 'year', 'season', 'start_date', 'end_date', 'is_active']
    search_fields = ['name', 'year']
    list_filter = ['season', 'year', 'is_active']
    ordering = ['-year', '-season']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'year', 'season')
        }),
        ('Schedule', {
            'fields': ('start_date', 'end_date')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )

@admin.register(CurriculumSubject)
class CurriculumSubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'study_program', 'credits', 'semester_number', 'is_mandatory']
    search_fields = ['name', 'study_program__name']
    list_filter = ['study_program', 'semester_number', 'is_mandatory']
    ordering = ['study_program__name', 'semester_number', 'name']

@admin.register(StudySubject)
class StudySubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'curriculum_subject', 'credits', 'hours_per_week', 'subject_type']
    search_fields = ['name', 'curriculum_subject__name']
    list_filter = ['curriculum_subject__study_program', 'subject_type']
    ordering = ['curriculum_subject__name', 'name']
