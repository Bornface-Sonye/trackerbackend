from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
import json
from .models import User
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password


from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
import json
from .models import User

from django.http import JsonResponse
from django.views import View
from django.contrib.auth.models import User
from .models import Complaint

@method_decorator(csrf_exempt, name='dispatch')
class UserSignupView(View):

    def patch(self, request):
        try:
            data = json.loads(request.body)

            email = data.get('Email')  # Use email to locate the user
            if not email:
                return JsonResponse({'message': 'Email is required to identify the user.'}, status=400)

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return JsonResponse({'message': 'User with this email does not exist.'}, status=404)

            username = data.get('Username')
            password = data.get('PasswordHash')
            confirm_password = data.get('ConfirmPassword')

            if username:
                if User.objects.filter(username=username).exclude(email=email).exists():
                    return JsonResponse({'message': 'Username already taken by another user.'}, status=400)
                user.username = username

            if password or confirm_password:
                if password != confirm_password:
                    return JsonResponse({'message': 'Passwords do not match.'}, status=400)
                user.password = make_password(password)

            user.save()
            return JsonResponse({'message': 'User updated successfully.'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON.'}, status=400)
        except Exception as e:
            return JsonResponse({'message': f'An error occurred: {str(e)}'}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class UserLoginView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            username = data.get('Username')
            password = data.get('Password')

            if not username or not password:
                return JsonResponse({'message': 'Username and password are required.'}, status=400)

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return JsonResponse({'message': 'Invalid credentials.'}, status=401)

            if not check_password(password, user.password):
                return JsonResponse({'message': 'Invalid credentials.'}, status=401)

            # Store user info in session
            request.session['user_id'] = user.id
            request.session['username'] = user.username

            return JsonResponse({'message': 'Login successful.'})
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON.'}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class UserLogoutView(View):
    def post(self, request, *args, **kwargs):
        try:
            # Clear the session data
            request.session.flush()  # This will delete all session data

            return JsonResponse({'message': 'Logout successful.'}, status=200)
        except Exception as e:
            return JsonResponse({'message': f'An error occurred: {str(e)}'}, status=500)

class ComplaintView(View):
    def get(self, request, username):
        try:
            # Get the user by the provided username
            user = User.objects.get(username=username)
            
            # Retrieve all complaints related to the user
            complaints = Complaint.objects.filter(student=user)
            
            # Prepare data to return
            complaints_data = [
                {
                    'id': complaint.id,
                    'course': complaint.course.course_name,
                    'semester': complaint.semester.name,
                    'complaint_time': complaint.complaint_time,
                    'is_resolved': complaint.is_resolved
                }
                for complaint in complaints
            ]
            
            return JsonResponse({'complaints': complaints_data}, status=200)

        except User.DoesNotExist:
            # If the user does not exist
            return JsonResponse({'error': 'User not found'}, status=404)

