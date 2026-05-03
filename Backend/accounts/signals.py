from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .tasks import send_welcome_email_task, send_goodbye_email_task

@receiver(post_save, sender=User)
def on_user_created(sender, instance, created, **kwargs):
    if created and instance.email:
        send_welcome_email_task.delay(instance.username, instance.email)

@receiver(post_delete, sender=User)
def on_user_deleted(sender, instance, **kwargs):
    if instance.email:
        send_goodbye_email_task.delay(instance.username, instance.email)
