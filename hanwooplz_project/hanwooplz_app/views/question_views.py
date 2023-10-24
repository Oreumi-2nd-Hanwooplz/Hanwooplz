from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..forms import *
from ..models import *
from ..serializers import *

def question_list(request):
    return render(request, "question_list.html")

def question_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post_question = get_object_or_404(PostQuestion, post_id=post_id)
    context = {
        'post': post,
        'post_question': post_question,
    }
    return render(request, "question.html", context)

@login_required(login_url='login')
def write_question(request, post_id=None):
    if post_id:
        post = get_object_or_404(Post, pk=post_id)
        post_question = get_object_or_404(PostQuestion, post_id=post_id)
        context = {
            'post': post,
            'post_question': post_question,
        }
        return render(request, "write_question.html", context)
    else:
        return render(request, "write_question.html")

def create_question(request, post_id=None):
    if post_id:
        post = get_object_or_404(PostQuestion, pk=post_id)
    #     form = QuestionForm(request.POST, request.FILES)
    
    # if form.is_valid():
    #     pass
    return redirect('', post_id=post.id)