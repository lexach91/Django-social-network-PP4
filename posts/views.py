from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .models import Post, Comment
from .forms import PostForm


# Create your views here.
class CreatePostAjaxView(View):
    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST, request.FILES)
        print(form.is_valid())
        if form.is_valid():
            print(form.cleaned_data)
            post = form.save(commit=False)
            post.has_media = True if request.FILES else False
            if post.has_media:
                post.image = request.FILES['image']
            
            post.author = request.user
            post.save()
            # need to return the post object
            avatar = None
            if request.user.profile.avatar:
                avatar = request.user.profile.avatar.url
                print(avatar)
                print(request.user.profile)
                print(request.user.profile.avatar)
                print(request.user.profile.avatar.url)
            print(avatar)
            post_data = {
                'author': str(post.author.profile),
                'author_url': f'/profiles/{post.author.username}',
                'avatar': avatar,
                # created_at should be in format as it is in temlate date:"d/m/Y H:i"
                'created_at': post.created_at.strftime("%d/%m/%Y %H:%M"),
                'content': post.content,
                'id': post.id,
                'has_media': post.has_media,
                'image': post.image.url if post.has_media else None,
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
        
class CreateCommentAjaxView(View):
    def post(self, request, *args, **kwargs):
        post_id = request.POST.get('post_id')
        print(post_id)
        post = Post.objects.get(id=post_id)
        comment_content = request.POST.get('comment_content')
        comment = Comment(
            author=request.user,
            post=post,
            content=comment_content
        )
        comment.save()
        if comment.author.profile.avatar:
            avatar = comment.author.profile.avatar.url
        else:
            avatar = None
        comment_data = {
            'author': str(comment.author.profile),
            'author_url': f'/profiles/{comment.author.username}',
            'avatar': avatar,
            'created_at': comment.created_at.strftime("%d/%m/%Y %H:%M"),
            'content': comment.content,
            'id': comment.id,
            'comment_count': comment.post.comments_count()
        }
        return JsonResponse({'success': True, 'comment': comment_data})

class LikeCommentAjaxView(View):
    def post(self, request, *args, **kwargs):
        comment_id = request.POST.get('comment_id')
        comment = Comment.objects.get(id=comment_id)
        if request.user in comment.likes.all():
            comment.likes.remove(request.user)
        elif request.user in comment.dislikes.all():
            comment.dislikes.remove(request.user)
            # comment.likes.add(request.user)
        else:
            comment.likes.add(request.user)
        comment.save()
        likes_count = comment.get_likes()
        dislikes_count = comment.get_dislikes()
        liked = True if request.user in comment.likes.all() else False
        disliked = True if request.user in comment.dislikes.all() else False
        return JsonResponse({
            'success': True,
            'likes_count': likes_count,
            'dislikes_count': dislikes_count,
            'liked': liked,
            'disliked': disliked
            })
        
class DislikeCommentAjaxView(View):
    def post(self, request, *args, **kwargs):
        comment_id = request.POST.get('comment_id')
        comment = Comment.objects.get(id=comment_id)
        if request.user in comment.dislikes.all():
            comment.dislikes.remove(request.user)
        elif request.user in comment.likes.all():
            comment.likes.remove(request.user)
            # comment.dislikes.add(request.user)
        else:
            comment.dislikes.add(request.user)
        comment.save()
        likes_count = comment.get_likes()
        dislikes_count = comment.get_dislikes()
        liked = True if request.user in comment.likes.all() else False
        disliked = True if request.user in comment.dislikes.all() else False
        return JsonResponse({
            'success': True,
            'likes_count': likes_count,
            'dislikes_count': dislikes_count,
            'disliked': disliked,
            'liked': liked
            })
