from django.urls import path
from . import views

urlpatterns = [
    path('settings/', views.timerflow_settings, name='timerflow_settings'),
    path('settings/update/', views.update_timerflow_settings, name='update_timerflow_settings'),
    path('sessions/', views.studysession_list, name='studysession_list'),
    path('sessions/today-stats/', views.today_stats, name='today_stats'),
    path('sessions/create/', views.create_studysession, name='create_studysession'),
]
