from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from ..forms import *
from ..models import *
from ..serializers import *
from django.utils import timezone
from django.db.models import Q

# tmp_chat_rooms = [
#         {
#             'id': 1,  # 임의의 채팅 룸 ID
#             'post': {
#                 'title': 'Post 1',  # 게시물 제목
#                 'author': {
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
#         {
#             'id': 2,  # 임의의 채팅 룸 ID
#             'post': {
#                 'title': 'Post 1',  # 게시물 제목
#                 'author': {
#                     'id': 1,  # 게시물 작성자 ID
#                     'username': 'User1'  # 게시물 작성자 이름
#                 }
#             },
#             'sender': {
#                 'id': 4,  # 채팅을 보낸 사용자 ID
#                 'username': 'User4'  # 채팅을 보낸 사용자 이름
#             },
#             'receiver': {
#                 'id': 3,  # 채팅을 받은 사용자 ID
#                 'username': 'User3'  # 채팅을 받은 사용자 이름
#             },
#             'created_at': '2023-10-20 12:30:00',  # 채팅 룸 생성 일자 및 시간
#             # 기타 필요한 데이터 추가
#         },
#         # 다른 채팅 룸 데이터도 추가 가능
#     ]

# tmp_chat_messages = [
#         {
#             'id':1, # 임의의 메세지 ID
#             'chat_room':{
#                 'id': 1,  # 임의의 채팅 룸 ID
#                 'post': {
#                     'title': 'Post 1',  # 게시물 제목
#                     'author': {
#                         'id': 1,  # 게시물 작성자 ID
#                         'username': 'User1'  # 게시물 작성자 이름
#                     }
#                 },
#                 'sender': {
#                     'id': 2,  # 채팅을 보낸 사용자 ID
#                     'username': 'User2'  # 채팅을 보낸 사용자 이름
#                 },
#                 'receiver': {
#                     'id': 3,  # 채팅을 받은 사용자 ID
#                     'username': 'User3'  # 채팅을 받은 사용자 이름
#                 },
#                 'created_at': '2023-10-20 10:30:00',  # 채팅 룸 생성 일자 및 시간
#                 # 기타 필요한 데이터 추가
#             },
#             'sender': {
#                     'id': 2,  # 채팅을 보낸 사용자 ID
#                     'username': 'User2'  # 채팅을 보낸 사용자 이름
#                 },
#             'receiver': {
#                     'id': 3,  # 채팅을 받은 사용자 ID
#                     'username': 'User3'  # 채팅을 받은 사용자 이름
#                 },
#             'message': '안녕하세요',
#             'read_or_not': 'False',
#             'created_at': '2023-10-20 10:30:00',
#         },
#         {
#             'id':2, # 임의의 메세지 ID
#             'chat_room':{
#                 'id': 2,  # 임의의 채팅 룸 ID
#                 'post': {
#                     'title': 'Post 1',  # 게시물 제목
#                     'author': {
#                         'id': 1,  # 게시물 작성자 ID
#                         'username': 'User1'  # 게시물 작성자 이름
#                     }
#                 },
#                 'sender': {
#                     'id': 4,  # 채팅을 보낸 사용자 ID
#                     'username': 'User4'  # 채팅을 보낸 사용자 이름
#                 },
#                 'receiver': {
#                     'id': 3,  # 채팅을 받은 사용자 ID
#                     'username': 'User3'  # 채팅을 받은 사용자 이름
#                 },
#                 'created_at': '2023-10-20 12:30:00',  # 채팅 룸 생성 일자 및 시간
#                 # 기타 필요한 데이터 추가
#             },
#             'sender': {
#                     'id': 4,  # 채팅을 보낸 사용자 ID
#                     'username': 'User4'  # 채팅을 보낸 사용자 이름
#                 },
#             'receiver': {
#                     'id': 3,  # 채팅을 받은 사용자 ID
#                     'username': 'User3'  # 채팅을 받은 사용자 이름
#                 },
#             'message': '누구세요',
#             'read_or_not': 'False',
#             'created_at': '2023-10-20 10:30:00',
#         },
        
# ]

