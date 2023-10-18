from django.urls import path
from . import views

app_name = 'hanwooplz_app'

urlpatterns = [
    path('', views.index, name='index'),
    #path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("login/", views.custom_login, name="login"),
    path("register/", views.register, name="register"),
    path("question_list/", views.question_list, name="question_list"),
    path("question/", views.question_detail, name="question_detail"),
    path("write_question/", views.create_question, name="question"),
    path("myinfo/", views.myinfo, name="myinfo"),
    path("post/", views.post, name="post"),
]