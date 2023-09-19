from django.urls import path
from . import views

app_name = 'data'

urlpatterns = [
     path('visualise3D/', views.visualise_3D, name='visualise_3D'),
     path('visualise2D/', views.visualise_2D, name='visualise_2D'),
     path('frames/upload/', views.frames_upload, name='frames_upload'),
     path('session/init/', views.session_init, name='session_init'),
     path('api/init_user/', views.user_init, name='init_user'),
]