from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('report', views.report, name='report'),
    path('start-initial-processing', views.start_initial_processing, name='start_initial_processing'),
    path('start-complete-processing', views.start_complete_processing, name='start_complete_processing'),
    path('download/<str:file_type>', views.download, name='file_download')
    
]

