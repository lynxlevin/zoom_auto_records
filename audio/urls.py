from django.urls import path
from . import views


app_name = 'audio'
urlpatterns = [
    path('', views.index, name='index'),
    path('input/', views.input, name='input'),
    path('submit/', views.submit, name='submit'),
]
