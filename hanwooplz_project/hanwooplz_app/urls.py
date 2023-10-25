from django.urls import path, include
from .views import views, chat_views, comment_views, question_views


app_name = 'hanwooplz_app'

urlpatterns = [
    path('', views.main, name='main'),
    path('index/',views.index, name='index'),
    path('write/',views.write, name='write'),
    path('chat/<int:room_number>/<int:receiver_id>', chat_views.current_chat, name='chat'),
    path('chat-msg/<int:room_number>', chat_views.chat_msg, name='chat-msg'),
    path('login/', views.LoginView.as_view(), name="login"),
    path("logout/", views.log_out, name="logout"),
    path('register/', views.register, name='register'),
    path("question-list/", question_views.question_list, name="question-list"),
    path("question/<int:post_id>", question_views.question, name="question"),
    path("write-question/", question_views.write_question, name="write-question"),
    path("write-question/<int:post_id>", question_views.write_question, name="write-question"),
    path("myinfo/", views.myinfo, name="myinfo"),
    path("post/", views.post, name="post"),
    path("post-list/", views.post_list, name="post-list"),
    path('execute-chatbot/', views.execute_chatbot, name='execute-chatbot'),

    # comment_views.py
    path("api/comments/", comment_views.CommentList.as_view(), name="comment-list"),
    path("api/comments/<int:pk>/", comment_views.CommentDetail.as_view(), name="comment-detail"),
    path("api/comment/<int:pk>/like/", comment_views.CommentLikeView.as_view(), name="comment-like"),
    path("question-test/", comment_views.question_test, name="question-test"),
    path("post-test/", comment_views.post_test, name="post-test"),
]