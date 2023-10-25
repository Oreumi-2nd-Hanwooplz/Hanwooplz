from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..forms import *
from ..models import *
from ..serializers import *

def question_list(request):
    post_question = PostQuestion.objects.all().order_by('-id')[:10]
    post_id = post_question.values('post')
    # get title, author, created_at in Post
    # get like and keyword in PostQuestion
    # make them into a context dictionary
    context = {}
    return render(request, 'question_list.html', context)

def question(request, post_id=None):
    if post_id:
        post = get_object_or_404(Post, id=post_id)
        post_question = get_object_or_404(PostQuestion, post_id=post_id)
        author = get_object_or_404(UserProfile, id=post.author_id)
        context = {
            'title': post.title,
            'content': post.content,
            'author': author.username,
            'created_at': post.created_at,
            'like': post_question.like,
            'keywords': post_question.keyword,
        }
        return render(request, 'question.html', context)
    else:
        messages.info('올바르지 않은 접근입니다.')
        return redirect('question_list')

@login_required(login_url='login')
def write_question(request, post_id=None):
    if post_id:
        post = get_object_or_404(Post, id=post_id)
        post_question = get_object_or_404(PostQuestion, post_id=post_id)
    else:
        post = Post()
        post_question = PostQuestion()
    
    if request.method == 'POST':
        if 'delete-button' in request.POST:
            post.delete()
            return redirect('hanwooplz_app:question_list')
        if 'temp-save-button' in request.POST:
            messages.info(request, '임시저장은 현재 지원되지 않는 기능입니다.')
            context={
                'title': request.POST.get('title'),
                'content': request.POST.get('content'),
                'keyword': request.POST.get('keyword'),
            }
            return render(request, 'write_question.html', context)
        
        post_form = PostForm(request.POST, request.FILES, instance=post)
        post_question_form = PostQuestionForm(request.POST, request.FILES, instance=post_question)

        if post_form.is_valid() and post_question_form.is_valid():
            post = post_form.save(commit=False)
            post_question = post_question_form.save(commit=False)
            if not post_id:
                post.author_id = request.user.id
                post.save()
                post_question.post_id = post_id = post.id
                post_question.save()
            else:
                post.save()
                post_question.save()

            return redirect('hanwooplz_app:question', post_id=post_id)
        else:
            messages.info(request, '질문을 등록하는데 실패했습니다. 다시 시도해주세요.')
            context={
                'title': request.POST.get('title'),
                'content': request.POST.get('content'),
                'keyword': request.POST.get('keyword'),
            }
            return render(request, 'write_question.html', context)
    else:
        if post_id:
            if request.user.id == post.author_id:
                context = {
                    'post_id': post.id,
                    'title': post.title,
                    'content': post.content,
                    'keyword': ' '.join(post_question.keyword),
                }
                return render(request, 'write_question.html', context)
            else:
                messages.info('올바르지 않은 접근입니다.')
                return redirect('hanwooplz_app:question', post_id=post_id)
        else:
            return render(request, 'write_question.html')
