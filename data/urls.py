from django.urls import path
from . import views

app_name = 'data'

urlpatterns = [
     path('visualise/', views.visualise_coordinates, name='visualise_coordinates'),
     path('frames/upload/', views.frames_upload, name='frames_upload'),
     path('session/init/', views.session_init, name='session_init'),
     path('api/init_user/', views.user_init, name='init_user'),
]