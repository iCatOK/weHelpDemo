from chat.models import Message, Chat


def get_last_message(chat):
    return Message.objects.filter(chat=chat).order_by('-timestamp')[0]
