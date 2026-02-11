from django.db import models


class FlowCard(models.Model):
    library = models.OneToOneField(
        'library.LibraryContent', on_delete=models.CASCADE, related_name='flowcard'
    )
    name = models.CharField(unique=True)
    slug = models.SlugField(unique=True)
    term = models.CharField()
    definition = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)
