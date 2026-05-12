from django.db import models
from django.contrib.auth.models import User


class TaskFlow(models.Model):

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='taskflows'
    )

    library = models.OneToOneField(
        'library.LibraryContent',
        on_delete=models.CASCADE,
        related_name='taskflow'
    )

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True)
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='medium'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    due_date = models.DateField(null=True,blank=True)
    due_time = models.TimeField(null=True, blank=True)
    reminder = models.DateTimeField(null=True, blank=True)

    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['due_date', 'due_time']

    def __str__(self):
        return self.name