import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_date
from api.models import Course, Teacher, CourseType, Semester
import re
from datetime import datetime, date


class Command(BaseCommand):
    help = 'Scrape course data from University of Applied Arts Vienna'

    def add_arguments(self, parser):
        parser.add_argument(
            '--pages',
            type=int,
            default=5,
            help='Number of pages to scrape (default: 5)'
        )

    def handle(self, *args, **options):
        base_url = "https://base.uni-ak.ac.at/courses/"
        pages_to_scrape = options['pages']
        
        self.stdout.write(f"Starting to scrape {pages_to_scrape} pages of course data...")
        
        total_courses = 0
        
        for page in range(1, pages_to_scrape + 1):
            self.stdout.write(f"Scraping page {page}...")
            
            try:
                # Request the page
                if page == 1:
                    url = base_url
                else:
                    url = f"{base_url}?page={page}"
                
                response = requests.get(url, timeout=30)
                response.raise_for_status()
                
                # Parse the HTML
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find course entries
                courses_scraped = self.parse_courses(soup)
                total_courses += courses_scraped
                
                self.stdout.write(f"Page {page}: Found {courses_scraped} courses")
                
            except requests.RequestException as e:
                self.stdout.write(
                    self.style.ERROR(f"Error fetching page {page}: {e}")
                )
                continue
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Error processing page {page}: {e}")
                )
                continue
        
        self.stdout.write(
            self.style.SUCCESS(f"Successfully scraped {total_courses} courses total")
        )

    def parse_courses(self, soup):
        """Parse individual courses from the soup object"""
        courses_count = 0
        
        # Look for course links and course information
        # The structure appears to be: course title as link, teacher name, description
        course_links = soup.find_all('a', href=re.compile(r'/courses/\d+[WS]/S\d+/'))
        
        for link in course_links:
            try:
                course_title = link.get_text(strip=True)
                if not course_title:
                    continue
                
                # Find the parent container for this course
                course_container = link.find_parent()
                if not course_container:
                    continue
                
                # Extract teacher name (usually the next text element after the link)
                teacher_name = None
                next_sibling = link.find_next_sibling()
                if next_sibling and next_sibling.name != 'a':
                    teacher_text = next_sibling.get_text(strip=True)
                    if teacher_text and not teacher_text.startswith('—'):
                        teacher_name = teacher_text
                
                # If no teacher found in sibling, look in the next elements
                if not teacher_name:
                    parent = link.parent
                    if parent:
                        # Look for text after the link in the same container
                        remaining_text = parent.get_text()
                        link_text = link.get_text()
                        after_link = remaining_text.split(link_text, 1)
                        if len(after_link) > 1:
                            potential_teacher = after_link[1].strip().split('\n')[0].strip()
                            # Clean up potential teacher name
                            if potential_teacher and not potential_teacher.startswith('—') and not potential_teacher.startswith('–'):
                                potential_teacher = re.sub(r'^[^\w]*', '', potential_teacher)  # Remove leading non-word chars
                                if potential_teacher and len(potential_teacher) < 100:  # Reasonable name length
                                    teacher_name = potential_teacher
                
                # Extract course details from the full text
                full_text = course_container.get_text()
                
                # Extract semester and year from the text (e.g., "2025W", "2026S")
                semester_match = re.search(r'(\d{4}[WS])', full_text)
                semester_str = semester_match.group(1) if semester_match else "2025W"
                
                # Extract ECTS credits
                ects_match = re.search(r'(\d+(?:\.\d+)?)\s*ECTS', full_text)
                credits = float(ects_match.group(1)) if ects_match else 0
                
                # Extract course type (e.g., "Vorlesung und Übungen", "scientific seminar")
                type_patterns = [
                    r'(scientific seminar)',
                    r'(Vorlesung und Übungen)',
                    r'(artistic Seminar)',
                    r'(Lecture and Discussion)',
                    r'(Übungen)',
                    r'(Vorlesung)',
                ]
                
                course_type_name = "General"
                for pattern in type_patterns:
                    type_match = re.search(pattern, full_text, re.IGNORECASE)
                    if type_match:
                        course_type_name = type_match.group(1)
                        break
                
                # Extract description (text between teacher name and semester info)
                description = self.extract_description(full_text, course_title, teacher_name, semester_str)
                
                # Save to database
                self.save_course(
                    title=course_title,
                    teacher_name=teacher_name,
                    description=description,
                    semester_str=semester_str,
                    credits=int(credits) if credits else 0,
                    course_type_name=course_type_name
                )
                
                courses_count += 1
                
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f"Error parsing course '{course_title}': {e}")
                )
                continue
        
        return courses_count

    def extract_description(self, full_text, title, teacher_name, semester_str):
        """Extract course description from the full text"""
        try:
            # Remove the title from the beginning
            text = full_text.replace(title, '', 1).strip()
            
            # Remove teacher name if present
            if teacher_name:
                text = text.replace(teacher_name, '', 1).strip()
            
            # Remove semester info and everything after it
            text = re.sub(f'{semester_str}.*$', '', text, flags=re.DOTALL).strip()
            
            # Clean up the text
            text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
            text = text.strip('—–')  # Remove leading dashes
            
            # Limit description length
            if len(text) > 500:
                text = text[:497] + "..."
            
            return text if text else "No description available"
            
        except:
            return "No description available"

    def save_course(self, title, teacher_name, description, semester_str, credits, course_type_name):
        """Save course data to the database"""
        try:
            # Get or create course type
            course_type, created = CourseType.objects.get_or_create(
                name=course_type_name,
                defaults={'description': f'Course type: {course_type_name}'}
            )
            
            # Get or create teacher
            teacher = None
            if teacher_name and teacher_name.strip():
                # Generate a placeholder email
                email_name = re.sub(r'[^\w\s]', '', teacher_name.lower())
                email_name = re.sub(r'\s+', '.', email_name.strip())
                email = f"{email_name}@uni-ak.ac.at"
                
                teacher, created = Teacher.objects.get_or_create(
                    name=teacher_name.strip(),
                    defaults={
                        'email': email,
                        'subject': 'Arts and Design'
                    }
                )
            
            # Parse semester and year
            year = int(semester_str[:4])
            semester_code = semester_str[4:]  # W or S
            semester_name = f"{year} {'Winter' if semester_code == 'W' else 'Summer'}"
            
            # Get or create semester
            semester, created = Semester.objects.get_or_create(name=semester_name)
            
            # Create default dates (you may want to adjust these)
            if semester_code == 'W':  # Winter semester
                start_date = date(year, 10, 1)  # October 1st
                end_date = date(year + 1, 1, 31)  # January 31st
            else:  # Summer semester
                start_date = date(year, 3, 1)  # March 1st
                end_date = date(year, 6, 30)  # June 30th
            
            # Check if course already exists (avoid duplicates)
            existing_course = Course.objects.filter(
                title=title,
                year=year,
                semester=semester_name
            ).first()
            
            if existing_course:
                self.stdout.write(f"Course '{title}' for {semester_name} already exists, skipping...")
                return
            
            # Create the course
            course = Course.objects.create(
                title=title,
                description=description,
                type=course_type,
                semester=semester_name,
                year=year,
                start_date=start_date,
                end_date=end_date,
                teacher=teacher,
                credits=credits,
                gender_diversity=False  # Default value, could be enhanced
            )
            
            self.stdout.write(f"Created course: {title}")
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Error saving course '{title}': {e}")
            )
