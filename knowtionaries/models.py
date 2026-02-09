from django.db import models


class Knowtionary(models.Model):
    name = models.CharField()
    description = models.CharField(blank=True)
    question = models.CharField()
    answer = models.CharField()
    image = models.ImageField(
        models.ImageField(upload_to='media', default='media/default.png', blank=True)
    )
