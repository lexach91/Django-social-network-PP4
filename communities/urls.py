from django.urls import path
from .views import (
    UsersCommunitiesView,
    CommunityView,
    JoinCommunityView,
    LeaveCommunityView,
    CreateCommunityView,
    EditCommunityView,
    DeleteCommunityView,
)


urlpatterns = [
    path(
        '',
        UsersCommunitiesView.as_view(),
        name='users_communities'
    ),
    path(
        'create/',
        CreateCommunityView.as_view(),
        name='create_community'
    ),
    path(
        '<slug>/',
        CommunityView.as_view(),
        name='community'
    ),
    path(
        '<slug>/join/',
        JoinCommunityView.as_view(),
        name='join_community'
    ),
    path(
        '<slug>/leave/',
        LeaveCommunityView.as_view(),
        name='leave_community'
    ),
    path(
        '<slug>/edit/',
        EditCommunityView.as_view(),
        name='edit_community'),
    path(
        '<slug>/delete/',
        DeleteCommunityView.as_view(),
        name='delete_community'
    ),
]
