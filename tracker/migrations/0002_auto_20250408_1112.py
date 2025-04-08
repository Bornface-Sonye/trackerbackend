from django.db import migrations
from django.utils import timezone

def seed_data(apps, schema_editor):
    Department = apps.get_model('tracker', 'Department')
    User = apps.get_model('tracker', 'User')
    Programme = apps.get_model('tracker', 'Programme')
    Course = apps.get_model('tracker', 'Course')
    AcademicYear = apps.get_model('tracker', 'AcademicYear')
    Semester = apps.get_model('tracker', 'Semester')
    Registration = apps.get_model('tracker', 'Registration')
    Result = apps.get_model('tracker', 'Result')
    Complaint = apps.get_model('tracker', 'Complaint')
    Comment = apps.get_model('tracker', 'Comment')

    # Departments
    departments = {}
    for name in [
        'Computer Science', 'Electrical Engineering', 'Mechanical Engineering',
        'Civil Engineering', 'Business Administration', 'Law', 'Medicine'
    ]:
        dept, _ = Department.objects.get_or_create(name=name)
        departments[name] = dept

    # Users
    student = User.objects.create(
        username='student1',
        email='student1@student.mmust.ac.ke',
        password='studentpass',
        role='student',
        department=departments['Computer Science']
    )

    lecturer = User.objects.create(
        username='lecturer1',
        email='lecturer1@mmust.ac.ke',
        password='lecturerpass',
        role='lecturer',
        department=departments['Computer Science']
    )

    # Programme
    programme = Programme.objects.create(
        name='BSc Computer Science',
        department=departments['Computer Science'],
        programme_type='degree',
        duration_years=4
    )

    # Course
    course = Course.objects.create(
        programme=programme,
        course_code='CSC101',
        course_name='Introduction to Programming'
    )

    # Academic Year
    academic_year = AcademicYear.objects.create(
        programme=programme,
        year='2024/2025'
    )

    # Semester
    semester = Semester.objects.create(
        academic_year=academic_year,
        semester_number=1
    )

    # Registration
    registration = Registration.objects.create(
        student=student,
        course=course,
        semester=semester
    )

    # Result
    Result.objects.create(
        registration=registration,
        cat_score=15.0,
        exam_score=55.0
    )

    # Complaint
    complaint = Complaint.objects.create(
        student=student,
        course=course,
        semester=semester,
        complaint_time=timezone.now(),
        is_resolved=False
    )

    # Comment
    Comment.objects.create(
        complaint=complaint,
        user=lecturer,
        comment_time=timezone.now(),
        comment_text='This issue is under review.'
    )

class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_data),
    ]
