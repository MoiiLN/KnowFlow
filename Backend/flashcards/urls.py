from django.urls import path
from . import views

urlpatterns = [
    path('', views.flowcard_list, name='flowcard_list'),
    path('add/', views.add_flowcard, name='add_flowcard'),
    path('<slug:slug>/', views.flowcard_detail, name='flowcard_detail'),
    path('<slug:slug>/edit/', views.edit_flowcard, name='edit_flowcard'),
    path('<slug:slug>/play/', views.play_flowcard, name='play_flowcard'),
]
