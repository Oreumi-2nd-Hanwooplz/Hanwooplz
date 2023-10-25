from django.urls import path, include
from .views import views, chat_views, comment_views, question_views


app_name = 'hanwooplz_app'

urlpatterns = [
    path('', views.main, name='main'),
    path('index/',views.index, name='index'),
    path('write/',views.write, name='write'),
    path('chat/<int:room_number>/<int:receiver_id>', chat_views.current_chat, name='chat'),
    path('chat-msg/<int:room_number>', chat_views.chat_msg, name='chat_msg'),
    path('login/', views.LoginView.as_view(), name="login"),
    path("logout/", views.log_out, name="logout"),
    path('register/', views.register, name='register'),
    path("question-list/", question_views.question_list, name="question_list"),
    path("question/<int:post_id>", question_views.question, name="question"),
    path("write-question/", question_views.write_question, name="write_question"),
    path("write-question/<int:post_id>", question_views.write_question, name="write_question"),
    path("myinfo/", views.myinfo, name="myinfo"),
    path("post/", views.post, name="post"),
    path('execute-chatbot/', views.execute_chatbot, name='execute_chatbot'),

    # comment_views.py
    path("api/comments/", comment_views.CommentList.as_view(), name="comment_list"),
    path("api/comments/<int:pk>/", comment_views.CommentDetail.as_view(), name="comment_detail"),
    path("api/comment/<int:pk>/like/", comment_views.CommentLikeView.as_view(), name="comment_like"),
    path("question-test/", comment_views.question_test, name="question_test"),
    path("post-test/", comment_views.post_test, name="post_test"),
]