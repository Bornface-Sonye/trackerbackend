from django.contrib import admin
from .models import User, Department, Programme, Course, AcademicYear, Semester, Registration, Result, Complaint, Comment

# List of all the models you want to register
models = [User, Department, Programme, Course, AcademicYear, Semester, Registration, Result, Complaint, Comment]

# Loop through the models and register them in the admin site
for model in models:
    admin.site.register(model)
