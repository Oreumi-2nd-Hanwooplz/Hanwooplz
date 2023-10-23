from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.views import View
from django.http import JsonResponse
import json
import openai
from django.http import HttpResponse
from django.views.generic import FormView
from . import forms, models
from .forms import CustomUserCreationForm, LoginForm

# Create your views here.
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

from django.utils import timezone
from .models import post as Post, user_profile as UserProfile, chat_room, chat_messages
from django.db.models import Q
from django.contrib.auth.models import User

tmp_user = []

def format_datetime(dt):
    today = timezone.now().date()
    if dt.date() == today:
        return dt.strftime("오늘 %p %I:%M")
    yesterday = today - timezone.timedelta(days=1)
    if dt.date() == yesterday:
        return dt.strftime("어제 %p %I:%M")
    return dt.strftime("%Y-%m-%d %p %I:%M")

tmp_chat_rooms = [
        {
            'id': 1,  # 임의의 채팅 룸 ID
            'post': {
                'title': 'Post 1',  # 게시물 제목
                'author': {
                    'id': 1,  # 게시물 작성자 ID
                    'username': 'User1'  # 게시물 작성자 이름
                }
            },
            'sender': {
                'id': 2,  # 채팅을 보낸 사용자 ID
                'username': 'User2'  # 채팅을 보낸 사용자 이름
            },
            'receiver': {
                'id': 3,  # 채팅을 받은 사용자 ID
                'username': 'User3'  # 채팅을 받은 사용자 이름
            },
            'created_at': '2023-10-20 10:30:00',  # 채팅 룸 생성 일자 및 시간
            # 기타 필요한 데이터 추가
        },
        {
            'id': 2,  # 임의의 채팅 룸 ID
            'post': {
                'title': 'Post 1',  # 게시물 제목
                'author': {
                    'id': 1,  # 게시물 작성자 ID
                    'username': 'User1'  # 게시물 작성자 이름
                }
            },
            'sender': {
                'id': 4,  # 채팅을 보낸 사용자 ID
                'username': 'User4'  # 채팅을 보낸 사용자 이름
            },
            'receiver': {
                'id': 3,  # 채팅을 받은 사용자 ID
                'username': 'User3'  # 채팅을 받은 사용자 이름
            },
            'created_at': '2023-10-20 12:30:00',  # 채팅 룸 생성 일자 및 시간
            # 기타 필요한 데이터 추가
        },
        # 다른 채팅 룸 데이터도 추가 가능
    ]


# chat_room.objects.create(
#     sender=UserProfile.objects.get(id=1),  # 채팅을 보내는 사용자
#     receiver=UserProfile.objects.get(id=2),  # 채팅을 받는 사용자
#     created_at="2023-10-23 10:30:00"  # 생성 일자 및 시간
# )

# UserProfile.objects.create(

# )

# chat_messages.objects.create(
#         id = 1,
#         chat_room = '1',
#         sender = 'user1',
#         receiver = 'user2',
#         message = '안녕하세요',
#         read_or_not = 'False',
#         created_at="2023-10-23 10:30:00",
# )

tmp_chat_messages = [
        {
            'id':1, # 임의의 메세지 ID
            'chat_room':{
                'id': 1,  # 임의의 채팅 룸 ID
                'post': {
                    'title': 'Post 1',  # 게시물 제목
                    'author': {
                        'id': 1,  # 게시물 작성자 ID
                        'username': 'User1'  # 게시물 작성자 이름
                    }
                },
                'sender': {
                    'id': 2,  # 채팅을 보낸 사용자 ID
                    'username': 'User2'  # 채팅을 보낸 사용자 이름
                },
                'receiver': {
                    'id': 3,  # 채팅을 받은 사용자 ID
                    'username': 'User3'  # 채팅을 받은 사용자 이름
                },
                'created_at': '2023-10-20 10:30:00',  # 채팅 룸 생성 일자 및 시간
                # 기타 필요한 데이터 추가
            },
            'sender': {
                    'id': 2,  # 채팅을 보낸 사용자 ID
                    'username': 'User2'  # 채팅을 보낸 사용자 이름
                },
            'receiver': {
                    'id': 3,  # 채팅을 받은 사용자 ID
                    'username': 'User3'  # 채팅을 받은 사용자 이름
                },
            'message': '안녕하세요',
            'read_or_not': 'False',
            'created_at': '2023-10-20 10:30:00',
        },
        {
            'id':2, # 임의의 메세지 ID
            'chat_room':{
                'id': 2,  # 임의의 채팅 룸 ID
                'post': {
                    'title': 'Post 1',  # 게시물 제목
                    'author': {
                        'id': 1,  # 게시물 작성자 ID
                        'username': 'User1'  # 게시물 작성자 이름
                    }
                },
                'sender': {
                    'id': 4,  # 채팅을 보낸 사용자 ID
                    'username': 'User4'  # 채팅을 보낸 사용자 이름
                },
                'receiver': {
                    'id': 3,  # 채팅을 받은 사용자 ID
                    'username': 'User3'  # 채팅을 받은 사용자 이름
                },
                'created_at': '2023-10-20 12:30:00',  # 채팅 룸 생성 일자 및 시간
                # 기타 필요한 데이터 추가
            },
            'sender': {
                    'id': 4,  # 채팅을 보낸 사용자 ID
                    'username': 'User4'  # 채팅을 보낸 사용자 이름
                },
            'receiver': {
                    'id': 3,  # 채팅을 받은 사용자 ID
                    'username': 'User3'  # 채팅을 받은 사용자 이름
                },
            'message': '누구세요',
            'read_or_not': 'False',
            'created_at': '2023-10-20 10:30:00',
        },
        
]

