from django.urls import path
from . import views

urlpatterns = [
    path('', views.input_frame, name='input_frame'),
    path('result/', views.result, name='result'),
]