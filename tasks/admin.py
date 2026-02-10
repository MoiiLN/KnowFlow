from django.contrib import admin

from .models import TaskFlow


@admin.register(TaskFlow)
class TaskFlowAdmin(admin.ModelAdmin):
    pass
