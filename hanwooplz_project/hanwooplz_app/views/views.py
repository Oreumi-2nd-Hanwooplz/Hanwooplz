from pyexpat.errors import messages
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views import View
from django.http import HttpResponse
from django.http import JsonResponse
from ..forms import *
from ..models import *
from ..serializers import *
import json
import openai
from django.db.models import Q
from django.contrib.auth.forms import PasswordResetForm, PasswordChangeForm


# Create your views here.
def main(request):
    return render(request, 'main.html')
def index(request):
    return render(request, 'index.html')


# 게시글 작성 화면
def write(request):
    return render(request, 'write.html')
   


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hanwooplz_app:login')  # You can change 'login' to the name of your login view.
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            user_id = request.user.id
            return redirect(reverse('hanwooplz_app:myinfo', args=[user_id]))
    else:
        form = UserProfileForm(instance=request.user)
        form.fields['username'].widget.attrs['readonly'] = True
        form.fields['email'].widget.attrs['readonly'] = True

    return render(request, 'edit_profile.html', {'form': form})

def change_password(request):
    if request.method == 'POST':
        password_change_form = PasswordChangeForm(request.user, request.POST)

        if password_change_form.is_valid():
            password_change_form.save()
            update_session_auth_hash(request, request.user) 
            return redirect(reverse("hanwooplz_app:login"))
    else:
        password_change_form = PasswordChangeForm(request.user)

    return render(request, 'change_password.html', {'password_change_form': password_change_form})


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

def myinfo(request, user_id):
    userinfo = UserProfile.objects.get(id=user_id)
    user_posts = Post.objects.filter(author=userinfo)

    selected_category = request.GET.get('category', 'postportfolio')

    posts = []

    for post in user_posts:
        if selected_category == 'postportfolio':
            category = 'portfolio'
            postcategory = PostPortfolio.objects.filter(post=post).first()
        elif selected_category == 'postproject':
            category = 'project'
            postcategory = PostProject.objects.filter(post=post).first()
        elif selected_category == 'postquestion':
            category = 'question'
            postcategory = PostQuestion.objects.filter(post=post).first()

        if postcategory:
            posts.append({
                'title': post.title,
                'content': post.content,
                'created_at': post.created_at,
                'post_id': postcategory.id,
                "category": category,
            })

    context = {
        "user_id": userinfo.id,
        "username": userinfo.username,
        "full_name": userinfo.full_name,
        "job": userinfo.job,
        "tech_stack": userinfo.tech_stack,
        "career": userinfo.career,
        "career_detail": userinfo.career_detail,
        "introduction": userinfo.introduction,
        "posts": posts,
        "github_link": userinfo.github_link,
        "linkedin_link": userinfo.linkedin_link,
        "selected_category": selected_category,
        
    }
    return render(request, "myinfo.html", context)


def get_posts_by_category(request):
    category = request.GET.get('category')
    if category == 'post':
        posts = Post.objects.all()  # Post 모델의 게시물을 가져옵니다.
    elif category == 'postportfolio':
        posts = PostPortfolio.objects.all()  # PostPortfolio 모델의 게시물을 가져옵니다.
    elif category == 'postproject':
        posts = PostProject.objects.all()  # PostProject 모델의 게시물을 가져옵니다.
    elif category == 'postquestion':
        posts = PostQuestion.objects.all()  # PostQuestion 모델의 게시물을 가져옵니다.

    # 가져온 게시물을 템플릿에 전달하여 HTML로 렌더링합니다.
    context = {'posts': posts}
    return render(request, 'posts_by_category.html', context)

def post(request):
    return render(request, "post.html")

def post_list(request):
    return render(request, "post_list.html")


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
        return JsonResponse({"response": response})
    return render(request, 'index.html')

