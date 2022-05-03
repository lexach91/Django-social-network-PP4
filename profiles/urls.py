from django.urls import path
from .views import MyProfileView, UserProfileView, EditAvatarAjaxView

urlpatterns = [
    path('my_profile/', MyProfileView.as_view(), name='my_profile'),
    path('<str:username>/', UserProfileView.as_view(), name='user_profile'),
    path('my_profile/edit_avatar/', EditAvatarAjaxView.as_view(), name='edit_avatar_ajax'),
]