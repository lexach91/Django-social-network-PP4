from django.shortcuts import render, reverse, redirect
from django.views import View
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from posts.forms import PostForm, CommentForm
from .forms import EditProfileInfoForm, ChangeAvatarForm

from .models import Profile


class MyProfileView(View):
    """Class based view for my profile page"""

    def get(self, request, *args, **kwargs):
        """Get method for my profile page"""
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
            'user_profile': request.user.profile,
        }
        return render(request, 'profiles/my_profile.html', context)


class UserProfileView(View):
    """Class based view for other user's profile pages"""

    def get(self, request, username, *args, **kwargs):
        """Get method for other user's profile page"""
        user_profile = Profile.objects.get(user__username=username)
        if user_profile.user == request.user:
            return HttpResponseRedirect(reverse('my_profile'))
        post_form = PostForm()
        comment_form = CommentForm()
        posts = user_profile.posts.all()
        context = {
            'post_form': post_form,
            'comment_form': comment_form,
            'posts': posts,
            'user_profile': user_profile,
        }
        return render(request, 'profiles/user_profile.html', context)


class EditAvatarAjaxView(View):
    """Class based ajax handler for changing an avatar"""

    def post(self, request, *args, **kwargs):
        """Post method for changing an avatar"""
        user = request.user
        new_avatar = request.FILES['avatar']
        user.profile.avatar = new_avatar
        user.profile.save()
        avatar_url = user.profile.avatar.url
        return JsonResponse({'success': True, 'avatar_url': avatar_url})


class EditProfileView(View):
    """Class based view for editing a user's profile"""

    def get(self, request, *args, **kwargs):
        """Get method for editing a user's profile"""
        profile_form = EditProfileInfoForm(instance=request.user.profile)
        password_form = PasswordChangeForm(user=request.user)
        password_form.fields['old_password'].widget.attrs['autofocus'] = False

        avatar_form = ChangeAvatarForm(instance=request.user.profile)
        context = {
            'profile_form': profile_form,
            'password_form': password_form,
            'avatar_form': avatar_form,
        }
        return render(request, 'profiles/edit_profile.html', context)

    def post(self, request, *args, **kwargs):
        """Post ajax handler for editing a user's profile"""
        # check which form was submitted and handle separately
        if request.POST['form_type'] == 'profile':
            profile_form = EditProfileInfoForm(
                request.POST, instance=request.user.profile)
            if profile_form.is_valid():
                profile_form.save()
                return JsonResponse({'success': True})
            return JsonResponse(
                {'success': False, 'errors': profile_form.errors}
            )
        if request.POST['form_type'] == 'password':
            password_form = PasswordChangeForm(request.POST)
            if password_form.is_valid():
                password_form.save()
                return JsonResponse({'success': True})
            return JsonResponse(
                {'success': False, 'errors': password_form.errors}
            )


class CheckUserOnlineStatusView(View):
    """Class based view for checking if a user is online"""

    def get(self, request, *args, **kwargs):
        """Get method for checking if a user is online"""
        if request.is_ajax():
            username = request.GET.get('username')
            user = User.objects.get(username=username)
            return JsonResponse({'online': user.profile.online})
        return JsonResponse({'success': False})


class ResetAvatarView(View):
    """Class based view for resetting a user's avatar"""

    def post(self, request, *args, **kwargs):
        """Post method for resetting a user's avatar"""
        if request.is_ajax():
            user = request.user
            user.profile.avatar = None
            user.profile.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})


class DeleteUserView(View):
    """Class based view for deleting an account"""

    def post(self, request, *args, **kwargs):
        """Post method for deleting an account"""
        if request.user.is_authenticated:
            user = request.user
            user.delete()
            return redirect('home')
