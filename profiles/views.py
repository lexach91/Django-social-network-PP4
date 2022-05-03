from django.shortcuts import render, reverse, redirect
from django.views import View
from django.http import JsonResponse, HttpResponseRedirect
from posts.forms import PostForm, CommentForm
from .forms import EditProfileInfoForm, ChangeAvatarForm

from .models import Profile
# Create your views here.

class MyProfileView(View):
    def get(self, request, *args, **kwargs):
        post_form = PostForm()
        comment_form = CommentForm()
        posts = Profile.objects.get(user=request.user).posts.all()
        edit_profile_form = EditProfileInfoForm(instance=request.user.profile)
        edit_avatar_form = ChangeAvatarForm(instance=request.user.profile)
        context = {
            'post_form': post_form,
            'comment_form': comment_form,
            'posts': posts,
            'edit_profile_form': edit_profile_form,
            'edit_avatar_form': edit_avatar_form,
        }
        return render(request, 'profiles/my_profile.html', context)
    
    
class UserProfileView(View):
    def get(self, request, username, *args, **kwargs):
        user_profile = Profile.objects.get(user__username=username)
        if user_profile.user == request.user:
            return HttpResponseRedirect(reverse('my_profile'))
        post_form = PostForm()
        comment_form = CommentForm()
        posts = user_profile.posts.all()
        return render(request, 'profiles/user_profile.html', {'user_profile': user_profile, 'post_form': post_form, 'comment_form':comment_form, 'posts': posts})
