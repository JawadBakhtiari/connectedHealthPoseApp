from . import views
from django.urls import path

urlpatterns = [
    path('', views.input_frame, name='input_frame'),
    path('result/', views.result, name='result'),
]