from django.urls import path

from . import views

urlpatterns = [
    path('profile/<str:username>/', views.user_detail, name='user-detail'),
    path('edit-profile/<str:username>/', views.edit_profile, name='edit-profile'),
    path('leave/', views.leave, name='leave'),
    path('api/auth/', views.auth, name='auth'),
    path('api/me/', views.me_api, name='me'),
]
