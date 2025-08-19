from django.db import models

# Create your models here.

class Course(models.Model):
	title = models.CharField(max_length=100)
	course_code = models.CharField(
		max_length=10, 
		unique=True, 
		help_text="Unique course code, e.g., S05618, S04261",
		db_index=True
	)
	description = models.TextField()
	type = models.ForeignKey('CourseType', on_delete=models.CASCADE, null=True, blank=True)
	# Removed single semester field, replaced with many-to-many relationship below
	year = models.IntegerField(null=True, blank=True)
	start_date = models.DateField(null=True, blank=True)
	end_date = models.DateField(null=True, blank=True)
	teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, null=True, blank=True)
	credits = models.IntegerField(null=True, blank=True)
	gender_diversity = models.BooleanField(default=False)
	
	# Many-to-many relationship with Semester
	semesters = models.ManyToManyField('Semester', related_name='courses', blank=True, help_text="Semesters where this course is offered")
	
	# Add relationships for filtering
	institute = models.ForeignKey('Institute', on_delete=models.CASCADE, null=True, blank=True)
	department = models.ForeignKey('Department', on_delete=models.CASCADE, null=True, blank=True)
	study_program = models.ForeignKey('StudyProgram', on_delete=models.CASCADE, null=True, blank=True)
	curriculum_subject = models.ForeignKey('CurriculumSubject', on_delete=models.CASCADE, null=True, blank=True)
	study_subject = models.ForeignKey('StudySubject', on_delete=models.CASCADE, null=True, blank=True)

	class Meta:
		ordering = ['course_code', 'title']
		indexes = [
			models.Index(fields=['course_code']),
			models.Index(fields=['year']),
		]

	def clean(self):
		"""Validate course code format"""
		from django.core.exceptions import ValidationError
		import re
		
		if self.course_code:
			# Validate course code format (S followed by 5 digits)
			if not re.match(r'^S\d{5}$', self.course_code):
				raise ValidationError({
					'course_code': 'Course code must be in format S followed by 5 digits (e.g., S05618)'
				})
		elif self.course_code == '':
			# Empty string is not allowed since field is unique
			raise ValidationError({
				'course_code': 'Course code cannot be empty'
			})

	def save(self, *args, **kwargs):
		"""Override save to run validation"""
		self.full_clean()
		super().save(*args, **kwargs)

	def __str__(self):
		return f"{self.course_code} - {self.title}" if self.course_code else self.title
	
	@property
	def formatted_course_code(self):
		"""Return formatted course code for display"""
		return self.course_code if self.course_code else "No Code"

class CourseType(models.Model):
	name = models.CharField(max_length=50)
	description = models.TextField()

	def __str__(self):
		return self.name
	
class StudyProgram(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField()
	department = models.ForeignKey('Department', on_delete=models.CASCADE)
	year = models.IntegerField()

	def __str__(self):
		return self.name

class Teacher(models.Model):
	name = models.CharField(max_length=100)
	email = models.EmailField(unique=True)
	# department = models.ForeignKey('Department', on_delete=models.CASCADE)
	subject = models.CharField(max_length=100)

	def __str__(self):
		return self.name

class Institute(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField()

	def __str__(self):
		return self.name

class Department(models.Model):
	name = models.CharField(max_length=100)
	institute = models.ForeignKey(Institute, on_delete=models.CASCADE, related_name='departments')

	def __str__(self):
		return self.name
	
class Curicculum(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField()
	year = models.IntegerField()
	department = models.ForeignKey(Department, on_delete=models.CASCADE)
	courses = models.ManyToManyField(Course, related_name='curriculums')

	def __str__(self):
		return self.name

class Semester(models.Model):
	SEMESTER_CHOICES = [
		('W', 'Winter'),
		('S', 'Summer'),
	]
	
	name = models.CharField(max_length=20, help_text="e.g., 2025W, 2026S")
	year = models.IntegerField(help_text="Academic year")
	season = models.CharField(max_length=1, choices=SEMESTER_CHOICES, help_text="W for Winter, S for Summer")
	start_date = models.DateField(null=True, blank=True)
	end_date = models.DateField(null=True, blank=True)
	is_active = models.BooleanField(default=True, help_text="Is this semester currently active for enrollment")
	
	class Meta:
		unique_together = ['year', 'season']
		ordering = ['-year', '-season']

	def __str__(self):
		return self.name
	
	@property
	def formatted_name(self):
		"""Return formatted name like '2025W' """
		return f"{self.year}{self.season}"

class CurriculumSubject(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField(blank=True)
	study_program = models.ForeignKey(StudyProgram, on_delete=models.CASCADE, related_name='curriculum_subjects')
	credits = models.IntegerField(default=0)
	semester_number = models.IntegerField(help_text="Which semester this subject is taught in")
	is_mandatory = models.BooleanField(default=True)
	
	def __str__(self):
		return f"{self.name} ({self.study_program.name})"

class StudySubject(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField(blank=True)
	curriculum_subject = models.ForeignKey(CurriculumSubject, on_delete=models.CASCADE, related_name='study_subjects')
	credits = models.IntegerField(default=0)
	hours_per_week = models.IntegerField(default=0)
	subject_type = models.CharField(max_length=50, choices=[
		('lecture', 'Lecture'),
		('seminar', 'Seminar'),
		('workshop', 'Workshop'),
		('practical', 'Practical'),
		('project', 'Project'),
		('thesis', 'Thesis'),
	], default='lecture')
	
	def __str__(self):
		return f"{self.name} ({self.curriculum_subject.name})"
	

#User model is not defined here, assuming it is imported from Django's auth models
# If you need to extend the User model, you can create a custom user model or use