
# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Assuming 'name' is additional to the standard 'first_name' and 'last_name'
    name = models.CharField(max_length=255, null=True, blank=True)
    # Gender field with choices
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, null=True, blank=True)
