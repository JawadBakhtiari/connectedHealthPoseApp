from django.urls import path
from . import views

app_name = 'data'

urlpatterns = [
     path('visualise/', views.visualise_coordinates, name='visualise_coordinates'),
]