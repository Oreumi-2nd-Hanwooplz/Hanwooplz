from django.urls import path, include
from . import views

app_name = 'hanwooplz_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('write/',views.write, name='write'),
    path('chat/', views.current_chat, name='chat'),
]