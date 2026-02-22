from django.conf import settings
from django.db import models
from library.models import LibraryContent

class Note(models.Model):
    content = models.OneToOneField(
        LibraryContent,
        on_delete=models.CASCADE,
        related_name='note'
    )
    text = models.TextField(blank=True)
    file = models.FileField(upload_to='notes/', blank=True, null=True)