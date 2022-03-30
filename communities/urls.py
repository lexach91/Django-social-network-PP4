from django.urls import path
from .views import UsersCommunitiesView


urlpatterns = [
    path('', UsersCommunitiesView.as_view(), name='users_communities'),
]
    