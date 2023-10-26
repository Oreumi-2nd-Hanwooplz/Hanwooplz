from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..forms import *
from ..models import *
from ..serializers import *

def portfolio_list(request, page_num=1):
    total = PostPortfolio.objects.all().count()
    if total > (page_num-1)*10:
        post_portfolio = PostPortfolio.objects.all().order_by('-id')[(page_num-1)*10:total]
    else:
        post_portfolio = PostPortfolio.objects.all().order_by('-id')[(page_num-1)*10:page_num*10]
    
    portfolio_id_list = post_portfolio.values_list('post_id', flat=True)
    post = Post.objects.filter(id__in=portfolio_id_list)
    post_author_id = post.values_list('author_id', flat=True)
    user = [UserProfile.objects.filter(id=pa_id).values()[0] for pa_id in post_author_id]

    context = {
        'portfolio_list': zip(post, post_portfolio, user),
    }
    return render(request, 'portfolio_list.html', context)

def portfolio(request, post_portfolio_id=None):
    if post_portfolio_id:
        post_portfolio = get_object_or_404(PostPortfolio, id=post_portfolio_id)
        post = get_object_or_404(Post, id=post_portfolio.post_id)
        author = get_object_or_404(UserProfile, id=post.author_id)
        context = {
            'title': post.title,
            'author': author.username,
            'created_at': post.created_at,
            'start_date': post_portfolio.start_date,
            'end_date': post_portfolio.end_date,
            'members': post_portfolio.members,
            'tech_stacks': post_portfolio.tech_stack,
            'ext_link': post_portfolio.ext_link,
            'content': post.content,
        }
        return render(request, 'portfolio.html', context)
    else:
        messages.info('올바르지 않은 접근입니다.')
        return redirect('hanwooplz_app:portfolio_list')

@login_required(login_url='login')
def write_portfolio(request, post_portfolio_id=None):
    if post_portfolio_id:
        post_portfolio = get_object_or_404(PostPortfolio, id=post_portfolio_id)
        post = get_object_or_404(Post, id=post_portfolio.post_id)
    else:
        post = Post()
        post_portfolio = PostPortfolio()
    
    if request.method == 'POST':
        if 'delete-button' in request.POST:
            post.delete()
            return redirect('hanwooplz_app:portfolio_list')
        if 'temp-save-button' in request.POST:
            messages.info(request, '임시저장은 현재 지원되지 않는 기능입니다.')
            context={
                'title': request.POST.get('title'),
                'start_date': request.POST.get('start_date'),
                'end_date': request.POST.get('end_date'),
                'members': request.POST.get('members'),
                'tech_stack': request.POST.get('tech_stack'),
                'ext_link': request.POST.get('ext_link'),
                'content': request.POST.get('content'),
            }
            return render(request, 'write_portfolio.html', context)
        
        post_form = PostForm(request.POST, request.FILES, instance=post)
        post_portfolio_form = PostPortfolioForm(request.POST, request.FILES, instance=post_portfolio)

        if post_form.is_valid() and post_portfolio_form.is_valid():
            post = post_form.save(commit=False)
            post_portfolio = post_portfolio_form.save(commit=False)
            if not post_portfolio_id:
                post.author_id = request.user.id
                post.save()
                post_portfolio.post_id = post.id
                post_portfolio.save()
                post_portfolio_id = post_portfolio.id
            else:
                post.save()
                post_portfolio.save()

            return redirect('hanwooplz_app:portfolio', post_portfolio_id)
        else:
            messages.info(request, '질문을 등록하는데 실패했습니다. 다시 시도해주세요.')
            context={
                'title': request.POST.get('title'),
                'start_date': request.POST.get('start_date'),
                'end_date': request.POST.get('end_date'),
                'members': request.POST.get('members'),
                'tech_stack': request.POST.get('tech_stack'),
                'ext_link': request.POST.get('ext_link'),
                'content': request.POST.get('content'),
            }
            return render(request, 'write_portfolio.html', context)
    else:
        if post_portfolio_id:
            if request.user.id == post.author_id:
                start_date = str(post_portfolio.start_date).replace('년 ','-').replace('월 ','-').replace('일','')
                end_date = str(post_portfolio.end_date).replace('년 ','-').replace('월 ','-').replace('일','')
                context = {
                    'post_portfolio_id': post_portfolio_id,
                    'title': post.title,
                    'start_date': start_date,
                    'end_date': end_date,
                    'members': post_portfolio.members,
                    'tech_stack': ' '.join(post_portfolio.tech_stack),
                    'ext_link': post_portfolio.ext_link,
                    'content': post.content,
                }
                return render(request, 'write_portfolio.html', context)
            else:
                messages.info('올바르지 않은 접근입니다.')
                return redirect('hanwooplz_app:portfolio', post_portfolio_id)
        else:
            return render(request, 'write_portfolio.html')