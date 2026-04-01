from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class FlowCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='flowcards')
    library = models.OneToOneField(
        'library.LibraryContent', on_delete=models.CASCADE, related_name='flowcard'
    )
    name = models.CharField(unique=True)
    slug = models.SlugField(unique=True)
    term = models.CharField()
    definition = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)