def format_datetime(dt):
    today = timezone.now().date()
    if dt.date() == today:
        return dt.strftime("오늘 %p %I:%M")
    yesterday = today - timezone.timedelta(days=1)
    if dt.date() == yesterday:
        return dt.strftime("어제 %p %I:%M")
    return dt.strftime("%Y-%m-%d %p %I:%M")


def get_rooms(request):
    chat_rooms = ChatRoom.objects.filter(Q(sender=request.user.id) | Q(receiver=request.user.id))
    
    latest_messages = []
    for room in chat_rooms:
        try:
            unread_message_count = ChatMessages.objects.filter(
                Q(chat_room=room),
                ~Q(sender=request.user),
                Q(read_or_not=False)
            ).count()
            

            latest_message = ChatMessages.objects.filter(chat_room=room).latest('created_at')
            # latest_message = {
            #     'message': tmp_chat_messages[room_id - 1]['message'],
            #     'created_at': '2023-10-23 15:45:00',
            # }
            receiver = None
            goods_img = None

            if latest_message.chat_room.sender == request.user:
                receiver = latest_message.chat_room.receiver
            else:
                receiver = latest_message.chat_room.sender

            try:
                goods_img = Post.objects.filter(user=receiver).latest('created_at')
            except Post.DoesNotExist:
                pass

            latest_messages.append({
                'chat_room_id': room.id,
                'receiver_id': receiver.id,
                'receiver': receiver,
                'message': latest_message.message,
                'created_at': format_datetime(latest_message.created_at),
                'unread_message_count': unread_message_count,
                'goods_img': goods_img
            })
        except ChatMessages.DoesNotExist:
            receiver = None

            if room.receiver.id == request.user.id:
                receiver = UserProfile.objects.get(pk=request.user.id)
            else:
                receiver = room.receiver
            
            latest_messages.append({
                'chat_room_id': room.id,
                'receiver_id': receiver.id,
                'receiver': receiver,
                'message': '',
                'created_at': '',
                'unread_message_count': 0,
                'goods_img': None,
            })
            pass

    latest_messages.sort(key=lambda x: x['created_at'], reverse=True)

    return latest_messages

def current_chat(request, room_number, receiver_id):
    current_chat = None
    formatted_chat_msgs = []
    first_unread_index = -1

    if room_number == 0 and receiver_id == 12:
        

        context = {
            "room_number" : -1,
            "chat_msgs" : [],
            "latest_messages" : get_rooms(request),
            'first_unread_index': 0,    
            
        }

        return render(request, 'chat.html', context)

    if room_number == 0:
        if receiver_id == request.user.id:
            pass
        else:
            receiver = UserProfile.objects.get(id=receiver_id)
            sender = UserProfile.objects.get(id=request.user.id)
            new_chat_room = ChatRoom.objects.create(sender=sender, receiver=receiver)
            room_number = new_chat_room.id
    else:
        current_room = ChatRoom.objects.get(pk=room_number)
        current_chat = ChatMessages.objects.filter(chat_room=current_room).order_by('created_at')     
        

        for i, chat in enumerate(current_chat):
            if chat.read_or_not == False:
                if chat.sender.id != request.user.id:
                    chat.read_or_not = True
                    chat.save()
                    if first_unread_index == -1:
                        first_unread_index = chat.id

        for chat in current_chat:
            formatted_chat_msgs.append({
                'created_at': format_datetime(chat.created_at),
                'message': chat.message,
                'username': chat.sender.username,
                'is_read': chat.read_or_not, 
                'id': chat.id,
            })

    context = {
        "room_number" : room_number,
        "chat_msgs" : formatted_chat_msgs,
        "latest_messages" : get_rooms(request),
        'first_unread_index': first_unread_index,
  
    }

    return render(request, 'chat.html', context)


def chat_msg(request, room_number):
    room = get_object_or_404(ChatRoom, pk=room_number)

    current_time = timezone.now()
    three_days_ago = current_time - timezone.timedelta(days=3)
    chat_msgs = ChatMessages.objects.filter(chat_room=room, created_at__gte=three_days_ago).order_by('-created_at')

    created_at = format_datetime(chat_msg.created_at)

    if request.method == 'POST':
        chatInput = request.POST.get('chat-send-msg')
        sender = request.user
        chat_msg = ChatMessages(chat_room=room, sender=sender, message=chatInput, read_or_not=False)
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

