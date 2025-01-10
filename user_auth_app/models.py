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
    type = models.CharField(choices=types_Choices, default='customer', max_length=8) 
    created_at = models.DateTimeField(auto_now_add=True)
    tel = models.CharField(max_length=13, blank=True, null=True, default='')
    location = models.CharField(max_length=100, blank=True, null=True, default='')
    working_hours = models.CharField(max_length=100, blank=True, null=True, default='')
    description = models.CharField(max_length=100, blank=True, null=True, default='')
    file = models.FileField(upload_to='profile_pictures/', null=True, blank=True, default='')
    uploaded_at = models.DateTimeField(auto_now_add=True, null=True)
    

    def __str__(self):
        return f"{self.user.username} - {self.type}"