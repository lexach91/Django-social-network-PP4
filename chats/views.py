from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
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
            # check if these users are friends
            if second_user.profile in request.user.profile.friends.all():
                chat = Chat.objects.create()
                chat.members.add(request.user, second_user)
                chat.save()
            else:
                # return 404
                return render(request, '404.html')
        if chat.messages.filter(is_read=False).exists():
            # mark all unread messages written by second_user as read
            chat.messages.filter(author=second_user, is_read=False).update(is_read=True)
        room_name = chat.id
        return render(request, 'chats/chat_detail.html', {'chat': chat, 'room_name': room_name, 'second_user': second_user})
    
    
class GetMessageTimeView(View):
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            message = get_object_or_404(Message, id=request.POST['message_id'])
            sent_at = message.sent_at
            return JsonResponse({'sent_at': sent_at})
        
class UpdateMessageReadStatusView(View):
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            message = get_object_or_404(Message, id=request.POST['message_id'])
            message.is_read = True
            message.save()
            return JsonResponse({'message_id': message.id})