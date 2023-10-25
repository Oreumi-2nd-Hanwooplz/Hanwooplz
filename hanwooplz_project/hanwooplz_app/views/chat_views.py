from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from ..forms import *
from ..models import *
from ..serializers import *
from django.utils import timezone
from django.db.models import Q

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
            # unread_message_count = ChatMessages.objects.filter(
            #     Q(chat_room=room),
            #     ~Q(sender=request.user),
            #     Q(read_or_not=False)
            # ).count()

            latest_message = ChatMessages.objects.filter(chat_room=room.id).latest('created_at')

            sender = None

            if latest_message.chat_room.receiver == request.user:
                sender = latest_message.chat_room.sender
            else:
                sender = latest_message.chat_room.receiver


            latest_messages.append({
                'chat_room_id': room.id,
                'sender_id': sender.id,
                'sender': sender,
                'message': latest_message.message,
                'created_at': format_datetime(latest_message.created_at),
                # 'unread_message_count': unread_message_count,
            })
        except ChatMessages.DoesNotExist:
            sender = None

            if room.receiver.id == request.user.id:
                sender = UserProfile.objects.get(pk=request.user.id)
            else:
                sender = room.receiver
            
            latest_messages.append({
                'chat_room_id': room.id,
                'sender_id': sender.id,
                'sender': sender,
                'message': '메세지를 입력해주세요',
                'created_at': '',
                # 'unread_message_count': 0,
            })
            pass

    latest_messages.sort(key=lambda x: x['created_at'], reverse=True)

    return latest_messages


def current_chat(request, room_number, receiver_id):
    # 이미 생성된 채팅방 찾기
    already_room = ChatRoom.objects.filter(Q(Q(sender=request.user.id, receiver=receiver_id) | Q(sender=receiver_id, receiver=request.user.id))).first()

    if room_number == 0:
        if receiver_id == request.user.id:
            # 자기 자신에게 메시지를 보낼 수 없음
            return JsonResponse({"error": "You can't send messages to yourself."})
        if already_room:
            # 이미 생성된 채팅방이 있을 경우 해당 채팅방으로 이동
            room_number = already_room.id
        else:
            # 새 채팅방 생성
            receiver = UserProfile.objects.get(id=receiver_id)
            sender = UserProfile.objects.get(id=request.user.id)
            new_chat_room = ChatRoom.objects.create(sender=sender, receiver=receiver)
            room_number = new_chat_room.id

    current_room = ChatRoom.objects.get(pk=room_number)
    current_chat = ChatMessages.objects.filter(chat_room=current_room).order_by('created_at')

    first_unread_index = -1

    for chat in current_chat:
        if chat.read_or_not == False and chat.sender.id != request.user.id:
            chat.read_or_not = True
            chat.save()
            if first_unread_index == -1:
                first_unread_index = chat.id

    formatted_chat_msgs = [
        {
            'created_at': format_datetime(chat.created_at),
            'message': chat.message,
            'username': chat.sender.username,
            'is_read': chat.read_or_not,
            'id': chat.id,
        }
        for chat in current_chat
    ]

    context = {
        "room_number": room_number,
        "chat_msgs": formatted_chat_msgs,
        "latest_messages": get_rooms(request),
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

