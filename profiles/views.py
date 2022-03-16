from django.shortcuts import render
from django.views import View

from .models import Profile
# Create your views here.

class MyProfileView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'profiles/my_profile.html', {})
    
    
class UserProfileView(View):
    def get(self, request, username, *args, **kwargs):
        user_profile = Profile.objects.get(user__username=username)
        return render(request, 'profiles/user_profile.html', {'user_profile': user_profile})