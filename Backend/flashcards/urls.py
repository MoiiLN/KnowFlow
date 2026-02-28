from django.urls import path
from . import views

urlpatterns = [
    path('flowcards/', views.flowcard_list),
    path('flowcards/add/', views.add_flowcard),
    path('flowcards/<slug:slug>/', views.flowcard_detail),
    path('flowcards/<slug:slug>/edit/', views.edit_flowcard),
    path('flowcards/<slug:slug>/play/', views.play_flowcard),
]
