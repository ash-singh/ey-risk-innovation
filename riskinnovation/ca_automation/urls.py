from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('report', views.report, name='report'),
    path('start-processing', views.start_processing, name='start_processing'),
    
]