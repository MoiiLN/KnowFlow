from django.db import models


class TaskFlow(models.Model):
    name = models.CharField(unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    completed = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(auto_now_add=True, blank=True)