def get_rooms(request):
    # chat_rooms = chat_room.objects.filter(Q(buyer=request.user.id) | Q(seller=request.user.id))
    

    latest_messages = []
    for room in tmp_chat_rooms:
        try:
            # unread_message_count = chat_messages.objects.filter(
            #     Q(chat_room=room),
            #     ~Q(sender=request.user),
            #     Q(read_or_not=False)
            # ).count()
            room_id = room['id']
            unread_message_count = 0  # 임시로 0으로 설정

            # latest_message = chat_messages.objects.filter(chat_room=room).latest('created_at')
            latest_message = {
                'message': tmp_chat_messages[room_id - 1]['message'],
                'created_at': '2023-10-23 15:45:00',
            }
            # seller = None
            sender = room['sender']  # seller을 receiver로 설정
            goods_img = None

            # if latest_message.chat_room.buyer == request.user:
            #     seller = latest_message.chat_room.seller
            # else:
            #     seller = latest_message.chat_room.buyer

            # try:
            #     goods_img = Post.objects.filter(user=seller).latest('created_at')
            # except Post.DoesNotExist:
            #     pass

            latest_messages.append({
                'chat_room_id': room_id,
                'sender_id': sender['id'],
                'sender': sender['username'],
                'message': latest_message['message'],
                'created_at': latest_message['created_at'],
                'unread_message_count': unread_message_count,
                'goods_img': goods_img
            })
        except chat_messages.DoesNotExist:
            sender = None

            # if room.seller.id == request.user.id:
            #     seller = UserProfile.objects.get(pk=request.user.id)
            # else:
            #     seller = room.seller
            seller = room['receiver']  # seller을 receiver로 설정

            latest_messages.append({
                'chat_room_id': room_id,
                'seneder_id': sender['id'],
                'sender': sender['username'],
                'message': '',
                'created_at': '',
                'unread_message_count': 0,
                'goods_img': None,
            })
            pass

    latest_messages.sort(key=lambda x: x['created_at'], reverse=True)

    return latest_messages

# def get_rooms(request):
#     # 임시 데이터 생성
#     chat_rooms = [
#         {
#             'id': 1,  # 임의의 채팅 룸 ID
#             'post': {
#                 'title': 'Post 1',  # 게시물 제목
#                 'user': {
#                     'id': 1,  # 게시물 작성자 ID
#                     'username': 'User1'  # 게시물 작성자 이름
#                 }
#             },
#             'sender': {
#                 'id': 2,  # 채팅을 보낸 사용자 ID
#                 'username': 'User2'  # 채팅을 보낸 사용자 이름
#             },
#             'receiver': {
#                 'id': 3,  # 채팅을 받은 사용자 ID
#                 'username': 'User3'  # 채팅을 받은 사용자 이름
#             },
#             'created_at': '2023-10-20 10:30:00',  # 채팅 룸 생성 일자 및 시간
#             # 기타 필요한 데이터 추가
#         },
#         # 다른 채팅 룸 데이터도 추가 가능
#     ]

#     latest_messages = []
#     for room in chat_rooms:
#         # 데이터를 가져오는 부분 수정
#         room_id = room['id']
#         unread_message_count = 0  # 임시로 0으로 설정

#         latest_message = {
#             'message': 'Latest message for room ' + str(room_id),
#             'created_at': '2023-10-23 15:45:00',
#         }

#         seller = room['receiver']  # seller을 receiver로 설정
#         goods_img = None  # 임시로 None으로 설정

#         latest_messages.append({
#             'chat_room_id': room_id,
#             'seller_id': seller['id'],
#             'seller': seller,
#             'message': latest_message['message'],
#             'created_at': latest_message['created_at'],
#             'unread_message_count': unread_message_count,
#             'goods_img': goods_img
#         })

#     # 데이터 정렬
#     latest_messages.sort(key=lambda x: x['created_at'], reverse=True)

#     return latest_messages

