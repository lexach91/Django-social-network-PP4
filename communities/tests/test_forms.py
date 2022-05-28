"""Tests for the forms of the communities app."""
from django.test import TestCase
from communities.forms import CommunityForm
from django.contrib.auth.models import User


class TestCommunityForm(TestCase):
    """Test community form."""

    def setUp(self):
        """Set up test users."""
        self.user = User.objects.create_user(
            username='user',
            password='Testuser1',
            first_name='User',
            last_name='Test',
            email='test@test.com'
        )

    def test_form_has_fields(self):
        """Test if the form has the correct fields."""
        form = CommunityForm()
        expected = ['name', 'description', 'bg_image', 'logo']
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)

    def test_form_is_valid(self):
        """Test if the form is valid."""
        form = CommunityForm({
            'name': 'Test community',
            'description': 'Test description',
            'bg_image': open('static/images/default-bg.jpg', 'rb'),
            'logo': open('static/images/default-logo.png', 'rb')
        })
        self.assertTrue(form.is_valid())

    def test_form_not_valid(self):
        """Test if the form is not valid."""
        form = CommunityForm({
            'name': '',  # The only required field
            'description': 'Test description',
            'bg_image': open('static/images/default-bg.jpg', 'rb'),
            'logo': open('static/images/default-logo.png', 'rb')
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['name'], [u'This field is required.'])
