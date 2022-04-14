from django.urls import path
from . import views

urlpatterns = [
    path('sign-up/', views.SignUpView.as_view()),      # API for user sign-up
    path('forgot-password/', views.ForgotPasswordView.as_view()),       # API for forgot password
    path('profile/', views.ProfileView.as_view()),      # API to view a user profile
    path('student-create/', views.StudentCreateView.as_view()),     # API for teachers to create a student profile
    path('user-create/', views.UserCreateView.as_view()),       # API for admin to create any profile
]
