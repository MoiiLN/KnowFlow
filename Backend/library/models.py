from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class Library(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='libraries'
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'name')
        verbose_name_plural = "Libraries"

    def __str__(self):
        return self.name


class LibraryContent(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='library_contents'
    )
    library = models.ForeignKey(
        'library.Library',
        on_delete=models.CASCADE,
        related_name='contents'
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField()
    is_favorite = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('library', 'slug')

    def __str__(self):
        return self.title