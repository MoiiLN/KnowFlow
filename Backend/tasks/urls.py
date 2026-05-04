from django.urls import path

from . import views

urlpatterns = [
    path('<int:id>/delete/', views.delete_task, name='delete-task'),
    path('', views.task_list, name='task-list'),
    path('create/', views.create_task, name='create-task'),
    path('edit/<int:id>/', views.edit_task, name='edit-task'),
    path('<int:id>/', views.task_detail, name='task-detail'),
    path('planner/', views.planner, name='planner'),
]
