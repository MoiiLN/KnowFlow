from django.urls import path

from . import views

urlpatterns = [
    path('', views.note_list, name='note-list'),
    path('add/', views.add_note, name='add-note'),
    path('<slug:slug>/', views.note_detail, name='note-detail'),
    path('edit/<slug:slug>/', views.edit_note, name='edit-note'),
]
