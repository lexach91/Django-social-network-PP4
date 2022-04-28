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
                'author_url': f'/profiles/{post.author.username}',
                'avatar': avatar,
                # created_at should be in format as it is in temlate date:"d/m/Y H:i"
                'created_at': post.created_at.strftime("%d/%m/%Y %H:%M"),
                'content': post.content,
            }
            return JsonResponse({'success': True, 'post': post_data})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
        

class LikePostAjaxView(View):
    def post(self, request, *args, **kwargs):
        post_id = request.POST.get('post_id')
        post = Post.objects.get(id=post_id)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        elif request.user in post.dislikes.all():
            post.dislikes.remove(request.user)
            # post.likes.add(request.user)
        else:
            post.likes.add(request.user)
        post.save()
        likes_count = post.get_likes()
        dislikes_count = post.get_dislikes()
        liked = True if request.user in post.likes.all() else False
        disliked = True if request.user in post.dislikes.all() else False
        return JsonResponse({
            'success': True,
            'likes_count': likes_count,
            'dislikes_count': dislikes_count,
            'liked': liked,
            'disliked': disliked
            })
    
class DislikePostAjaxView(View):
    def post(self, request, *args, **kwargs):
        post_id = request.POST.get('post_id')
        post = Post.objects.get(id=post_id)
        if request.user in post.dislikes.all():
            post.dislikes.remove(request.user)
        elif request.user in post.likes.all():
            post.likes.remove(request.user)
            # post.dislikes.add(request.user)
        else:
            post.dislikes.add(request.user)
        post.save()
        likes_count = post.get_likes()
        dislikes_count = post.get_dislikes()
        liked = True if request.user in post.likes.all() else False
        disliked = True if request.user in post.dislikes.all() else False
        return JsonResponse({
            'success': True,
            'likes_count': likes_count,
            'dislikes_count': dislikes_count,
            'disliked': disliked,
            'liked': liked
            })