"""Tests for the urls of the friends app"""
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from friends.views import (
    SendFriendRequest,
    AcceptFriendRequest,
    DeclineFriendRequest,
    RemoveFriend,
    MyFriendsView,
    CancelFriendRequest
)


class TestUrls(SimpleTestCase):
    """Test the urls for the friends app"""
    
    def test_send_friend_request_url_resolves(self):
        """Test the send friend request url"""
        url = reverse('send-friend-request')
        self.assertEquals(resolve(url).func.view_class, SendFriendRequest)
        
    def test_accept_friend_request_url_resolves(self):
        """Test the accept friend request url"""
        url = reverse('accept-friend-request')
        self.assertEquals(resolve(url).func.view_class, AcceptFriendRequest)
        
    def test_decline_friend_request_url_resolves(self):
        """Test the decline friend request url"""
        url = reverse('decline-friend-request')
        self.assertEquals(resolve(url).func.view_class, DeclineFriendRequest)
        
    def test_cancel_friend_request_url_resolves(self):
        """Test the cancel friend request url"""
        url = reverse('cancel-friend-request')
        self.assertEquals(resolve(url).func.view_class, CancelFriendRequest)
        
    def test_remove_friend_url_resolves(self):
        """Test the remove friend url"""
        url = reverse('remove-friend')
        self.assertEquals(resolve(url).func.view_class, RemoveFriend)
        
    def test_my_friends_url_resolves(self):
        """Test the my friends url"""
        url = reverse('my-friends')
        self.assertEquals(resolve(url).func.view_class, MyFriendsView)
