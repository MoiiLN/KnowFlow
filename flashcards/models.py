from django.db import models


class FlowCard(models.Model):
    name = models.CharField(unique=True)
    slug = models.SlugField(unique=True)
    term = models.CharField()
    definition = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)
