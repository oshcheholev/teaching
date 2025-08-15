
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Course, CourseType, StudyProgram, Teacher, Department, Curicculum, Institute

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'is_staff', 'is_active', 'date_joined')
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class CourseSerializer(serializers.ModelSerializer):
	class Meta:
		model = Course
		fields = '__all__'
		read_only_fields = ['id']
		depth = 1

class CourseWriteSerializer(serializers.ModelSerializer):
	class Meta:
		model = Course
		fields = '__all__'
		read_only_fields = ['id']
		# No depth for write operations - allows foreign key IDs

class CourseTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = CourseType
		fields = '__all__'
		read_only_fields = ['id']
		depth = 1

class StudyProgramSerializer(serializers.ModelSerializer):
	class Meta:
		model = StudyProgram
		fields = '__all__'
		read_only_fields = ['id']
		depth = 1

class StudyProgramWriteSerializer(serializers.ModelSerializer):
	class Meta:
		model = StudyProgram
		fields = '__all__'
		read_only_fields = ['id']
		# No depth for write operations - allows foreign key IDs

class TeacherSerializer(serializers.ModelSerializer):
	class Meta:
		model = Teacher
		fields = '__all__'
		read_only_fields = ['id']
		depth = 1

class TeacherWriteSerializer(serializers.ModelSerializer):
	class Meta:
		model = Teacher
		fields = '__all__'
		read_only_fields = ['id']
		# No depth for write operations

class DepartmentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Department
		fields = '__all__'
		read_only_fields = ['id']
		depth = 1

class DepartmentWriteSerializer(serializers.ModelSerializer):
	class Meta:
		model = Department
		fields = '__all__'
		read_only_fields = ['id']
		# No depth for write operations - allows foreign key IDs

class InstituteSerializer(serializers.ModelSerializer):
	class Meta:
		model = Institute
		fields = '__all__'
		read_only_fields = ['id']
		depth = 1

class CuricculumSerializer(serializers.ModelSerializer):
	class Meta:
		model = Curicculum
		fields = '__all__'
		read_only_fields = ['id']
		depth = 1

# User serializer for creating users
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user