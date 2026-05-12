from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class FlowCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='flowcards')
    library = models.OneToOneField(
        'library.LibraryContent', on_delete=models.CASCADE, related_name='flowcard', null=True, blank=True
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    term = models.CharField(max_length=255)
    definition = models.TextField()

    class Meta:
        unique_together = ('user', 'name')
    created_at = models.DateTimeField(auto_now_add=True)
