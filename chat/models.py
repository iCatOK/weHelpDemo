from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()


class Chat(models.Model):
    chat_name = models.TextField()
    users = models.ManyToManyField(User, related_name='chats')

    def __str__(self):
        return self.chat_name

    def all_chats(self):
        return Chat.objects.order_by('-timestamp').all()


class Message(models.Model):
    author = models.ForeignKey(User, related_name='author_messages', on_delete=models.DO_NOTHING)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    chat = models.ForeignKey(Chat, default=1, related_name='chat_messages', on_delete=models.CASCADE)

    def __str__(self):
        return self.author.name

    def last_10_messages(room_id):
        return Message.objects.filter(chat_id=room_id).order_by('timestamp').all()[:10]
