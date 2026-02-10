from django.db import models


class Note(models.Model):
    title = models.CharField(unique=True)
    slug = models.SlugField(unique=True)
    content = models.TextField()
