# ------ imports -------
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import EmailValidator

# user manager for custom user model
class CustomAccountManager(BaseUserManager):

    # super user or super admin only being created through django terminal
    def create_superuser(self, email, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, password, **other_fields)

    def create_user(self, email, password=None, **other_fields):
        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user

# ------ User Model -------
class User(AbstractBaseUser, PermissionsMixin):

    ROLE_CHOICES = (
        ('T', 'Teacher'),
        ('S', 'Student'),
        ('A', 'Super-Admin'),
    )

    # ------ Fields for Profile -------
    email = models.EmailField(_('email address'), validators=[EmailValidator()], unique=True)
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=1, choices=ROLE_CHOICES, null=True)
    
    # ------ Boolean Fields not to be accesed directly through User Profile -------
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) # if this is true, implies user is a teacher

    # ------ Timestamp for user Created -------
    created = models.DateTimeField(auto_now_add=True)

    # ------ Account Manager for Custom User Model -------
    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teacher')

    def __str__(self) -> str:
        return self.user.name

class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student')