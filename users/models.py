from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import CustomUserManager
from django.db import models

GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
]


BLOOD_GROUP_CHOICES = [
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('O+', 'O+'),
    ('O-', 'O-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
]


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True, help_text= "Enter the date formate year-month-day")
    gender = models.CharField(max_length=255, choices=GENDER_CHOICES)
    blood_group = models.CharField(max_length=3, null= True, blank= True, choices=BLOOD_GROUP_CHOICES)
    image = models.ImageField(upload_to='images/profileImage/', null=True)
    date_joined = models.DateField(default=timezone.now)
    last_update = models.DateField(auto_now = True)
    is_email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.username
    
    
    objects = CustomUserManager()