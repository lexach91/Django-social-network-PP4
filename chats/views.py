from django.shortcuts import render
from django.views import View
from .models import Chat, Message
from django.contrib.auth.models import User
# get_object_or_404 import
from django.shortcuts import get_object_or_404

# Create your views here.
class MyMessagesView(View):
    def get(self, request, *args, **kwargs):
        chats = Chat.objects.filter(members=request.user)
        return render(request, 'chats/my_messages.html', {'chats': chats})
    
    
class ChatView(View):
    def get(self, request, *args, **kwargs):
        second_user = get_object_or_404(User, username=kwargs['username'])
        chat = Chat.objects.filter(members=request.user).filter(members=second_user).first()
        if not chat:
            chat = Chat.objects.create(members=request.user)
            chat.members.add(second_user)
            chat.save()
        if not chat.messages.filter(is_read=False).exists():
            chat.messages.update(is_read=True)
        return render(request, 'chats/chat_detail.html', {'chat': chat})