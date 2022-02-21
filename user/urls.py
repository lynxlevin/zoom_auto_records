from django.urls import path
from . import views


app_name = 'user'
urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('zoom/auth/init/', views.zoom_init, name='zoom_init'),
    path('zoom/auth/return/', views.zoom_return, name='zoom_return'),
]
