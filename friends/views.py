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
            profile_id = request.POST.get('profile_id')
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
            accepting_profile = request.user.profile
            profile_id = request.POST.get('profile_id')
            accepted_profile = get_object_or_404(Profile, id=profile_id)
            friend_request = get_object_or_404(
                FriendRequest,
                from_profile=accepted_profile,
                to_profile=accepting_profile
            )
            if friend_request:
                friend_request.accepted = True
                friend_request.declined = False
                accepting_profile.friends.add(accepted_profile)
                accepted_profile.friends.add(accepting_profile)
                friend_request.save()
                accepting_profile.save()
                accepted_profile.save()
                return JsonResponse({'status': 'ok'})
            return JsonResponse({'status': 'error'})
        return JsonResponse({'status': 'error'})

    
    
class DeclineFriendRequest(View):
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            declining_profile = request.user.profile
            profile_id = request.POST.get('profile_id')
            declined_profile = get_object_or_404(Profile, id=profile_id)
            friend_request = get_object_or_404(
                FriendRequest,
                from_profile=declined_profile,
                to_profile=declining_profile
            )
            if friend_request:
                friend_request.accepted = False
                friend_request.declined = True
                friend_request.save()
                return JsonResponse({'status': 'ok'})
            return JsonResponse({'status': 'error'})
        return JsonResponse({'status': 'error'})
    
class RemoveFriend(View):
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            remover = request.user.profile
            friend = get_object_or_404(Profile, id=request.POST.get('profile_id'))
            remover.friends.remove(friend)
            friend.friends.remove(remover)
            remover.save()
            friend.save()
            return JsonResponse({'status': 'ok'})
        
        
class CancelFriendRequest(View):
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            profile1 = request.user.profile
            profile2 = get_object_or_404(Profile, id=request.POST.get('profile_id'))
            friend_request = get_object_or_404(
                FriendRequest,
                from_profile=profile1,
                to_profile=profile2
            )
            friend_request.delete()
            return JsonResponse({'status': 'ok'})
        return JsonResponse({'status': 'error'})

class MyFriendsView(View):
    def get(self, request, *args, **kwargs):
        friends = request.user.profile.friends.all()
        pending_requests = FriendRequest.get_pending_requests().filter(
            to_profile=request.user.profile
        )
        return render(request, 'friends/my_friends.html', {
            'friends': friends,
            'pending_requests': pending_requests
        })
