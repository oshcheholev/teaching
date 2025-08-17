from django.core.management.base import BaseCommand
from django.db import transaction
from api.models import Course, Teacher, Department, Institute
import json
import os

class Command(BaseCommand):
    help = 'Load course data from scraped JSON file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default='scraped_course_data.json',
            help='JSON file containing scraped course data'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before loading new data'
        )

    def handle(self, *args, **options):
        file_path = options['file']
        
        if not os.path.exists(file_path):
            self.stdout.write(
                self.style.ERROR(f'File {file_path} does not exist')
            )
            return

        # Clear existing data if requested
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            Course.objects.all().delete()
            Teacher.objects.all().delete()
            Department.objects.all().delete()
            Institute.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Existing data cleared'))

        # Load data from JSON file
        self.stdout.write(f'Loading data from {file_path}...')
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error reading file: {e}')
            )
            return

        with transaction.atomic():
            # Create departments
            self.stdout.write('Creating departments...')
            departments = {}
            for dept_name in data.get('departments', []):
                dept, created = Department.objects.get_or_create(
                    name=dept_name,
                    defaults={'description': f'Department of {dept_name}'}
                )
                departments[dept_name] = dept
                if created:
                    self.stdout.write(f'  Created department: {dept_name}')

            # Create institutes
            self.stdout.write('Creating institutes...')
            institutes = {}
            for inst_name in data.get('institutes', []):
                inst, created = Institute.objects.get_or_create(
                    name=inst_name,
                    defaults={'description': f'Institute for {inst_name}'}
                )
                institutes[inst_name] = inst
                if created:
                    self.stdout.write(f'  Created institute: {inst_name}')

            # Create teachers
            self.stdout.write('Creating teachers...')
            teachers = {}
            for teacher_data in data.get('teachers', []):
                # Get or create department
                dept_name = teacher_data.get('department', 'Applied Arts')
                department = departments.get(dept_name)
                
                if not department:
                    department, _ = Department.objects.get_or_create(
                        name=dept_name,
                        defaults={'description': f'Department of {dept_name}'}
                    )
                    departments[dept_name] = department

                teacher, created = Teacher.objects.get_or_create(
                    name=teacher_data['name'],
                    defaults={
                        'email': teacher_data.get('email', ''),
                        'department': department,
                        'bio': teacher_data.get('bio', '')
                    }
                )
                teachers[teacher_data['name']] = teacher
                if created:
                    self.stdout.write(f'  Created teacher: {teacher_data["name"]}')

            # Create courses
            self.stdout.write('Creating courses...')
            courses_created = 0
            for course_data in data.get('courses', []):
                # Get teacher
                teacher_name = course_data.get('teacher', 'Unknown Teacher')
                teacher = teachers.get(teacher_name)
                
                if not teacher:
                    # Create unknown teacher if not exists
                    dept_name = course_data.get('department', 'Applied Arts')
                    department = departments.get(dept_name)
                    if not department:
                        department, _ = Department.objects.get_or_create(
                            name=dept_name,
                            defaults={'description': f'Department of {dept_name}'}
                        )
                    
                    teacher, _ = Teacher.objects.get_or_create(
                        name=teacher_name,
                        defaults={
                            'email': f"{teacher_name.lower().replace(' ', '.')}@uni-ak.ac.at",
                            'department': department,
                            'bio': f'Faculty member at University of Applied Arts Vienna'
                        }
                    )
                    teachers[teacher_name] = teacher

                # Get department and institute
                dept_name = course_data.get('department', 'Applied Arts')
                inst_name = course_data.get('institute', 'General Studies')
                
                department = departments.get(dept_name)
                institute = institutes.get(inst_name)
                
                # Create if not exists
                if not department:
                    department, _ = Department.objects.get_or_create(
                        name=dept_name,
                        defaults={'description': f'Department of {dept_name}'}
                    )
                    departments[dept_name] = department
                
                if not institute:
                    institute, _ = Institute.objects.get_or_create(
                        name=inst_name,
                        defaults={'description': f'Institute for {inst_name}'}
                    )
                    institutes[inst_name] = institute

                # Create course
                course, created = Course.objects.get_or_create(
                    course_code=course_data.get('course_code', 'UNKNOWN'),
                    defaults={
                        'title': course_data.get('title', 'Unknown Course'),
                        'description': course_data.get('description', ''),
                        'credits': course_data.get('credits', 2.0),
                        'semester': course_data.get('semester', 'Unknown'),
                        'year': course_data.get('year', 2025),
                        'teacher': teacher,
                        'department': department,
                        'institute': institute,
                        'course_type': course_data.get('course_type', 'Unknown')
                    }
                )
                
                if created:
                    courses_created += 1
                    if courses_created % 10 == 0:
                        self.stdout.write(f'  Created {courses_created} courses...')

        # Summary
        self.stdout.write(
            self.style.SUCCESS(
                f'\nData loading complete!\n'
                f'Departments: {Department.objects.count()}\n'
                f'Institutes: {Institute.objects.count()}\n'
                f'Teachers: {Teacher.objects.count()}\n'
                f'Courses: {Course.objects.count()}\n'
                f'New courses created: {courses_created}'
            )
        )
