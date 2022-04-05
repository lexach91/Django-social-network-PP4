from django.urls import path
from .views import CreatePostAjaxView


urlpatterns = [
    path('create/', CreatePostAjaxView.as_view(), name='create_post_ajax'),
]
