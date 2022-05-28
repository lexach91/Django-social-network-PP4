"""Tests for the forms of the profiles app."""
from django.test import TestCase
from profiles.forms import ChangeAvatarForm, EditProfileInfoForm
from datetime import date


class TestForms(TestCase):
    """Test forms of the profiles app."""
    
    def test_change_avatar_form_has_fields(self):
        """Test if the change avatar form has the correct fields."""
        form = ChangeAvatarForm()
        expected = ['avatar']
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)
        
    def test_change_avatar_form_is_valid(self):
        """Test if the change avatar form is valid."""
        form = ChangeAvatarForm({
            'avatar': open('static/images/default-bg.jpg', 'rb')
        })
        self.assertTrue(form.is_valid())
        
    def test_edit_profile_info_form_has_fields(self):
        """Test if the edit profile info form has the correct fields."""
        form = EditProfileInfoForm()
        expected = ['first_name', 'last_name', 'country', 'city', 'bio', 'birth_date']
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)
        
    def test_edit_profile_info_form_is_valid(self):
        """Test if the edit profile info form is valid."""
        form = EditProfileInfoForm({
            'first_name': 'Test',
            'last_name': 'Test',
            'country': 'Test',
            'city': 'Test',
            'bio': 'Test',
            'birth_date': date(2000, 1, 1)
        })
        self.assertTrue(form.is_valid())
