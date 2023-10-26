from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..forms import *
from ..models import *
from ..serializers import *

def question_list(request, page_num=1):
    total = PostQuestion.objects.all().count()
    if total > (page_num-1)*10:
        post_question = PostQuestion.objects.all().order_by('-id')[(page_num-1)*10:total]
    else:
        post_question = PostQuestion.objects.all().order_by('-id')[(page_num-1)*10:page_num*10]
    
    question_id_list = post_question.values_list('post_id', flat=True)
    post = Post.objects.filter(id__in=question_id_list)
    post_author_id = post.values_list('author_id', flat=True)
    user = [UserProfile.objects.filter(id=pa_id).values()[0] for pa_id in post_author_id]

    context = {
        'question_list': zip(post, post_question, user),
    }
    return render(request, 'question_list.html', context)

def question(request, post_question_id=None):
    if post_question_id:
        post_question = get_object_or_404(PostQuestion, id=post_question_id)
        post = get_object_or_404(Post, id=post_question.post_id)
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
        return redirect('hanwooplz_app:question_list')

@login_required(login_url='login')
def write_question(request, post_question_id=None):
    if post_question_id:
        post_question = get_object_or_404(PostQuestion, id=post_question_id)
        post = get_object_or_404(Post, id=post_question.post_id)
    else:
        post_question = PostQuestion()
        post = Post()
    
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
            if not post_question_id:
                post.author_id = request.user.id
                post.save()
                post_question.post_id = post.id
                post_question.save()
                post_question_id = post_question.id
            else:
                post.save()
                post_question.save()

            return redirect('hanwooplz_app:question', post_question_id)
        else:
            messages.info(request, '질문을 등록하는데 실패했습니다. 다시 시도해주세요.')
            context={
                'title': request.POST.get('title'),
                'content': request.POST.get('content'),
                'keyword': request.POST.get('keyword'),
            }
            return render(request, 'write_question.html', context)
    else:
        if post_question_id:
            if request.user.id == post.author_id:
                context = {
                    'post_question_id': post_question_id,
                    'title': post.title,
                    'content': post.content,
                    'keyword': ' '.join(post_question.keyword),
                }
                return render(request, 'write_question.html', context)
            else:
                messages.info('올바르지 않은 접근입니다.')
                return redirect('hanwooplz_app:question', post_question_id)
        else:
            return render(request, 'write_question.html')
