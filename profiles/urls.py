from django.urls import path
from .views import (
    MyProfileView,
    UserProfileView,
    EditAvatarAjaxView,
    EditProfileView,
    CheckUserOnlineStatusView,
    ResetAvatarView,
    DeleteUserView
)

urlpatterns = [
    path('my_profile/', MyProfileView.as_view(), name='my_profile'),
    path('my_profile/edit_avatar/',
         EditAvatarAjaxView.as_view(), name='edit_avatar_ajax'),
    path('my_profile/edit/', EditProfileView.as_view(), name='edit_profile'),
    path('my_profile/reset_avatar/',
         ResetAvatarView.as_view(), name='reset-avatar'),
    path('my_profile/delete/', DeleteUserView.as_view(), name='delete-user'),
    path('check_online/',
         CheckUserOnlineStatusView.as_view(), name='check_online'),
    path('<str:username>/', UserProfileView.as_view(), name='user_profile'),
]
