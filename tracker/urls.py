from django.urls import path
from .views import UserSignupView, UserLoginView, UserLogoutView, IncompleteGradeCountView

urlpatterns = [
    path('user/signup/', UserSignupView.as_view(), name='user-signup'),
    path('user/login/', UserLoginView.as_view(), name='user-login'),
    path('user/logout/', UserLogoutView.as_view(), name='user-logout'),
    path('missing/marks/', IncompleteGradeCountView.as_view(), name='missing-marks'),
]
