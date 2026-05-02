from django.db import models
from library.models import LibraryContent

class Knowtionary(models.Model):
    content = models.OneToOneField(
        LibraryContent,
        on_delete=models.CASCADE,
        related_name='knowtionary'
    )
    description = models.TextField(blank=True)
    max_score_per_question = models.IntegerField(default=1)
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
    options = models.JSONField(default=list)
    correct_option = models.IntegerField(default=0)
    answer = models.TextField(blank=True)
    image = models.ImageField(upload_to='quiz', blank=True, null=True)

    def __str__(self):
        return self.question