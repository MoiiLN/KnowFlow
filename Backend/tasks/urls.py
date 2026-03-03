from django.urls import path

from . import views

urlpatterns = [
    path('', views.task_list, name='task-list'),
    path('<slug:slug>/', views.task_detail, name='task-detail'),
    path('create/', views.create_task, name='create-task'),
    path('<slug:slug>/update/', views.edit_task, name='edit-task'),
    path('<slug:slug>/delete/', views.delete_task, name='delete-task'),
]
