from django.db import models


class TaskFlow(models.Model):
    library = models.OneToOneField(
        'library.LibraryContent', on_delete=models.CASCADE, related_name='taskflow'
    )
    name = models.CharField(unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(auto_now_add=True, blank=True)
