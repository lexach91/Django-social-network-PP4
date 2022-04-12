from django.urls import path
from .views import UsersCommunitiesView, CommunityView


urlpatterns = [
    path('', UsersCommunitiesView.as_view(), name='users_communities'),
    path('<slug>/', CommunityView.as_view(), name='community'),
]
    