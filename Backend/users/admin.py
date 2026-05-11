from django.contrib import admin

from .models import Profile, Token


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    pass


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscription_plan')
