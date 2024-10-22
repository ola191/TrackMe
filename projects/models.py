from django.conf import settings
from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_projects')  # Zaktualizowane
    team = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='projects', blank=True)  # Zaktualizowane
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name