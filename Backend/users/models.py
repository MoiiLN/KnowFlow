import uuid

from django.conf import settings
from django.db import models


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

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='profile', on_delete=models.CASCADE
    )
    role = models.CharField(max_length=1, choices=Role, default=Role.MEMBER)
    avatar = models.ImageField(upload_to='avatars', default='avatars/noavatar.png', blank=True)
    bio = models.TextField(blank=True)

    def is_member(self):
        return self.role == 'M'

    def __str__(self):
        return f'Perfil de {self.user.username} con el rol {self.role}'
