from django.core.management.base import BaseCommand
from api.models import CourseType, Institute, Department, StudyProgram

class Command(BaseCommand):
    help = 'Populate database with sample data for filters'

    def handle(self, *args, **options):
        # Create sample CourseTypes
        course_types = [
            {'name': 'Seminar', 'description': 'Interactive seminar course'},
            {'name': 'Vorlesung', 'description': 'Traditional lecture course'},
            {'name': 'Workshop', 'description': 'Hands-on workshop course'},
            {'name': 'Studio', 'description': 'Creative studio course'},
            {'name': 'Praktikum', 'description': 'Practical internship course'},
            {'name': 'Übung', 'description': 'Exercise course'},
        ]

        for ct_data in course_types:
            course_type, created = CourseType.objects.get_or_create(
                name=ct_data['name'],
                defaults={'description': ct_data['description']}
            )
            if created:
                self.stdout.write(f'Created CourseType: {course_type.name}')

        # Create sample Institutes
        institutes = [
            {'name': 'Institute of Fine Arts', 'description': 'Fine arts and visual arts institute'},
            {'name': 'Institute of Design', 'description': 'Design and applied arts institute'},
            {'name': 'Institute of Media Arts', 'description': 'Digital and new media arts institute'},
            {'name': 'Institute of Applied Arts', 'description': 'Applied arts and crafts institute'},
            {'name': 'Institute of Art Sciences', 'description': 'Art theory and history institute'},
        ]

        institute_objects = {}
        for inst_data in institutes:
            institute, created = Institute.objects.get_or_create(
                name=inst_data['name'],
                defaults={'description': inst_data['description']}
            )
            institute_objects[institute.name] = institute
            if created:
                self.stdout.write(f'Created Institute: {institute.name}')

        # Create sample Departments
        departments = [
            {'name': 'Painting', 'institute': 'Institute of Fine Arts'},
            {'name': 'Sculpture', 'institute': 'Institute of Fine Arts'},
            {'name': 'Graphics', 'institute': 'Institute of Design'},
            {'name': 'Industrial Design', 'institute': 'Institute of Design'},
            {'name': 'Digital Art', 'institute': 'Institute of Media Arts'},
            {'name': 'Photography', 'institute': 'Institute of Media Arts'},
            {'name': 'Textile Design', 'institute': 'Institute of Applied Arts'},
            {'name': 'Ceramics', 'institute': 'Institute of Applied Arts'},
            {'name': 'Art History', 'institute': 'Institute of Art Sciences'},
            {'name': 'Art Theory', 'institute': 'Institute of Art Sciences'},
        ]

        department_objects = {}
        for dept_data in departments:
            institute = institute_objects[dept_data['institute']]
            department, created = Department.objects.get_or_create(
                name=dept_data['name'],
                defaults={'institute': institute}
            )
            department_objects[department.name] = department
            if created:
                self.stdout.write(f'Created Department: {department.name}')

        # Create sample StudyPrograms
        study_programs = [
            {'name': 'Bachelor Fine Arts', 'description': 'Bachelor degree in fine arts', 'department': 'Painting', 'year': 2024},
            {'name': 'Master Fine Arts', 'description': 'Master degree in fine arts', 'department': 'Painting', 'year': 2024},
            {'name': 'Bachelor Design', 'description': 'Bachelor degree in design', 'department': 'Graphics', 'year': 2024},
            {'name': 'Master Design', 'description': 'Master degree in design', 'department': 'Graphics', 'year': 2024},
            {'name': 'Digital Arts Program', 'description': 'Specialized program in digital arts', 'department': 'Digital Art', 'year': 2024},
            {'name': 'Photography Studies', 'description': 'Comprehensive photography program', 'department': 'Photography', 'year': 2024},
            {'name': 'Applied Arts Program', 'description': 'Applied arts and crafts program', 'department': 'Textile Design', 'year': 2024},
            {'name': 'Art History Program', 'description': 'Art history and theory program', 'department': 'Art History', 'year': 2024},
        ]

        for sp_data in study_programs:
            department = department_objects[sp_data['department']]
            study_program, created = StudyProgram.objects.get_or_create(
                name=sp_data['name'],
                defaults={
                    'description': sp_data['description'],
                    'department': department,
                    'year': sp_data['year']
                }
            )
            if created:
                self.stdout.write(f'Created StudyProgram: {study_program.name}')

        self.stdout.write(self.style.SUCCESS('Successfully populated database with sample data'))
