from django.urls import path
from .views import SendFriendRequest, AcceptFriendRequest, DeclineFriendRequest


urlpatterns = [
    path('send-friend-request/', SendFriendRequest.as_view(), name='send-friend-request'),
    path('accept-friend-request/', AcceptFriendRequest.as_view(), name='accept-friend-request'),
    path('decline-friend-request/', DeclineFriendRequest.as_view(), name='decline-friend-request'),
]
