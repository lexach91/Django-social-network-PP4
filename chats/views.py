from django.shortcuts import render
from django.views import View
from .models import Chat, Message

# Create your views here.
class MyMessagesView(View):
    def get(self, request, *args, **kwargs):
        chats = Chat.objects.filter(members=request.user)
        return render(request, 'chats/my_messages.html', {'chats': chats})