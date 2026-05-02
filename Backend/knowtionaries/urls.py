from django.urls import path

from . import views

app_name = 'knowtionaries'

urlpatterns = [
    path('', views.knowtionary_list, name='knowtionary-list'),
    path('add/', views.add_knowtionary, name='add-knowtionary'),
    path('edit/<slug:slug>/', views.edit_knowtionary, name='edit-knowtionary'),
    path('delete/<slug:slug>/', views.delete_knowtionary, name='delete-knowtionary'),
    path('favorite/<slug:slug>/', views.toggle_favorite, name='toggle-favorite'),
    path('play/<slug:slug>/', views.play_knowtionary, name='play-knowtionary'),
    path('<slug:slug>/score/', views.knowtionary_score, name='knowtionary-score'),
    path('<slug:slug>/', views.knowtionary_detail, name='knowtionary-detail'),
]
