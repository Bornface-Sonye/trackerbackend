from django.db import models
from django.core.exceptions import ValidationError
import re

class User(models.Model):
    id = models.AutoField(primary_key=True)
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('lecturer', 'Lecturer'),
        ('chair_of_department', 'Chair of Department'),
        ('exam_officer', 'Exam Officer'),
    ]
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    department = models.ForeignKey('Department', null=True, blank=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return self.username

class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

    @classmethod
    def get_default_departments(cls):
        return [
            'Computer Science',
            'Electrical Engineering',
            'Mechanical Engineering',
            'Civil Engineering',
            'Business Administration',
            'Law',
            'Medicine'
        ]
    
    @classmethod
    def create_default_departments(cls):
        """Create default departments in the database."""
        for dept_name in cls.get_default_departments():
            cls.objects.get_or_create(name=dept_name)

class Programme(models.Model):
    id = models.AutoField(primary_key=True)
    PROGRAMME_TYPE_CHOICES = [
        ('degree', 'Degree'),
        ('diploma', 'Diploma'),
        ('certificate', 'Certificate'),
    ]
    
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    programme_type = models.CharField(max_length=11, choices=PROGRAMME_TYPE_CHOICES)
    duration_years = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.name} - {self.programme_type}'


class Course(models.Model):
    id = models.AutoField(primary_key=True)
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE, related_name='courses')
    course_code = models.CharField(max_length=20, unique=True)
    course_name = models.CharField(max_length=200)
    
    def __str__(self):
        return f'{self.course_code} - {self.course_name}'


def validate_academic_year_format(value):
    """Validator to check that the academic year follows the 'YYYY/YYYY' format."""
    if not re.match(r'^\d{4}/\d{4}$', value):
        raise ValidationError(f'{value} is not a valid academic year format. Expected format: YYYY/YYYY')


class AcademicYear(models.Model):
    id = models.AutoField(primary_key=True)
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE, related_name='academic_years')
    year = models.CharField(max_length=9, unique=True, validators=[validate_academic_year_format])

    def __str__(self):
        return self.year

class Semester(models.Model):
    id = models.AutoField(primary_key=True)
    ACADEMIC_YEAR_CHOICES = [
        (1, 'Semester 1'),
        (2, 'Semester 2'),
    ]
    
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='semesters')
    semester_number = models.PositiveIntegerField(choices=ACADEMIC_YEAR_CHOICES)
    
    def __str__(self):
        return f'{self.academic_year.programme.name} - Year {self.academic_year.year} - Semester {self.semester_number}'


class Registration(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registrations')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='registrations')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.student.username} registered for {self.course.course_name} in {self.semester}'


class Result(models.Model):
    id = models.AutoField(primary_key=True)
    registration = models.OneToOneField(Registration, on_delete=models.CASCADE, related_name='result')
    cat_score = models.FloatField(null=True, blank=True)
    exam_score = models.FloatField(null=True, blank=True)
    grade_status = models.CharField(max_length=50, choices=[('incomplete', 'Incomplete'), ('completed', 'Completed')], default='completed')

    def save(self, *args, **kwargs):
        if self.cat_score is None or self.exam_score is None:
            self.grade_status = 'incomplete'
        else:
            self.grade_status = 'completed'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Result for {self.registration.student.username} in {self.registration.course.course_name}'


class Complaint(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complaints')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='complaints')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    complaint_time = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Complaint by {self.student.username} for {self.course.course_name}'


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_time = models.DateTimeField(auto_now_add=True)
    comment_text = models.TextField()

    def __str__(self):
        return f'Comment by {self.user.username} on {self.complaint.course.course_name}'
