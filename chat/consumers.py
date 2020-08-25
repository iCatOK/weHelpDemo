import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import Message, Chat
from django.contrib.auth import get_user_model
User = get_user_model()


class ChatConsumer(WebsocketConsumer):
    def fetch_messages(self, data):
        room_id = data['room_id']
        messages = Message.last_10_messages(room_id)
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            'author': message.author.email,
            'content': message.content,
            'timestamp': str(message.timestamp)
        }

    def new_message(self, data):
        author = data['from']
        author_user = User.objects.filter(email=author)[0]
        chat = Chat.objects.get(id=data['room_id'])
        message = Message.objects.create(
            author=author_user,
            chat=chat,
            content=data['message'])

        message.chat = chat
        message.save()
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        print('new_message')
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps(message))


class ChatLobbyConsumer(WebsocketConsumer):
    def fetch_chats(self, data):
        email = data['from']
        chats = Chat.objects.filter(users__email=email)
        content = {
            'command': 'chats',
            'chats': self.chats_to_json(chats)
        }
        self.send_chat(content)

    def chats_to_json(self, chats):
        result = []
        for chat in chats:
            result.append(self.chat_to_json(chat))
        return result

    def chat_to_json(self, chat):
        return {
            'user1': chat.users.all()[0].email,
            'user2': chat.users.all()[1].email,
            'room_id': chat.chat_name,
        }

    def new_chat(self, data):
        author_email = data['from']
        receiver = data['receiver']

        author_user = User.objects.filter(email=author_email)[0]

        try:
            receiver_user = User.objects.filter(email=receiver)[0]
        except NameError:
            return

        chat = Chat.objects.create()
        chat.chat_name = chat.id
        chat.users.add(author_user)
        chat.users.add(receiver_user)
        chat.save()

        content = {
            'command': 'new_chat',
            'chat': self.chat_to_json(chat)
        }

        return self.send_chat_new(content)

    commands = {
        'fetch_chats': fetch_chats,
        'new_chat': new_chat
    }

    def connect(self):
        self.room_name = 'lobby'
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        print('chat-received')
        self.commands[data['command']](self, data)

    def send_chat_new(self, chat):
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_new',
                'chat': chat
            }
        )

    def send_chat(self, chat):
        self.send(text_data=json.dumps(chat))

    # Receive message from room group
    def chat_new(self, event):
        chat = event['chat']
        print('sending')
        # Send message to WebSocket
        self.send(text_data=json.dumps(chat))
