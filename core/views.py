from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
# ------ rest framework imports -------
from rest_framework.permissions import AllowAny
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
# ------ Permission Classes -------
from education.permissions import IsTeacher, IsAdmin
# ------ Models -------
from .models import User, Student, Teacher
# ------ Serializers -------
from .serializers import AccountSerializer

# for Sign Up, required fields
class SignUpView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = AccountSerializer

# For Forgot Password
class ForgotPasswordView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        data = request.data.copy()      # creating a copy of request data to deal with immutable data
        user = User.objects.get(email = data['email'])
        if user is None:        # if no user is returned from the database
            return Response({'message':'Email not registered. Please check email and try Again.'})
        password = data['new_password']
        if check_password(password, user.password):     # if the password is same as the old one
            return Response({'message':'Password cannot be same as old one'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        password = make_password(password)
        user.password = password
        user.save()
        return Response({'message':'Password Changed Successfully'}, status=status.HTTP_202_ACCEPTED)

# To view profile, accessible by every user
class ProfileView(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = AccountSerializer

    def get_object(self):
        obj = get_object_or_404(User, email=self.request.user.email)
        return obj

    def get_queryset(self):
        return User.objects.get(email=self.request.user.email)

# to create a student user, either a existing user 
# can be made student or a new one can be created,
# can only be accessed by teachers
class StudentCreateView(generics.ListCreateAPIView):       # allowed methods, GET and POST

    queryset = User.objects.all()
    permission_classes = [IsTeacher]
    serializer_class = AccountSerializer

    def get_queryset(self):
        return User.objects.filter(role='S')

    def post(self, request):
        data = request.data.copy()      # creating a copy of request data to deal with immutable data
        if User.objects.filter(email=request.data['email']).exists():       # to check if user already exists
            instance = User.objects.get(email=request.data['email'])
        else:       # if a new user need to be registered or signed up
            data.pop('email')
            data.pop('name')
            if data['password'] is not None:
                password = request.data['password']
                password = make_password(password)
                data.pop('password')
            else:
                # if no password was specified password will be blank
                password = None
            # new user being created
            instance=User.objects.create(email=request.data['email'], name=request.data['name'], password = password)
        role = request.data['role']     # role specified in the request
        # if the role specified is student or not
        if role =='Student' or role == 'S' or role is None:
            Student.objects.create(user=instance)
            group=Group.objects.get_or_create(name='Students')
            instance.groups.add(group[0])
            instance.role = 'S'
        # if the role is other than student, permission will be denied
        else:
            raise PermissionDenied
        instance.save()
        serializer = AccountSerializer(instance=instance)
        return Response(serializer.data)

# to create any user with the role of teacher, student 
# or super-admin, existing or new, can only be accessed 
# by superuser or super-admin
class UserCreateView(generics.ListCreateAPIView):       # allowed methods, GET and POST

    queryset = User.objects.all()
    permission_classes = [IsAdmin]
    serializer_class = AccountSerializer
    
    def post(self, request):
        data = request.data.copy()
        if User.objects.filter(email=request.data['email']).exists():       # to check if user already exists
            instance = User.objects.get(email=request.data['email'])
        else:       # if a new user need to be registered or signed up
            data.pop('email')
            data.pop('name')
            if data['password'] is not None:
                password = request.data['password']
                password = make_password(password)
                data.pop('password')
            else:
                # if no password was specified password will be blank
                password = None
            # new user being created
            instance=User.objects.create(email=request.data['email'], name=request.data['name'], password = password)
        role = request.data['role']         # role specified in the request
        # if the user is a student
        if role =='Student' or role == 'S' or role is None:
            Student.objects.create(user=instance)
            group=Group.objects.get_or_create(name='Students')
            instance.groups.add(group[0])
            instance.role = 'S'
        # if the user needs to be a teacher
        elif role == 'Teacher' or role == 'T':
            Teacher.objects.create(user=instance)
            group=Group.objects.get_or_create(name='Teachers')
            instance.groups.add(group[0])
            instance.role = 'T'
            instance.is_staff = True
        # if the user needs to be a superadmin
        elif role == 'Admin' or role == 'Super-Admin':
            instance.is_staff = True
            instance.is_superuser = True
        instance.save()
        serializer = AccountSerializer(instance=instance)
        return Response(serializer.data)