def current_chat(request, room_number, seller_id):
    current_chat = None
    formatted_chat_msgs = []
    first_unread_index = -1

    if room_number == 0 and seller_id == 12:
        

        context = {
            "room_number" : -1,
            "chat_msgs" : [],
            "latest_messages" : get_rooms(request),
            'first_unread_index': 0,    
            
        }

        return render(request, 'chat.html', context)

    if room_number == 0:
        if seller_id == request.user.id:
            pass
        else:
            seller = UserProfile.objects.get(id=seller_id)
            buyer = UserProfile.objects.get(id=request.user.id)
            new_chat_room = chat_room.objects.create(buyer=buyer, seller=seller)
            room_number = new_chat_room.id
    else:
        # current_room = chat_room.objects.get(id=room_number)
        current_room = [
        {
            'id': 1,  # 임의의 채팅 룸 ID
            'post': {
                'title': 'Post 1',  # 게시물 제목
                'author': {
                    'id': 1,  # 게시물 작성자 ID
                    'username': 'User1'  # 게시물 작성자 이름
                }
            },
            'sender': {
                'id': 2,  # 채팅을 보낸 사용자 ID
                'username': 'User2'  # 채팅을 보낸 사용자 이름
            },
            'receiver': {
                'id': 3,  # 채팅을 받은 사용자 ID
                'username': 'User3'  # 채팅을 받은 사용자 이름
            },
            'created_at': '2023-10-20 10:30:00',  # 채팅 룸 생성 일자 및 시간
            # 기타 필요한 데이터 추가
        },
        # 다른 채팅 룸 데이터도 추가 가능
    ]
        # current_chat = chat_messages.objects.filter(chat_room=current_room).order_by('created_at')     
        current_chat = [
        {
            'id':1, # 임의의 메세지 ID
            'chat_room':{
                'id': 1,  # 임의의 채팅 룸 ID
                'post': {
                    'title': 'Post 1',  # 게시물 제목
                    'author': {
                        'id': 1,  # 게시물 작성자 ID
                        'username': 'User1'  # 게시물 작성자 이름
                    }
                },
                'sender': {
                    'id': 2,  # 채팅을 보낸 사용자 ID
                    'username': 'User2'  # 채팅을 보낸 사용자 이름
                },
                'receiver': {
                    'id': 3,  # 채팅을 받은 사용자 ID
                    'username': 'User3'  # 채팅을 받은 사용자 이름
                },
                'created_at': '2023-10-20 10:30:00',  # 채팅 룸 생성 일자 및 시간
                # 기타 필요한 데이터 추가
            },
            'sender': {
                    'id': 2,  # 채팅을 보낸 사용자 ID
                    'username': 'User2'  # 채팅을 보낸 사용자 이름
                },
            'receiver': {
                    'id': 3,  # 채팅을 받은 사용자 ID
                    'username': 'User3'  # 채팅을 받은 사용자 이름
                },
            'message': '안녕하세요',
            'read_or_not': 'False',
            'created_at': '2023-10-20 10:30:00',
        }
]

        # for i, chat in enumerate(current_chat):
        #     if chat.read_or_not == False:
        #         if chat.sender.id != request.user.id:
        #             chat.read_or_not = True
        #             chat.save()
        #             if first_unread_index == -1:
        #                 first_unread_index = chat.id

        # for chat in current_chat:
        #     formatted_chat_msgs.append({
        #         'created_at': format_datetime(chat.created_at),
        #         'message': chat.message,
        #         'username': chat.sender.username,
        #         'is_read': chat.read_or_not, 
        #         'id': chat.id,
        #     })

    seller_profile = {
        'username': '',
        'rating_score': 37.5
    }

    # seller_profile['username'] = UserProfile.objects.get(id=seller_id).username


    context = {
        "room_number" : room_number,
        "chat_msgs" : formatted_chat_msgs,
        "latest_messages" : get_rooms(request),
        'first_unread_index': first_unread_index,
        # 'seller': seller_profile
    }

    return render(request, 'chat.html', context)


def chat_msg(request, room_number):
    room = get_object_or_404(chat_room, pk=room_number)

    current_time = timezone.now()
    three_days_ago = current_time - timezone.timedelta(days=3)
    chat_msgs = chat_messages.objects.filter(chat_room=room, created_at__gte=three_days_ago).order_by('-created_at')

    created_at = format_datetime(chat_msg.created_at)

    if request.method == 'POST':
        chatInput = request.POST.get('chat-send-msg')
        sender = request.user
        chat_msg = chat_messages(chat_room=room, sender=sender, message=chatInput, read_or_not=False)
        chat_msg.save()

        response_data = {
            'created_at': created_at,
            'message': chat_msg.message,
            'username': chat_msg.sender.username,
        }

        return JsonResponse(response_data)

    context = {
        "room_number" : room_number,
        "chat_msgs" : chat_msgs
    }

    return render(request, 'chat.html', context)
