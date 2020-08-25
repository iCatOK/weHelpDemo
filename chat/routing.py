from django.urls import re_path

from .consumers import ChatConsumer, ChatLobbyConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_id>\w+)/$', ChatConsumer),
    re_path(r'ws/lobby/$', ChatLobbyConsumer),
]