@login_required
@ensure_csrf_cookie
def send_application(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        post_id = data.get('post_id')
        author_id = data.get('recipient_id')
        sender_id = request.user.id  # 요청을 보낸 사용자의 ID

        try:
            post = Post.objects.get(pk=post_id)
            recipient = UserProfile.objects.get(pk=author_id)
            sender = UserProfile.objects.get(pk=sender_id)

            # 중복 레코드 방지를 위해 먼저 확인
            if not Notifications.objects.filter(user=recipient, sender=sender, post=post).exists():
                # 중복 레코드가 없을 때만 알림 메시지 생성
                notification = Notifications(user=recipient, sender=sender, post=post, accept_or_not=None)
                notification.save()
                success = True
            else:
                success = False  # 이미 존재하는 레코드라면 중복 처리
        except (Post.DoesNotExist, UserProfile.DoesNotExist) as e:
            # 필요한 객체를 찾을 수 없는 경우
            success = False
    else:
        success = False

    return JsonResponse({'success': success})

def get_notifications(request):
    if request.user.is_authenticated:
        notifications = Notifications.objects.filter(Q(user=request.user) | Q(sender=request.user)).order_by('-created_at')

        notifications_list = []
        for notification in notifications:
            postinfo = Post.objects.get(id=notification.post.id)
            projectinfo = PostProject.objects.get(post_id=postinfo.id)
            senderinfo = UserProfile.objects.get(id=notification.sender.id)
            created_at_formatted = notification.created_at.strftime('%Y-%m-%d %H:%M')
            notifications_list.append({
                'id': notification.id,
                'user': notification.user.username,
                'title': postinfo.title,
                'sender': senderinfo.username,
                'created_at': created_at_formatted,
                'accept_or_not': notification.accept_or_not,
                'titlelink': f'/project/{projectinfo.id}',
                'senderlink': f'/myinfo/{senderinfo.id}',
            })

        context = {
        "notifications_list": notifications_list,
        }
        return JsonResponse({'notifications': context})
    else:
        return JsonResponse({'notifications': []})

def accept_reject_notification(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            notification_id = data.get('notificationId')
            result = data.get('result')
            
            if notification_id is not None and result is not None:
                try:
                    notification = Notifications.objects.get(id=notification_id)

                    if result == '수락':
                        notification.accept_or_not = True
                        notification.save()
                        
                        # 추가적인 작업을 수행 (예: ProjectMembers에 멤버 추가)
                        sender = notification.sender.id
                        projectinfo = PostProject.objects.get(post_id=notification.post.id)
                        projectid = projectinfo.id
                        ProjectMembers.objects.create(members_id=sender, project_id=projectid)
                        members = ProjectMembers.objects.filter(project_id=projectid).count()
                        if members >= projectinfo.target_members:
                            projectinfo.status = 2
                            projectinfo.save()
                        

                    elif result == '거절':
                        notification.accept_or_not = False
                        notification.save()

                    response_data = {'success': True}
                    return JsonResponse(response_data)

                except Notifications.DoesNotExist:
                    response_data = {'success': False, 'error': '알림을 찾을 수 없습니다.'}
                    return JsonResponse(response_data)

            else:
                response_data = {'success': False, 'error': '잘못된 데이터 요청입니다.'}
                return JsonResponse(response_data)

        except json.JSONDecodeError as e:
            response_data = {'success': False, 'error': str(e)}
            return JsonResponse(response_data)

    else:
        response_data = {'success': False, 'error': 'POST 요청이 필요합니다.'}
        return JsonResponse(response_data)

      
def check_duplicate_notification(request):
    if request.method == 'POST':
        recipient_id = request.POST.get('recipient_id')
        post_id = request.POST.get('post_id')

        # 중복 알림 확인 로직
        duplicate = Notifications.objects.filter(user=recipient_id, post=post_id).exists()

        return JsonResponse({'duplicate': duplicate})
# 아이디 찾기

def find_id(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        user = get_user_model().objects.filter(full_name=name, email=email).first()

        if user:
            return render(request, 'find_userinfo/found_id.html', {'user_id': user.username})
        else:
            return render(request, 'find_userinfo/not_found.html')

    return render(request, 'find_userinfo/find_id.html')

# 비밀번호 찾기

def find_pw(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        user_model = get_user_model()

        try:
            user = user_model.objects.get(email=email, username=username)
        except user_model.DoesNotExist:
            # 사용자를 찾을 수 없음
            return render(request, 'find_userinfo/not_found.html')

        # 새로운 임시 비밀번호 생성
        new_password = user_model.objects.make_random_password()

        # 비밀번호 업데이트
        user.set_password(new_password)
        user.save()

        # 사용자에게 새로운 비밀번호 전달하는 방법 (이메일 등)

        # 여기에서는 임시 비밀번호를 템플릿을 통해 보여줍니다.
        context = {
            'new_password': new_password,
        }
        return render(request, 'find_userinfo/found_pw.html', context)
    else:
        return render(request, 'find_userinfo/find_pw.html')

def found_pw(request):
    # Your code to render the password reset done page goes here
    return render(request, 'find_userinfo/found_pw.html')
