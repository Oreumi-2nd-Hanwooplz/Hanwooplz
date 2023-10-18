from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    return render(request, "registration/register.html")

def custom_login(request):
    return render(request, "registration/login.html")

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