from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .models import Post
from .forms import PostForm


# Create your views here.
class CreatePostAjaxView(View):
    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            # need to return the post object
            if post.author.profile.avatar:
                avatar = post.author.profile.avatar.url
            else:
                avatar = None
            post_data = {
                'author': str(post.author.profile),
                'avatar': avatar,
                # created_at should be in format as it is in temlate date:"d/m/Y H:i"
                'created_at': post.created_at.strftime("%d/%m/%Y %H:%M"),
                'content': post.content,
            }
            return JsonResponse({'success': True, 'post': post_data})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})