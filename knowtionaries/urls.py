from django.urls import path

from . import views

urlpatterns = [
    path('', views.knowtionary_list, name='knowtionary-list'),
    path('<slug:slug>/', views.knowtionary_detail, name='knowtionary-detail'),
    path('add/', views.add_knowtionary, name='add-knowtionary'),
    path('edit/', views.edit_knowtionary, name='edit-knowtionary'),
    path('play/<slug:slug>/', views.play_knowtionary, name='play-knowtionary'),
    path('<slug:slug>/score/', views.knowtionary_score, name='knowtionary-score'),
]
