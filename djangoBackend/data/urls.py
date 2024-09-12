from django.urls import path
from . import views

app_name = 'data'

urlpatterns = [
     path('visualise2D/', views.visualise_2D, name='visualise_2D'),
     path('poses/upload/', views.poses_upload, name='frames_upload'),
     path('video/upload/', views.video_upload, name='video_upload'),
     path('session/init/', views.session_init, name='session_init'),
     path('api/init_user/', views.user_init, name='init_user'),
]