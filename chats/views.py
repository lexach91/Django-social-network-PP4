from django.shortcuts import render
from django.views import View
from .models import Chat, Message

# Create your views here.
class MyMessagesView(View):
    def get(self, request, *args, **kwargs):
        chats = Chat.objects.filter(members=request.user)
        return render(request, 'chats/my_messages.html', {'chats': chats})
    
    
class ChatView(View):
    def get(self, request, *args, **kwargs):
        chat = Chat.objects.get(id=kwargs['chat_id'])
        # when the chat has been read, mark all messages as read
        if not chat.messages.filter(is_read=False).exists():
            chat.messages.update(is_read=True)
        return render(request, 'chats/chat.html', {'chat': chat})