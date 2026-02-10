from django.db import models


class Knowtionary(models.Model):
    name = models.CharField(unique=True)
    slug = models.SlugField(unique=True)
    description = models.CharField(blank=True)
    question = models.CharField()
    answer = models.CharField()
    image = models.ImageField(
        models.ImageField(upload_to='media', default='media/default.png', blank=True, null=True)
    )
    created_at = models.DateTimeField(auto_now_add=True)
