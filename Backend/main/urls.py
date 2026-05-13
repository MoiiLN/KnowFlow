"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('users.urls')),
    path('api/tasks/', include('tasks.urls')),
    path('api/notes/', include('notes.urls')),
    path('api/flowcards/', include('flashcards.urls')),
    path('api/knowtionaries/', include('knowtionaries.urls')),
    path('api/libraries/', include('library.urls')),
    path('api/timerflow/', include('timerflow.urls')),
    path('django-rq/', include('django_rq.urls')),
]


# Forzar la entrega de archivos estáticos y media incluso bajo Gunicorn en este entorno
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# También incluir STATICFILES_DIRS para desarrollo
from django.contrib.staticfiles.views import serve
from django.urls import re_path

if settings.DEBUG:
    for static_dir in settings.STATICFILES_DIRS:
        urlpatterns += [
            re_path(r'^static/(?P<path>.*)$', serve, {'document_root': static_dir}),
        ]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
