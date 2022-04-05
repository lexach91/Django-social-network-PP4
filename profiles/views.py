from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from posts.forms import PostForm

from .models import Profile
# Create your views here.

class MyProfileView(View):
    def get(self, request, *args, **kwargs):
        form = PostForm()
        posts = Profile.objects.get(user=request.user).posts.all()
        return render(request, 'profiles/my_profile.html', {'form': form, 'posts': posts})
    
    
class UserProfileView(View):
    def get(self, request, username, *args, **kwargs):
        user_profile = Profile.objects.get(user__username=username)
        form = PostForm()
        return render(request, 'profiles/user_profile.html', {'user_profile': user_profile, 'form': form})
