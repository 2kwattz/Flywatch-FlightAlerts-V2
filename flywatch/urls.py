"""
URL configuration for flywatch project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from flywatch import views
from django.urls import path
from django.contrib import admin
from django.urls import path, include
from . import consumers

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('trackStatus/', views.trackStatus),
    path('api/memory-logs/', views.get_logs_in_memory, name='get_memory_logs'),
    path('api/print-logs/', views.get_print_logs, name='get_print_logs'),
    path('api/server-status/', views.getTaskStatus, name="getTaskStatus"),
      path('admin/', admin.site.urls),
    path('api/auth/', include('dj_rest_auth.urls')),  # Login, logout, and user APIs
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),  # Registration APIs  # Registration APIs
    path('accounts/', include('allauth.urls')),
    path('auth/', include('allauth.urls')),
    path('accounts/profile/', views.profile_view, name='profile'),
    # path('ws/esp8266/', consumers.Esp8266Consumer.as_asgi()),  # This is where ESP8266 connects
]
