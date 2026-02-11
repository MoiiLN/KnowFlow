from django.contrib import admin

from .models import FlowCard


@admin.register(FlowCard)
class FlowCardAdmin(admin.ModelAdmin):
    pass
