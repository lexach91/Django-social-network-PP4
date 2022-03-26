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
            profile_id = request.POST.get('id')
            to_profile = get_object_or_404(Profile, id=profile_id)
            # need to check if the request is already sent
            if FriendRequest.objects.filter(
                from_profile=from_profile,
                to_profile=to_profile
            ).exists():
                return JsonResponse({'status': 'error'})
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
            request_id = request.POST.get('id')
            friend_request = get_object_or_404(FriendRequest, id=request_id)
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
    
    
class DeclineFriendRequest(View):
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            request_id = request.POST.get('id')
            friend_request = get_object_or_404(FriendRequest, id=request_id)
            friend_request.declined = True
            friend_request.save()
            return JsonResponse({'status': 'ok'})
        return JsonResponse({'status': 'error'})
    
class RemoveFriend(View):
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            remover = request.user.profile
            friend = get_object_or_404(Profile, id=request.POST.get('id'))
            remover.friends.remove(friend)
            friend.friends.remove(remover)
            remover.save()
            friend.save()
            return JsonResponse({'status': 'ok'})

class MyFriendsView(View):
    def get(self, request, *args, **kwargs):
        friends = request.user.profile.friends.all()
        return render(request, 'friends/my_friends.html', {
            'friends': friends,
        })