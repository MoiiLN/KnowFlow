from django.conf import settings
from django.db import models
from django.urls import reverse


class Course(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField()


class Subject(models.Model):
    code = models.CharField(unique=True)
    name = models.CharField()
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='teaching', on_delete=models.PROTECT
    )
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='enrolled', through='subjects.Enrollment', blank=True
    )

    def __str__(self):
        return f'Code: {self.code} | Módulo: {self.teacher} | Teacher: {self.teacher}'

    def get_absolute_url(self):
        return reverse('subject-detail', args=[self.code])


class Lesson(models.Model):
    subject = models.ForeignKey(
        'subjects.Subject', related_name='lessons', on_delete=models.CASCADE
    )
    title = models.CharField()
    content = models.TextField(blank=True)

    def __str__(self):
        return f'PK: {self.pk} | Titulo {self.title}'

    def get_absolute_url(self):
        return reverse('lesson-detail', args=[self.pk, self.subject.code])
