from django.urls import path
from .views import (
    MyProfileView,
    UserProfileView,
    EditAvatarAjaxView,
    EditProfileView,
    CheckUserOnlineStatusView,
    ResetAvatarView
)

urlpatterns = [
    path('my_profile/', MyProfileView.as_view(), name='my_profile'),
    path('<str:username>/', UserProfileView.as_view(), name='user_profile'),
    path('my_profile/edit_avatar/', EditAvatarAjaxView.as_view(), name='edit_avatar_ajax'),
    path('my_profile/edit/', EditProfileView.as_view(), name='edit_profile'),
    path('check_online/', CheckUserOnlineStatusView.as_view(), name='check_online'),
    path('my_profile/reset_avatar/', ResetAvatarView.as_view(), name='reset-avatar')
]