from django.contrib.auth.models import User
from django.db import models

class FileUpload(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class UserProfile(models.Model):

    types_Choices = [
        ('business', 'Business'),
        ('customer', 'Customer'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    username = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    repeated_password = models.CharField(max_length=255)
    type = models.CharField(choices=types_Choices, default='customer', max_length=8)
    # first_name = models.CharField(max_length=30, blank=True, null=True)  # Vorname
    # last_name = models.CharField(max_length=30, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=13, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    working_hours = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    file = models.FileField(upload_to='profile_pictures/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.type}"