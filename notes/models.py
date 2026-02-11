from django.db import models


class Note(models.Model):
    library = models.OneToOneField(
        'library.LibraryContent', on_delete=models.CASCADE, related_name='note'
    )
    title = models.CharField(unique=True)
    slug = models.SlugField(unique=True)
    content = models.TextField()
