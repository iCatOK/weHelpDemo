from django.contrib.auth.decorators import login_required
from django.shortcuts import render
# Create your views here.
from django.utils.safestring import mark_safe
import json
from .models import Chat


def index(request):
    return render(request, 'chat/index.html')

@login_required
def lobby(request):
    return render(request, 'chat/lobby.html', {
        'email': mark_safe(json.dumps(request.user.email)),
    })

@login_required
def room(request, room_id):
    chat = Chat.objects.get(id=room_id)
    partner = chat.users.all()[0].email
    if chat.users.all()[0].email == request.user.email:
        partner = chat.users.all()[1].email
    return render(request, 'chat/room.html', {
        'room_id': room_id,
        'email': mark_safe(json.dumps(request.user.email)),
        'partner': partner
    })


