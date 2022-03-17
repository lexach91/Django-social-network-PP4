from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import JsonResponse
from .models import FriendRequest
from profiles.models import Profile

# Create your views here.
class SendFriendRequest(View):
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            from_profile = request.user.profile
            to_profile = get_object_or_404(Profile, id=kwargs['id'])
            friend_request = FriendRequest(
                from_profile=from_profile,
                to_profile=to_profile
            )
            friend_request.save()
            return JsonResponse({'status': 'ok'})
        return JsonResponse({'status': 'error'})


class AcceptFriendRequest(View):
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            friend_request = get_object_or_404(FriendRequest, id=kwargs['id'])
            friend_request.accepted = True
            accepting_profile = friend_request.to_profile
            accepted_profile = friend_request.from_profile
            accepting_profile.friends.add(accepted_profile)
            accepted_profile.friends.add(accepting_profile)
            accepting_profile.save()
            accepted_profile.save()
            friend_request.save()
            return JsonResponse({'status': 'ok'})
        return JsonResponse({'status': 'error'})