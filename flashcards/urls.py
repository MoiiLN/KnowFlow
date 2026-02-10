from django.urls import path

from . import views

urlpatterns = [
    path('', views.flowcard_list, name='flowcard-list'),
]
