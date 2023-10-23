import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from datetime import datetime
from .views import get_user_from_token,update_online_status

online_users = {}

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        token = self.scope["query_string"].decode("utf-8")
        user =   get_user_from_token(token)
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        print('room created',self.room_group_name)
        await self.accept()
        await update_online_status(True, user)

    async def disconnect(self, close_code):
        token = self.scope["query_string"].decode("utf-8")
        user =   get_user_from_token(token)
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await update_online_status(False, user)
       

        print('room disconnected',self.room_group_name)
    
    async def receive(self, text_data):
        print('message received')
        try:
            text_data_json = json.loads(text_data)
            sender = text_data_json.get('sender')
            receiver = text_data_json.get('receiver')
            message_content = text_data_json.get('message_content')

            if sender and receiver and message_content:
                message = {
                    'message_content': message_content,
                    'sender': sender,
                    'receiver': receiver
                }

             
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat.message',
                        'message_content': message_content,
                        'sender': sender,
                        'receiver': receiver
                    }
                )
            else:
                await self.send(text_data=json.dumps({'error': 'Invalid message format'}))
    
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({'error': 'Invalid JSON format'}))

    async def chat_message(self,event):
        message=event['message_content']
        sender=event['sender']
        receiver=event['receiver']
        
        timestamp = datetime.now().isoformat()
        await self.send(text_data=json.dumps({
            'message_content': message,
            'sender':sender,
            'receiver':receiver,
            'timestamp': timestamp 
        }))
    
    
class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"notification_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        print('room created',self.room_group_name)
        await self.accept()

    async def disconnect(self, close_code):
        
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
       

        print('room disconnected',self.room_group_name)
    
    async def receive(self,text_data):
        
        try:
            text_data_json = json.loads(text_data)
            username = text_data_json.get('text')
            print('yyy')
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'notification.message',
                    'notification_data':  f"Your request for {username} has approved",
                }
            )
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({'error': 'Invalid JSON format'}))


    async def notification_message(self, event):
        notification_data = event['notification_data']

        await self.send(text_data=json.dumps({
            'notification_data': notification_data,
        }))
    
    


    