from django.urls import path
from .views import (
    CreatePostAjaxView,
    LikePostAjaxView,
    DislikePostAjaxView,
    CreateCommentAjaxView,
    LikeCommentAjaxView,
    DislikeCommentAjaxView,
    EditPostAjaxView,
    EditCommentAjaxView,
    DeleteCommentAjaxView,
    DeletePostAjaxView
)


urlpatterns = [
    path('create-post/', CreatePostAjaxView.as_view(), name='create_post_ajax'),
    path('like-post/', LikePostAjaxView.as_view(), name='like_post_ajax'),
    path('dislike-post/', DislikePostAjaxView.as_view(), name='dislike_post_ajax'),
    path('create-comment/', CreateCommentAjaxView.as_view(), name='create_comment_ajax'),
    path('like-comment/', LikeCommentAjaxView.as_view(), name='like_comment_ajax'),
    path('dislike-comment/', DislikeCommentAjaxView.as_view(), name='dislike_comment_ajax'),
    path('edit-post/', EditPostAjaxView.as_view(), name='edit_post_ajax'),
    path('edit-comment/', EditCommentAjaxView.as_view(), name='edit_comment_ajax'),
    path('delete-comment/', DeleteCommentAjaxView.as_view(), name='delete_comment_ajax'),
    path('delete-post/', DeletePostAjaxView.as_view(), name='delete_post_ajax'),
]
