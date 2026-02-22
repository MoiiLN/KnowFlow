from django.db import models
from library.models import LibraryContent

class Knowtionary(models.Model):
    content = models.OneToOneField(
        LibraryContent,
        on_delete=models.CASCADE,
        related_name='quiz'
    )
    description = models.TextField(blank=True)

class Question(models.Model):
    quiz = models.ForeignKey(
        Knowtionary,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    question = models.CharField(max_length=255)
    answer = models.TextField()
    image = models.ImageField(upload_to='quiz', blank=True, null=True)