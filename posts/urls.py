from django.urls import path
from .views import (
    CreatePostAjaxView,
    LikePostAjaxView,
    DislikePostAjaxView,
    CreateCommentAjaxView,
    LikeCommentAjaxView,
    DislikeCommentAjaxView
)


urlpatterns = [
    path('create-post/', CreatePostAjaxView.as_view(), name='create_post_ajax'),
    path('like-post/', LikePostAjaxView.as_view(), name='like_post_ajax'),
    path('dislike-post/', DislikePostAjaxView.as_view(), name='dislike_post_ajax'),
    path('create-comment/', CreateCommentAjaxView.as_view(), name='create_comment_ajax'),
    path('like-comment/', LikeCommentAjaxView.as_view(), name='like_comment_ajax'),
    path('dislike-comment/', DislikeCommentAjaxView.as_view(), name='dislike_comment_ajax'),
]
