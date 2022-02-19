from django.urls import path
from . import views


app_name = 'audio'
urlpatterns = [
    path('input', views.input, name='input'),
]
