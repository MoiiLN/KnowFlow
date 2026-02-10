from django.contrib import admin

from .models import Knowtionary


@admin.register(Knowtionary)
class KnowtionaryAdmin(admin.ModelAdmin):
    pass
