from django.shortcuts import render, reverse, redirect
from django.views import View
from django.http import JsonResponse, HttpResponseRedirect
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
        if user_profile.user == request.user:
            return HttpResponseRedirect(reverse('my_profile'))
        form = PostForm()
        posts = user_profile.posts.all()
        return render(request, 'profiles/user_profile.html', {'user_profile': user_profile, 'form': form, 'posts': posts})
