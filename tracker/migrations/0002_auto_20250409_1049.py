from django.db import migrations
from tracker.models import Department, Programme, Course, AcademicYear, Semester, Registration, Result, Complaint, Comment, User

from django.db import migrations

def create_default_data(apps, schema_editor):
    # Create a single department
    dept, created = Department.objects.get_or_create(name='Computer Science')

    # Create a single user (student)
    user, created = User.objects.get_or_create(
        username='student1',
        email='student1@example.com',
        password='password123',  # Make sure this is hashed if using a real password
        role='student'
    )
    
    # Create a single programme for the department
    programme, created = Programme.objects.get_or_create(
        name=f'{dept.name} Programme',
        department=dept,
        programme_type='degree',
        duration_years=4
    )

    # Create a single academic year for the programme
    academic_year, created = AcademicYear.objects.get_or_create(
        programme=programme,
        year='2023/2024'
    )

    # Create a single semester for the academic year
    semester, created = Semester.objects.get_or_create(
        academic_year=academic_year,
        semester_number=1
    )

    # Create a single course for the programme
    course, created = Course.objects.get_or_create(
        programme=programme,
        course_code='CS101',  # Unique course code
        course_name=f'{dept.name} 101'
    )

    # Register the student in the course for the semester
    registration, created = Registration.objects.get_or_create(
        student=user,
        course=course,
        semester=semester
    )

    # Create a result for the registration
    result, created = Result.objects.get_or_create(
        registration=registration,
        cat_score=75,
        exam_score=85
    )

    # Create a complaint for the student
    complaint, created = Complaint.objects.get_or_create(
        student=user,
        course=course,
        semester=semester,
        status=Complaint.PENDING,
        description="Complaint about course material"
    )

    # Create a comment on the complaint
    comment, created = Comment.objects.get_or_create(
        complaint=complaint,
        user=user,  # Assuming the user is the one commenting
        comment_text="I have raised an issue regarding the course content."
    )

class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_data),
    ]


def reverse_create_default_data(apps, schema_editor):
    # Reverse the data population (delete the created records)
    Complaint.objects.all().delete()
    Comment.objects.all().delete()
    Result.objects.all().delete()
    Registration.objects.all().delete()
    Semester.objects.all().delete()
    AcademicYear.objects.all().delete()
    Course.objects.all().delete()
    Programme.objects.all().delete()
    User.objects.all().delete()
    Department.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_data, reverse_code=reverse_create_default_data),
    ]
