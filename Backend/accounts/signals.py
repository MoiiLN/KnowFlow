from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User

from redis import Redis

from .tasks import send_welcome_email_task, send_goodbye_email_task


def _redis_available() -> bool:
    try:
        queue_conf = settings.RQ_QUEUES.get('default', {})
        host = queue_conf.get('HOST', 'localhost')
        port = queue_conf.get('PORT', 6379)
        db = queue_conf.get('DB', 0)

        client = Redis(host=host, port=port, db=db, socket_connect_timeout=1)
        client.ping()
        return True
    except Exception:
        return False



@receiver(post_save, sender=User)
def on_user_created(sender, instance, created, **kwargs):
    if created and instance.email:
        if _redis_available():
            send_welcome_email_task.delay(instance.username, instance.email)
        else:
            send_welcome_email_task(instance.username, instance.email)



@receiver(post_delete, sender=User)
def on_user_deleted(sender, instance, **kwargs):
    if instance.email:
        if _redis_available():
            send_goodbye_email_task.delay(instance.username, instance.email)
        else:
            send_goodbye_email_task(instance.username, instance.email)

