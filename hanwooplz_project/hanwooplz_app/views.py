from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.http import JsonResponse
import json
import openai
from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CommentSerializer
from .models import comment
from django.views.generic import FormView
from . import forms, models
from .forms import CustomUserCreationForm, LoginForm

# Create your views here.
def main(request):
    return render(request, 'main.html')
def index(request):
    return render(request, 'index.html')


# 게시글 작성 화면
def write(request):
    return render(request, 'write.html')
    
# 게시글 수정 화면
# def edit(request, id):
#     post = get_object_or_404(Post, id=id)
#     if post:
#         post.description = post.description.strip()
#     if request.method == "POST":
#         post.title = request.POST['title']
#         post.description = request.POST['description']
#         post.save()
#         return redirect('hanwooplz_app:trade_post', pk=id)

#     return render(request, 'write.html', {'post': post})

def current_chat(request):
    return render(request, "chat.html")

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hanwooplz_app:login')  # You can change 'login' to the name of your login view.
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        context = {"form": form}
        return render(request, "registration/login.html", context)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")  # Redirect to the main page
            else:
                # 로그인 실패 메시지를 추가하고 다시 로그인 페이지를 렌더링
                messages.error(request, "로그인에 실패했습니다. 올바른 아이디와 비밀번호를 입력하세요.")

        context = {"form": form}
        return render(request, "registration/login.html", context)

def log_out(request):
    logout(request)
    return redirect(reverse("hanwooplz_app:login"))

def question_list(request):
    return render(request, "question_list.html")

def question_detail(request):
    return render(request, "question.html")

def create_question(request):
    return render(request, "question_form.html")

def myinfo(request):
    return render(request, "myinfo.html")

def post(request):
    return render(request, "post.html")

class ChatBot():
    def __init__(self, model='gpt-3.5-turbo'):
        self.model = model
        self.messages = []

    def ask(self, question):
        self.messages.append({
            'role': 'user',
            'content': question
        })
        res = self.__ask__()
        return res

    def __ask__(self):
        completion = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages
        )
        response = completion.choices[0].message['content']
        self.messages.append({
            'role': 'assistant',
            'content': response
        })
        return response

    def show_messages(self):
        return self.messages

    def clear(self):
        self.messages.clear()

def execute_chatbot(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        question = data.get('question')
        chatbot = ChatBot()
        response = chatbot.ask(question)
        chat_messages = chatbot.show_messages()
        
        chat_messages_json = [{'role': message['role'], 'content': message['content']} for message in chat_messages]
        
        return JsonResponse({"response": response, "chat_messages": chat_messages_json})
    
    return HttpResponse("Invalid Request")

class CommentList(APIView):
    def get(self, request):
        comments = comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    def post (self, request):
        author = request.user if request.user.is_authenticated else None

        comment_data = {
            "content": request.data.get("content"),
            "author": author,
        }
        serializer = CommentSerializer(data=comment_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CommentDetail(APIView):
    def get(self, request, pk):
        comment = get_object_or_404(comment, pk=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
    
    def put(self, request, pk):
        comment = get_object_or_404(comment, pk=pk)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        comment = get_object_or_404(comment, pk=pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
