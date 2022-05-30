from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .models import Chat, Message
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


class MyMessagesView(View):
    """Class based view for my_messages page"""

    def get(self, request, *args, **kwargs):
        """GET method for my_messages page"""
        chats = Chat.objects.filter(members=request.user)
        return render(request, 'chats/my_messages.html', {'chats': chats})


class ChatView(View):
    """Class based view for chat page"""

    def get(self, request, *args, **kwargs):
        """GET method for chat page"""
        second_user = get_object_or_404(User, username=kwargs['username'])
        if second_user.profile in request.user.profile.friends.all():
            chat = Chat.objects.filter(members=request.user).filter(
                members=second_user).first()
            if not chat:
                # check if these users are friends
                chat = Chat.objects.create()
                chat.members.add(request.user, second_user)
                chat.save()
            if chat.messages.filter(is_read=False).exists():
                # mark all unread messages written by second_user as read
                chat.messages.filter(author=second_user,
                                     is_read=False).update(is_read=True)
            room_name = chat.id
            context = {
                'chat': chat,
                'room_name': room_name,
                'second_user': second_user,
            }
            return render(request, 'chats/chat_detail.html', context)
        else:
            return render(request, 'errors/404.html')


class GetMessageTimeView(View):
    """Class based ajax view for getting message time"""

    def post(self, request, *args, **kwargs):
        """POST method for getting message time"""
        if request.is_ajax():
            message = get_object_or_404(Message, id=request.POST['message_id'])
            sent_at = message.sent_at
            return JsonResponse({'sent_at': sent_at})


class UpdateMessageReadStatusView(View):
    """Class based ajax view for updating message read status"""

    def post(self, request, *args, **kwargs):
        """POST method for updating message read status"""
        if request.is_ajax():
            message = get_object_or_404(Message, id=request.POST['message_id'])
            message.is_read = True
            message.save()
            return JsonResponse({'message_id': message.id})
