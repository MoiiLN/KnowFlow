from django.conf import settings
from django.db import models


class TimerFlow(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='timersflow'
    )
    default_minutes = models.IntegerField(default=25)
    short_break = models.IntegerField(default=5)
    long_break = models.IntegerField(default=15)
    cycle_before_long_break = models.IntegerField(default=4)

    def __str__(self):
        return self.default_minutes


class StudySession(models.Model):
    class SessionType(models.TextChoices):
        WORK = 'work', 'Work'
        SHORT_BREAK = 'short_break', 'Short Break'
        LONG_BREAK = 'long_break', 'Long Break'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='studysessions'
    )
    planned_minutes = models.IntegerField()  #
    session_type = models.CharField(choices=SessionType.choices)
    completed = models.BooleanField(default=False)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.session_type
