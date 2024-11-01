from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    STATUS_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
        ('busy', 'Busy'),
        ('away', 'Away'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='offline')

    def __str__(self):
        return self.username