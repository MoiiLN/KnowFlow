from django.conf import settings
from django.db import models


class Note(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='libraries'
    )
    library = models.OneToOneField(
        'library.LibraryContent', on_delete=models.CASCADE, related_name='note'
    )
    title = models.CharField(unique=True)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class UploadNote(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='libraries'
    )
    library = models.OneToOneField(
        'library.LibraryContent', on_delete=models.CASCADE, related_name='note'
    )
    title = models.CharField(unique=True)
    slug = models.SlugField(unique=True)
    file = models.FileField(upload_to='media/notes/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
