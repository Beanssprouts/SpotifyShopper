from django.test import TestCase, Client
from django.urls import reverse
from .models import User
from unittest.mock import patch
from datetime import timedelta
import responses
from django.utils import timezone

class AccountsTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.user.spotify_token = 'initial_token'
        self.user.refresh_token = 'initial_refresh_token'
        self.user.token_expiry = timezone.now() - timedelta(days=1)
        self.user.save()

    def test_user_creation(self):
        # Test that the user was created successfully
        self.assertEqual(User.objects.count(), 1)

    @patch('accounts.views.refresh_token')
    @responses.activate
    def test_get_user_data(self, mock_refresh_token):
        # Mock the refresh_token function to return a new token
        mock_refresh_token.return_value = 'new_token'
        # Mock the Spotify API response for user profile
        responses.add(responses.GET, 'https://api.spotify.com/v1/me', json={
            'id': 'testuser',
            'display_name': 'Test User',
            'email': 'testuser@example.com'
        })
        # Log in the test user
        self.client.login(username='testuser', password='password123')
        # Call the get_user_data view
        response = self.client.get(reverse('get_user_data'))
        # Verify the response
        self.assertEqual(response.status_code, 200)
        self.assertIn('testuser', response.content.decode())

    @responses.activate
    def test_spotify_callback(self):
        # Mock the Spotify API response for token exchange
        responses.add(responses.POST, 'https://accounts.spotify.com/api/token', json={
            'access_token': 'new_access_token',
            'refresh_token': 'new_refresh_token',
            'expires_in': 3600
        })
        # Mock the Spotify API response for user profile
        responses.add(responses.GET, 'https://api.spotify.com/v1/me', json={
            'id': 'testuser',
            'email': 'testuser@example.com'
        })
        # Call the spotify_callback view with a test code
        response = self.client.get(reverse('spotify_callback'), {'code': 'test_code'})
        # Verify the response and user data
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(username='testuser')
        self.assertEqual(user.spotify_token, 'new_access_token')
        self.assertEqual(user.refresh_token, 'new_refresh_token')
