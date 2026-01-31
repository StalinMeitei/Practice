"""
URL configuration for P1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
import sys
sys.path.insert(0, '/app')
from api_views import get_partners, get_keys, get_messages, get_stats

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pyas2/', include('pyas2.urls')),
    path('api/partners/', get_partners, name='api_partners'),
    path('api/keys/', get_keys, name='api_keys'),
    path('api/messages/', get_messages, name='api_messages'),
    path('api/stats/', get_stats, name='api_stats'),
]
