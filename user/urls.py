from django.urls import path
from . import views


app_name = 'user'
urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
]
