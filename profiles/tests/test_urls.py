"""Tests for the urls of the profiles app"""
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from profiles.views import (
    MyProfileView,
    UserProfileView,
    EditAvatarAjaxView,
    EditProfileView,
    CheckUserOnlineStatusView,
    ResetAvatarView,
    DeleteUserView
)


class TestUrls(SimpleTestCase):
    """Test the urls for the profiles app"""
    
    def test_my_profile_url_resolves(self):
        """Test the my profile url"""
        url = reverse('my_profile')
        self.assertEquals(resolve(url).func.view_class, MyProfileView)
        
    def test_user_profile_url_resolves(self):
        """Test the user profile url"""
        url = reverse('user_profile', args=['username'])
        self.assertEquals(resolve(url).func.view_class, UserProfileView)
        
    def test_edit_avatar_ajax_url_resolves(self):
        """Test the edit avatar ajax url"""
        url = reverse('edit_avatar_ajax')
        self.assertEquals(resolve(url).func.view_class, EditAvatarAjaxView)
        
    def test_edit_profile_url_resolves(self):
        """Test the edit profile url"""
        url = reverse('edit_profile')
        self.assertEquals(resolve(url).func.view_class, EditProfileView)
        
    def test_check_online_status_url_resolves(self):
        """Test the check online status url"""
        url = reverse('check_online')
        self.assertEquals(resolve(url).func.view_class, CheckUserOnlineStatusView)
        
    def test_reset_avatar_url_resolves(self):
        """Test the reset avatar url"""
        url = reverse('reset-avatar')
        self.assertEquals(resolve(url).func.view_class, ResetAvatarView)
        
    def test_delete_user_url_resolves(self):
        """Test the delete user url"""
        url = reverse('delete-user')
        self.assertEquals(resolve(url).func.view_class, DeleteUserView)
