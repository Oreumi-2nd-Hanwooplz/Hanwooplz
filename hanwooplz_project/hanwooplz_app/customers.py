import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatMessages, ChatRoom, UserProfile
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import timezone

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_number"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    @database_sync_to_async
    def get_room(self, room_number):
        return ChatRoom.objects.get(id=room_number)

    @database_sync_to_async
    def get_sender(self, username):
        try:
            return UserProfile.objects.get(username=username)
        except UserProfile.DoesNotExist:
            return None

    @database_sync_to_async
    def save_chat_message(self, room, sender, message, receiver, chat_uuid):
        chat_msg = ChatMessages(chat_room=room, sender=sender, message=message, read_or_not=False, receiver=receiver, chat_uuid=chat_uuid)
        chat_msg.save()

    @database_sync_to_async
    def get_chat_message_and_read_check(self, chat_uuid, receiver):
        try:
            chat_msg = ChatMessages.objects.get(chat_uuid=chat_uuid, receiver=receiver)
            chat_msg.read_or_not = True
            chat_msg.save()
        except ChatMessages.DoesNotExist:
            pass

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        if text_data_json['type'] == 'chat_message':
            message = text_data_json["message"]
            username = text_data_json["username"]
            receiver_username = text_data_json["receiver"]
            room_number = text_data_json["room_number"]
            created_at = text_data_json["created_at"]
            chat_uuid = text_data_json["chat_uuid"]

            room = await self.get_room(room_number)
            sender = await self.get_sender(username)
            receiver = await self.get_sender(receiver_username)

            await self.save_chat_message(room, sender, message, receiver, chat_uuid)

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name, {
                    "type": "chat_message",
                    "message": message,
                    "username": username,
                    "created_at": created_at,
                    "room_number": room_number,
                    'chat_uuid': chat_uuid,
                    'receiver': receiver_username
                }
            )

        if text_data_json['type'] == 'chat_message_read':
            receiver = text_data_json["receiver"]
            room_number = text_data_json["room_number"]
            chat_uuid = text_data_json["chat_uuid"]

            receive_user = await self.get_sender(receiver)

            await self.get_chat_message_and_read_check(chat_uuid, receive_user)

            await self.channel_layer.group_send(
                self.room_group_name, {
                    "type": "chat_message_read",
                    "chat_uuid": chat_uuid,
                    'room_number': room_number,
                    "receiver": receiver,
                    'is_read': True
                }
            )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]
        created_at = event["created_at"]
        room_number = event["room_number"]
        chat_uuid = event["chat_uuid"]

        # Send message and username to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            "message": message,
            "username": username,
            "created_at": created_at,
            "room_number": room_number, 
            'chat_uuid': chat_uuid
        }))
    
    async def chat_message_read(self, event):
        # 상대방에게 읽음 여부를 알리는 코드
        await self.send(text_data=json.dumps({
            'type': 'chat_message_read',
            "chat_uuid": event["chat_uuid"],
            'room_number': event['room_number'],
            "receiver": event["receiver"],
            "is_read": True
        }))

User = get_user_model()
class ChatListConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if not self.scope.get('user') or self.scope['user'].is_anonymous:
            await self.close()
        else:
            await self.accept()
            await self.get_chat_list()


    async def disconnect(self, close_code):
        pass

    def format_datetime(self, dt):
        today = timezone.now().date()
        if dt.date() == today:
            return dt.strftime("오늘 %p %I:%M")
        yesterday = today - timezone.timedelta(days=1)
        if dt.date() == yesterday:
            return dt.strftime("어제 %p %I:%M")
        return dt.strftime("%Y-%m-%d %p %I:%M")

    async def get_chat_list(self):
        user = self.scope['user']
        chat_rooms = ChatRoom.objects.filter(Q(sender=user) | Q(receiver=user))

        latest_messages = []
        for room in chat_rooms:
            try:
                unread_message_count = ChatMessages.objects.filter(
                    Q(chat_room=room),
                    ~Q(sender=user),
                    Q(read_or_not=False)
                ).count()

                latest_message = ChatMessages.objects.filter(chat_room=room.id).latest('created_at')

                receiver = None

                if latest_message.chat_room.sender == user:
                    receiver = latest_message.chat_room.receiver
                else:
                    receiver = latest_message.chat_room.sender

                latest_messages.append({
                    'chat_room_id': room.id,
                    'receiver_id': receiver.id,
                    'receiver': receiver.username,
                    'message': latest_message.message,
                    'created_at': self.format_datetime(latest_message.created_at),
                    'unread_message_count': unread_message_count,
                })
            except ChatMessages.DoesNotExist:
                pass

        latest_messages.sort(key=lambda x: x['created_at'], reverse=True)

        # 채팅방 목록 데이터를 클라이언트로 전송
        await self.send(text_data=json.dumps(latest_messages))