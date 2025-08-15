from django.db import models

# Create your models here.

class Course(models.Model):
	title = models.CharField(max_length=100)
	description = models.TextField()
	type = models.ForeignKey('CourseType', on_delete=models.CASCADE, null=True, blank=True)
	semester = models.CharField(max_length=20)
	year = models.IntegerField()
	start_date = models.DateField()
	end_date = models.DateField()
	teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, null=True, blank=True)
	credits = models.IntegerField()
	gender_diversity = models.BooleanField(default=False)
	
	# Add relationships for filtering
	institute = models.ForeignKey('Institute', on_delete=models.CASCADE, null=True, blank=True)
	department = models.ForeignKey('Department', on_delete=models.CASCADE, null=True, blank=True)
	study_program = models.ForeignKey('StudyProgram', on_delete=models.CASCADE, null=True, blank=True)

	def __str__(self):
		return self.title

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
	name = models.CharField(max_length=20)

	def __str__(self):
		return self.name
	

#User model is not defined here, assuming it is imported from Django's auth models
# If you need to extend the User model, you can create a custom user model or use