from django.db import models
from library.models import LibraryContent

class Knowtionary(models.Model):
    content = models.OneToOneField(
        LibraryContent,
        on_delete=models.CASCADE,
        related_name='knowtionary'
    )
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content.title

class Question(models.Model):
    quiz = models.ForeignKey(
        Knowtionary,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    question = models.TextField(max_length=255)
    answer = models.TextField()
    image = models.ImageField(upload_to='quiz', blank=True, null=True)