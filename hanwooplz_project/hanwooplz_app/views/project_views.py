from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from ..forms import *
from ..models import *
from ..serializers import *

def project_list(request, page_num=1):
    items_per_page = 10  # 페이지 당 항목 수

    # 페이지 번호를 이용해 해당 페이지의 포트폴리오 검색
    start_index = (page_num - 1) * items_per_page
    end_index = page_num * items_per_page

    post_project = PostProject.objects.order_by('-id')[start_index:end_index]
    project_lists = []

    query = request.GET.get('search')
    search_type = request.GET.get('search_type')  # 검색 옵션을 가져옵니다

    for project in post_project:
        post = Post.objects.get(id=project.post_id)
        author = UserProfile.objects.get(id=post.author_id)
        is_recruiting = True if project.status == 1 else False
        project_status = "모집 완료" if project.status == 2 else "모집 중단"

        if query:
            # 검색 쿼리와 검색 옵션에 따라 검색 결과 필터링
            if search_type == "title_content" and ((query in post.title) or (query in post.content)):
                project_lists.append({
                    'title': post.title,
                    'created_at': post.created_at,
                    'author_id': post.author_id,
                    'post_project': project.id,
                    'author': author.username,
                    'tech_stacks': project.tech_stack,
                    'isRecruiting': is_recruiting,
                    "project_status": project_status,
                })
            elif search_type == "writer" and (query in author.username):
                project_lists.append({
                    'title': post.title,
                    'created_at': post.created_at,
                    'author_id': post.author_id,
                    'post_project': project.id,
                    'author': author.username,
                    'tech_stacks': project.tech_stack,
                    'isRecruiting': is_recruiting,
                    "project_status": project_status,
                })
        else:
            # 검색 쿼리가 없는 경우, 모든 포트폴리오 추가
            project_lists.append({
                'title': post.title,
                'created_at': post.created_at,
                'author_id': post.author_id,
                'post_project': project.id,
                'author': author.username,
                'tech_stacks': project.tech_stack,
                'isRecruiting': is_recruiting,
                "project_status": project_status,
            })

    # "전체" 및 "모집중"에 따라 포스트 필터링
    filter_option = request.GET.get('filter_option')
    if filter_option == 'recruiting':
        project_lists = [project for project in project_lists if project['isRecruiting']]

    context = {
        "post_lists": project_lists,
        "board_name": "프로젝트 팀원 모집",
        "is_portfolio": False,
    }

    return render(request, 'project_list.html', context)



def project(request, post_project_id=None):
    if post_project_id:
        post_project = get_object_or_404(PostProject, id=post_project_id)
        post = get_object_or_404(Post, id=post_project.post_id)
        author = get_object_or_404(UserProfile, id=post.author_id)
        members = ProjectMembers.objects.filter(project=post_project_id).count()
        context = {
            'title': post.title,
            'author': author.username,
            'author_id': author.id,
            'created_at': post.created_at,
            'start_date': post_project.start_date,
            'end_date': post_project.end_date,
            'members': members,
            'target_members': post_project.target_members,
            'tech_stacks': post_project.tech_stack,
            'ext_link': post_project.ext_link,
            'content': post.content,
            'post_project_id' : post_project_id,
            'post_id': post.id,
            'project_status': post_project.status,
        }
        return render(request, 'project.html', context)
    else:
        messages.info('올바르지 않은 접근입니다.')
        return redirect('hanwooplz_app:project_list')

@login_required(login_url='login')
def write_project(request, post_project_id=None):
    if post_project_id:
        post_project = get_object_or_404(PostProject, id=post_project_id)
        post = get_object_or_404(Post, id=post_project.post_id)
    else:
        post_project = PostProject()
        post = Post()
    
    # 작성 시
    if request.method == 'POST':
        if 'delete-button' in request.POST:
            post.delete()
            return redirect('hanwooplz_app:project_list')
        if 'temp-save-button' in request.POST:
            messages.info(request, '임시저장은 현재 지원되지 않는 기능입니다.')
            context={
                'title': request.POST.get('title'),
                'start_date': request.POST.get('start_date'),
                'end_date': request.POST.get('end_date'),
                'target_members': request.POST.get('target_members'),
                'tech_stack': request.POST.get('tech_stack'),
                'ext_link': request.POST.get('ext_link'),
                'content': request.POST.get('content'),
            }
            return render(request, 'write_project.html', context)
        
        request.POST._mutable = True
        request.POST['tech_stack'] = request.POST.get('tech_stack').split()
        post_form = PostForm(request.POST, request.FILES, instance=post)
        post_project_form = PostProjectForm(request.POST, request.FILES, instance=post_project)

        if post_form.is_valid() and post_project_form.is_valid():
            post = post_form.save(commit=False)
            post_project = post_project_form.save(commit=False)
            if not post_project_id:
                post.author_id = request.user.id
                post.save()
                post_project.post_id = post.id
                post_project.save()
                post_project_id = post_project.id
                user = get_object_or_404(UserProfile, pk=request.user.id)
                project = get_object_or_404(PostProject, pk=post_project_id)
                ProjectMembers.objects.create(project=project, members=user)
            else:
                post.save()
                post_project.save()

            return redirect('hanwooplz_app:project', post_project_id)
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
            return render(request, 'write_project.html', context)
        
    # 게시물 수정 시
    else:
        if post_project_id:
            if request.user.id == post.author_id:
                start_date = str(post_project.start_date).replace('년 ','-').replace('월 ','-').replace('일','')
                end_date = str(post_project.end_date).replace('년 ','-').replace('월 ','-').replace('일','')
                context = {
                    'post_project_id': post_project_id,
                    'title': post.title,
                    'start_date': start_date,
                    'end_date': end_date,
                    'target_members': post_project.target_members,
                    'tech_stack': ' '.join(post_project.tech_stack),
                    'ext_link': post_project.ext_link,
                    'content': post.content,
                    'post_author_id': post.author_id,
                }
                return render(request, 'write_project.html', context)
            else:
                messages.info('올바르지 않은 접근입니다.')
                return redirect('hanwooplz_app:project', post_project_id)
        else:
            return render(request, 'write_project.html')

def update_views(request):
    if request.method == "POST":
        project_id = request.POST.get("project_id")
        status = request.POST.get("status")
        project = get_object_or_404(PostProject, pk=project_id)
        project.status = status
        project.save()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False})