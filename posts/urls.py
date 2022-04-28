from django.urls import path
from .views import CreatePostAjaxView, LikePostAjaxView, DislikePostAjaxView


urlpatterns = [
    path('create/', CreatePostAjaxView.as_view(), name='create_post_ajax'),
    path('like/', LikePostAjaxView.as_view(), name='like_post_ajax'),
    path('dislike/', DislikePostAjaxView.as_view(), name='dislike_post_ajax'),
]
