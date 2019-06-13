"""riskinnovation URL Configuration
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('ca_automation.urls')),
    path('admin/', admin.site.urls),
]
