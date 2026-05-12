from django.urls import path
from . import views

urlpatterns = [
    path('', views.library_list, name='library_list'),
    path('<int:library_id>/', views.library_detail, name='library_detail'),
    path('create/', views.create_library, name='create_library'),
    path('<int:library_id>/edit/', views.edit_library, name='edit_library'),
    path('<int:library_id>/delete/', views.delete_library, name='delete_library'),
    path('run-migrations/', views.run_migrations, name='run_migrations'),
]

