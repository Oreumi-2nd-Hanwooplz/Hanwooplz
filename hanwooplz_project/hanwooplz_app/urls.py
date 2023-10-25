from django.urls import path, include
from .views import views, chat_views, comment_views, question_views


app_name = 'hanwooplz_app'

urlpatterns = [
    path('', views.main, name='main'),
    path('index/',views.index, name='index'),
    path('write/',views.write, name='write'),
    path('chat/<int:room_number>/<int:receiver_id>', chat_views.current_chat, name='chat'),
    path('chat_msg/<int:room_number>', chat_views.chat_msg, name='chat_msg'),
    #path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path('login/', views.LoginView.as_view(), name="login"),
    path("logout/", views.log_out, name="logout"),
    path('register/', views.register, name='register'),
    path("question_list/", question_views.question_list, name="question_list"),
    path("question_detail/<int:post_id>", question_views.question_detail, name="question_detail"),
    path("write_question/", question_views.write_question, name="write_question"),
    path("write_question/<int:post_id>", question_views.write_question, name="write_question"),
    path("myinfo/", views.myinfo, name="myinfo"),
    path("post/", views.post, name="post"),
    path('execute_chatbot/', views.execute_chatbot, name='execute_chatbot'),

    # comment_views.py
    path("api/comments/", comment_views.CommentList.as_view(), name="comment_list"),
    path("api/comments/<int:pk>/", comment_views.CommentDetail.as_view(), name="comment_detail"),
    path("api/comment/<int:pk>/like/", comment_views.CommentLikeView.as_view(), name="comment_like"),
]