# example/urls.py
from django.urls import path

from example.views import index


urlpatterns = [
    path('', index),
    # path('test/', index.tester, name='tester'),
    path('api/get_prompt/', index.get_prompt, name='get_prompt'),
    path('api/suggest_input/', index.suggest_input, name='suggest_input'),
    path('api/generate_assistant_ai/', index.generate_assistant_ai, name='generate_assistant_ai'),
    path('api/upload_file/', index.upload_json, name='upload_file'),
]