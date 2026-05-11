import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone

class Token(models.Model):
    key = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.key)

class Profile(models.Model):
    class Role(models.TextChoices):
        MEMBER = 'M', 'Member'
        KNOWER = 'K', 'Knower'

    class SubscriptionPlan(models.TextChoices):
        FREE = 'free', 'Free'
        PREMIUM = 'premium', 'Premium'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='profile',
        on_delete=models.CASCADE
    )

    role = models.CharField(
        max_length=1,
        choices=Role,
        default=Role.MEMBER
    )

    subscription_plan = models.CharField(
        max_length=20,
        choices=SubscriptionPlan,
        default=SubscriptionPlan.FREE
    )
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True)
    bio = models.TextField(blank=True)
    streak = models.IntegerField(default=1)
    last_active_date = models.DateField(default=timezone.now)
    
    def is_premium(self):
        return self.subscription_plan == self.SubscriptionPlan.PREMIUM
    def __str__(self):
        return f'Perfil de {self.user.username} con el rol {self.subscription_plan}'
        