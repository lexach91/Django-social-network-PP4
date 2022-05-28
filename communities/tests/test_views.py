"""Tests for the views of the communities app."""
from django.test import TestCase, Client
from django.urls import reverse
from communities.models import Community
from django.contrib.auth.models import User


class TestViews(TestCase):
    """Tests for the views of the communities app."""

    def setUp(self):
        """Set up test users"""
        self.user1 = User.objects.create_user(
            username='user1',
            password='Testuser1',
            first_name='User1',
            last_name='Test',
            email='test1@test.com'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='Testuser2',
            first_name='User2',
            last_name='Test',
            email='test2@test.com'
        )
        self.client = Client()
        self.users_communities_url = reverse('users_communities')
        self.create_community_url = reverse('create_community')
        self.community_url = reverse(
            'community', kwargs={'slug': 'test-community'})
        self.join_community_url = reverse('join_community', kwargs={
                                          'slug': 'test-community'})
        self.leave_community_url = reverse('leave_community', kwargs={
                                           'slug': 'test-community'})
        self.edit_community_url = reverse('edit_community', kwargs={
                                          'slug': 'test-community'})
        self.delete_community_url = reverse(
            'delete_community', kwargs={'slug': 'test-community'})

    def test_users_communities_view(self):
        """Test users communities view"""
        self.client.login(username='user1', password='Testuser1')
        response = self.client.get(self.users_communities_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'communities/users_communities.html')
        self.assertEqual(response.context['user'], self.user1)
        self.assertEqual(response.context['communities'].count(), 0)
        community1 = Community.objects.create(
            name='Test community', creator=self.user1)
        community1.members.add(self.user1)
        response = self.client.get(self.users_communities_url)
        self.assertEqual(response.context['communities'].count(), 1)
        community2 = Community.objects.create(
            name='Test community 2', creator=self.user2)
        community2.members.add(self.user1)
        response = self.client.get(self.users_communities_url)
        self.assertEqual(response.context['communities'].count(), 2)

    def test_create_community_view(self):
        """Test create community view"""
        self.client.login(username='user1', password='Testuser1')
        response = self.client.get(self.create_community_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'communities/create_community.html')
        self.assertEqual(response.context['user'], self.user1)
        self.assertEqual(response.context['form']['name'].value(), None)
        self.assertEqual(response.context['form']['description'].value(), None)
        self.assertEqual(response.context['form']['bg_image'].value(), None)
        self.assertEqual(response.context['form']['logo'].value(), None)

        response = self.client.post(self.create_community_url, {
            'name': 'Test community',
            'description': 'Test description',
            'bg_image': '',
            'logo': ''
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.community_url)
        self.assertEqual(Community.objects.count(), 1)
        self.assertEqual(Community.objects.first().name, 'Test community')
        self.assertEqual(Community.objects.first().description,
                         'Test description')
        self.assertEqual(Community.objects.first().bg_image, None)
        self.assertEqual(Community.objects.first().logo, None)
        self.assertEqual(Community.objects.first().creator, self.user1)
        self.assertEqual(Community.objects.first().members.count(), 1)
        self.assertEqual(Community.objects.first().members.first(), self.user1)
        community = Community.objects.first()
        community.delete()
        bg_image_file = open('static/images/default-bg.jpg', 'rb')
        logo_file = open('static/images/default-logo.png', 'rb')
        form_data = {
            'name': 'Test community',
            'description': 'Test description',
            'bg_image': bg_image_file,
            'logo': logo_file
        }
        response = self.client.post(self.create_community_url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.community_url)
        self.assertEqual(Community.objects.count(), 1)
        self.assertEqual(Community.objects.first().name, 'Test community')
        self.assertEqual(Community.objects.first().description,
                         'Test description')
        self.assertTrue(
            'res.cloudinary.com' in Community.objects.first().bg_image.url)
        self.assertTrue(
            'res.cloudinary.com' in Community.objects.first().logo.url)
        self.assertEqual(Community.objects.first().creator, self.user1)
        self.assertEqual(Community.objects.first().members.count(), 1)
        self.assertEqual(Community.objects.first().members.first(), self.user1)

    def test_community_view(self):
        """Test the community view"""
        self.client.login(username='user1', password='Testuser1')
        community = Community.objects.create(
            name='Test community', creator=self.user1)
        response = self.client.get(self.community_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'communities/community.html')
        self.assertEqual(response.context['user'], self.user1)
        self.assertEqual(response.context['community'], community)
        self.assertEqual(response.context['posts'].count(), 0)
        self.assertTrue(response.context['post_form'])
        self.assertTrue(response.context['comment_form'])

    def test_join_community_view(self):
        """Test the join community view"""
        self.client.login(username='user1', password='Testuser1')
        community = Community.objects.create(
            name='Test community', creator=self.user2)
        response = self.client.post(
            self.join_community_url,
            {'community_id': community.id},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'), {'success': True})
        self.assertEqual(community.members.count(), 1)
        self.assertEqual(community.members.first(), self.user1)

    def leave_community_view(self):
        """Test the leave community view"""
        self.client.login(username='user1', password='Testuser1')
        community = Community.objects.create(
            name='Test community', creator=self.user2)
        community.members.add(self.user2)
        community.members.add(self.user1)
        self.assertEqual(community.members.count(), 2)
        response = self.client.post(
            self.leave_community_url,
            {'community_id': community.id},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'), {'success': True})
        self.assertEqual(community.members.count(), 1)

    def test_edit_community_view(self):
        """Test the edit community view"""
        self.client.login(username='user1', password='Testuser1')
        community = Community.objects.create(
            name='Test community', creator=self.user1)
        community.members.add(self.user1)
        response = self.client.get(self.edit_community_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'communities/create_community.html')
        self.assertEqual(response.context['user'], self.user1)
        self.assertEqual(response.context['community'], community)
        self.assertEqual(
            response.context['form']['name'].value(), 'Test community')
        self.assertEqual(response.context['form']['description'].value(), '')
        self.assertEqual(response.context['form']['bg_image'].value(), None)
        self.assertEqual(response.context['form']['logo'].value(), None)

        response = self.client.post(self.edit_community_url, {
            'name': 'Test community',
            'description': 'Test description',
            'bg_image': open('static/images/default-bg.jpg', 'rb'),
            'logo': open('static/images/default-logo.png', 'rb')
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.community_url)
        self.assertEqual(Community.objects.count(), 1)
        self.assertEqual(Community.objects.first().name, 'Test community')
        self.assertEqual(Community.objects.first().description,
                         'Test description')
        self.assertTrue(
            'res.cloudinary.com' in Community.objects.first().bg_image.url)
        self.assertTrue(
            'res.cloudinary.com' in Community.objects.first().logo.url)
        self.assertEqual(Community.objects.first().creator, self.user1)
        self.assertEqual(Community.objects.first().members.count(), 1)
        self.assertEqual(Community.objects.first().members.first(), self.user1)

    def test_delete_community_view(self):
        """Test the delete community view"""
        self.client.login(username='user1', password='Testuser1')
        community = Community.objects.create(
            name='Test community', creator=self.user1)
        community.members.add(self.user1)
        response = self.client.get(self.edit_community_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'communities/create_community.html')
        response = self.client.post(self.delete_community_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.users_communities_url)
        self.assertEqual(Community.objects.count(), 0)
        community = Community.objects.create(
            name='Test community', creator=self.user2)
        community.members.add(self.user1)
        response = self.client.get(self.edit_community_url)
        self.assertEqual(response.status_code, 302)  # user is not the creator
        self.assertRedirects(response, self.community_url)
        response = self.client.post(self.delete_community_url)
        self.assertEqual(response.status_code, 302)  # user is not the creator
        self.assertRedirects(response, self.community_url)
        self.assertEqual(Community.objects.count(), 1)
