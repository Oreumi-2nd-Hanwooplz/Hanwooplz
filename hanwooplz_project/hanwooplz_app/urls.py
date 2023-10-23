from django.urls import path, include
from . import views
from .views import LoginView

app_name = 'hanwooplz_app'

urlpatterns = [
    path('', views.main, name='main'),
    path('index/',views.index, name='index'),
    path('write/',views.write, name='write'),
    path('chat/', views.current_chat, name='chat'),
    #path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path('login/', LoginView.as_view(), name="login"),
    path('register/', views.register, name='register'),
    path("question_list/", views.question_list, name="question_list"),
    path("question/", views.question_detail, name="question_detail"),
    path("write_question/", views.create_question, name="question"),
    path("myinfo/", views.myinfo, name="myinfo"),
    path("post/", views.post, name="post"),
    path('execute_chatbot/', views.execute_chatbot, name='execute_chatbot'),
]