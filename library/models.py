from django.conf import settings
from django.db import models


class Library(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='libraries'
    )
    name = models.CharField(unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class LibraryContent(models.Model):
    class ContentType(models.TextChoices):
        FLOWCARD = 'flowcard', 'Flowcard'
        NOTE = 'note', 'Note'
        TASK = 'task', 'Task'
        KNOWTIONARY = 'knowtionary', 'Knowtionary'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contents'
    )
    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name='contents')
    title = models.CharField(unique=True)
    content_type = models.CharField(choices=ContentType.choices)
    is_favorite = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
