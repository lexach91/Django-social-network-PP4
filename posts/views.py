from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .models import Post, Comment
from .forms import PostForm
from feed.models import PostEvent, CommentEvent, LikeDislikeEvent
import cloudinary
import cloudinary.uploader


class CreatePostAjaxView(View):
    """Class based ajax view for creating post"""

    def post(self, request, *args, **kwargs):
        """POST ajax handler for creating post"""
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.has_media = True if request.FILES else False
            if post.has_media:
                post.image = request.FILES['image']

            post.author = request.user
            post.save()

            avatar = request.user.profile.avatar_url

            post_event = PostEvent.objects.create(
                initiator=request.user,
                post=post,
            )
            post_event.save()

            # forming the post data to be sent to the client
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
    """Class based ajax view for liking a post"""

    def post(self, request, *args, **kwargs):
        """POST ajax handler for liking a post"""
        post_id = request.POST.get('post_id')
        post = Post.objects.get(id=post_id)
        if request.user in post.likes.all():
            # one user can like a post only once
            post.likes.remove(request.user)
            like_event = LikeDislikeEvent.objects.filter(
                initiator=request.user,
                post=post,
                like=True,
            ).first()
            if like_event:
                like_event.delete()
        elif request.user in post.dislikes.all():
            # one user can either like or dislike a post
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

        # forming the data to be sent to the client
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
    """Class based ajax view for disliking a post"""

    def post(self, request, *args, **kwargs):
        """POST ajax handler for disliking a post"""
        post_id = request.POST.get('post_id')
        post = Post.objects.get(id=post_id)
        if request.user in post.dislikes.all():
            # one user can dislike a post only once
            post.dislikes.remove(request.user)
            dislike_event = LikeDislikeEvent.objects.filter(
                initiator=request.user,
                post=post,
                like=False,
            ).first()
            if dislike_event:
                dislike_event.delete()
        elif request.user in post.likes.all():
            # one user can either like or dislike a post
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

        # forming the data to be sent to the client
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
    """Class based ajax view for creating comment"""

    def post(self, request, *args, **kwargs):
        """POST ajax handler for creating comment"""
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

        # forming the comment data to be sent to the client
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
    """Class based ajax view for liking a comment"""

    def post(self, request, *args, **kwargs):
        comment_id = request.POST.get('comment_id')
        comment = Comment.objects.get(id=comment_id)
        if request.user in comment.likes.all():
            # one user can like a comment only once
            comment.likes.remove(request.user)
            like_event = LikeDislikeEvent.objects.filter(
                initiator=request.user,
                comment=comment,
                like=True,
            ).first()
            if like_event:
                like_event.delete()
        elif request.user in comment.dislikes.all():
            # one user can either like or dislike a comment
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

        # forming the data to be sent to the client
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
    """Class based ajax view for disliking a comment"""

    def post(self, request, *args, **kwargs):
        """POST ajax handler for disliking a comment"""
        comment_id = request.POST.get('comment_id')
        comment = Comment.objects.get(id=comment_id)
        if request.user in comment.dislikes.all():
            # one user can dislike a comment only once
            comment.dislikes.remove(request.user)
            dislike_event = LikeDislikeEvent.objects.filter(
                initiator=request.user,
                comment=comment,
                like=False,
            ).first()
            if dislike_event:
                dislike_event.delete()
        elif request.user in comment.likes.all():
            # one user can either like or dislike a comment
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

        # forming the data to be sent to the client
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
    """Class based ajax view for editing a post"""

    def post(self, request, *args, **kwargs):
        """POST ajax handler for editing a post"""
        post = Post.objects.get(id=request.POST.get('post_id'))
        if request.user == post.author:
            # remove 'post_id' from request.POST
            # so we can use the same post form for editing
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
    """Class based ajax view for editing a comment"""

    def post(self, request, *args, **kwargs):
        """POST ajax handler for editing a comment"""
        comment = Comment.objects.get(id=request.POST.get('comment_id'))
        if request.user == comment.author:
            comment.content = request.POST.get('comment_content')
            comment.edited = True
            comment.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})


class DeletePostAjaxView(View):
    """Class based ajax view for deleting a post"""

    def post(self, request, *args, **kwargs):
        """POST ajax handler for deleting a post"""
        post_id = request.POST.get('post_id')
        post = Post.objects.get(id=post_id)
        # check if the user is the author of the post
        if request.user == post.author:
            post.delete()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})


class DeleteCommentAjaxView(View):
    """Class based ajax view for deleting a comment"""

    def post(self, request, *args, **kwargs):
        """POST ajax handler for deleting a comment"""
        comment_id = request.POST.get('comment_id')
        comment = Comment.objects.get(id=comment_id)
        # check if the user is the author of the comment
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
