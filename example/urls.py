# example/urls.py
from django.urls import path

# from example.views import index

from . import views


urlpatterns = [
    path('', views.index),
    path('api/get_prompt/', views.get_prompt, name='get_prompt'),
    path('api/suggest_input/', views.suggest_input, name='suggest_input'),
    path('api/generate_assistant_ai/', views.generate_assistant_ai, name='generate_assistant_ai'),
    path('api/upload_file/', views.upload_json, name='upload_file'),
]