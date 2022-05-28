from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .models import Post, Comment
from .forms import PostForm
from feed.models import PostEvent, CommentEvent, LikeDislikeEvent
import cloudinary
import cloudinary.uploader


class CreatePostAjaxView(View):
    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.has_media = True if request.FILES else False
            if post.has_media:
                post.image = request.FILES['image']

            post.author = request.user
            post.save()
            # need to return the post object
            avatar = request.user.profile.avatar_url

            post_event = PostEvent.objects.create(
                initiator=request.user,
                post=post,
            )
            post_event.save()

            post_data = {
                'author': str(post.author.profile),
                'author_url': f'/profiles/{post.author.username}',
                'avatar': avatar,
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
            like_event = LikeDislikeEvent.objects.filter(
                initiator=request.user,
                post=post,
                like=True,
            ).first()
            if like_event:
                like_event.delete()
        elif request.user in post.dislikes.all():
            post.dislikes.remove(request.user)
            dislike_event = LikeDislikeEvent.objects.filter(
                initiator=request.user,
                post=post,
                like=False,
            ).first()
            if dislike_event:
                dislike_event.delete()
        else:
            post.likes.add(request.user)
            like_event = LikeDislikeEvent.objects.create(
                initiator=request.user,
                post=post,
                like=True,
            )
            like_event.save()
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
            dislike_event = LikeDislikeEvent.objects.filter(
                initiator=request.user,
                post=post,
                like=False,
            ).first()
            if dislike_event:
                dislike_event.delete()
        elif request.user in post.likes.all():
            post.likes.remove(request.user)
            like_event = LikeDislikeEvent.objects.filter(
                initiator=request.user,
                post=post,
                like=True,
            ).first()
            if like_event:
                like_event.delete()
        else:
            post.dislikes.add(request.user)
            dislike_event = LikeDislikeEvent.objects.create(
                initiator=request.user,
                post=post,
                like=False,
            )
            dislike_event.save()
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
        post = Post.objects.get(id=post_id)
        comment_content = request.POST.get('comment_content')
        comment = Comment(
            author=request.user,
            post=post,
            content=comment_content
        )
        comment.save()
        comment_event = CommentEvent.objects.create(
            initiator=request.user,
            post=post,
            comment=comment,
        )
        comment_event.save()
        avatar = comment.author.profile.avatar_url
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
            like_event = LikeDislikeEvent.objects.filter(
                initiator=request.user,
                comment=comment,
                like=True,
            ).first()
            if like_event:
                like_event.delete()
        elif request.user in comment.dislikes.all():
            comment.dislikes.remove(request.user)
            dislike_event = LikeDislikeEvent.objects.filter(
                initiator=request.user,
                comment=comment,
                like=False,
            ).first()
            if dislike_event:
                dislike_event.delete()
        else:
            comment.likes.add(request.user)
            like_event = LikeDislikeEvent.objects.create(
                initiator=request.user,
                comment=comment,
                like=True,
            )
            like_event.save()
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
            dislike_event = LikeDislikeEvent.objects.filter(
                initiator=request.user,
                comment=comment,
                like=False,
            ).first()
            if dislike_event:
                dislike_event.delete()
        elif request.user in comment.likes.all():
            comment.likes.remove(request.user)
            like_event = LikeDislikeEvent.objects.filter(
                initiator=request.user,
                comment=comment,
                like=True,
            ).first()
            if like_event:
                like_event.delete()
        else:
            comment.dislikes.add(request.user)
            dislike_event = LikeDislikeEvent.objects.create(
                initiator=request.user,
                comment=comment,
                like=False,
            )
            dislike_event.save()
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


class EditPostAjaxView(View):
    def post(self, request, *args, **kwargs):
        post = Post.objects.get(id=request.POST.get('post_id'))
        if request.user == post.author:
            # remove 'post_id' from request.POST
            request_post = request.POST.copy()
            del request_post['post_id']
            form = PostForm(request_post, request.FILES, instance=post)
            if form.is_valid():
                # check if post had an image before
                # and if form doesn't have an image delete image from storage
                if post.image and not request.FILES.get('image'):
                    cloudinary.uploader.destroy(
                        post.image.public_id,
                        invalidate=True
                    )
                    post.image = None
                form.save()
                image = post.image
                if image:
                    image_url = image.url
                    post.has_media = True
                else:
                    image_url = None
                    post.has_media = False
                post.edited = True
                post.save()
                return JsonResponse({'success': True, 'image': image_url})
        return JsonResponse({'success': False, 'errors': form.errors})


class EditCommentAjaxView(View):
    def post(self, request, *args, **kwargs):
        comment = Comment.objects.get(id=request.POST.get('comment_id'))
        if request.user == comment.author:
            comment.content = request.POST.get('comment_content')
            comment.edited = True
            comment.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})


class DeletePostAjaxView(View):
    def post(self, request, *args, **kwargs):
        post_id = request.POST.get('post_id')
        post = Post.objects.get(id=post_id)
        if request.user == post.author:
            post.delete()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})


class DeleteCommentAjaxView(View):
    def post(self, request, *args, **kwargs):
        comment_id = request.POST.get('comment_id')
        comment = Comment.objects.get(id=comment_id)
        if request.user == comment.author:
            comment_count = comment.post.comments_count() - 1
            post_id = comment.post.id
            comment.delete()
            return JsonResponse(
                {
                    'success': True,
                    'comment_count': comment_count,
                    'post_id': post_id
                }
            )
        return JsonResponse({'success': False})
