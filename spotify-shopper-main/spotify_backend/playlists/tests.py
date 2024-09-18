from django.test import TestCase, Client
from accounts.models import User
from .models import Cart, CartItem, Playlist
from datetime import timedelta
from django.utils import timezone
import responses
from unittest.mock import patch

class PlaylistsTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.user.spotify_token = 'initial_token'
        self.user.refresh_token = 'initial_refresh_token'
        self.user.token_expiry = timezone.now() + timedelta(days=1)
        self.user.save()
        self.client.login(username='testuser', password='password123')
        self.cart = Cart.objects.create(user=self.user)

    def test_add_cart_item(self):
        url = '/api/playlists/cart-items/'  # Ensure this URL is correct
        response = self.client.post(url, {
            'song_id': '6rqhFgbbKwnb9MLmUQDhG6',  # Example Spotify song ID
            'song_name': 'Example Song',
            'artist_name': 'Example Artist'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(CartItem.objects.count(), 1)

    def test_view_cart(self):
        CartItem.objects.create(cart=self.cart, song_id='6rqhFgbbKwnb9MLmUQDhG6', song_name='Example Song', artist_name='Example Artist')
        response = self.client.get(f'/api/playlists/carts/{self.cart.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Example Song', response.content.decode())

    @responses.activate
    def test_search_songs(self):
        responses.add(responses.GET, 'https://api.spotify.com/v1/search', json={
            'tracks': {'items': [{'id': '6rqhFgbbKwnb9MLmUQDhG6', 'name': 'Example Song', 'artists': [{'name': 'Example Artist'}]}]}
        }, status=200)
        response = self.client.get('/api/playlists/search/', {'query': 'Example'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Example Song', response.content.decode())


    ## This test fails, but i don't really know why. The actual thing works at this point 7/23/2024
    @responses.activate
    @patch('requests.post')
    def test_create_playlist(self, mock_post):
        # Add an item to the cart
        CartItem.objects.create(cart=self.cart, song_id='6rqhFgbbKwnb9MLmUQDhG6', song_name='Example Song', artist_name='Example Artist')
        # Mock the Spotify API responses for creating a playlist and adding tracks to it
        responses.add(responses.GET, 'https://api.spotify.com/v1/me', json={'id': 'testuser'}, status=200)
        responses.add(responses.POST, 'https://api.spotify.com/v1/users/testuser/playlists', json={'id': 'playlist123'}, status=201)
        responses.add(responses.POST, 'https://api.spotify.com/v1/playlists/playlist123/tracks', json={'snapshot_id': 'snapshot123'}, status=201)
        # Call the create_playlist view
        response = self.client.post('/api/playlists/create-playlist/', {'name': 'My Playlist'}, content_type='application/json')
        print(f"Response Status Code: {response.status_code}")  # Debugging line to print the status code
        print(f"Response Content: {response.content.decode()}")  # Debugging line to print the response content
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Playlist.objects.count(), 1)
        self.assertEqual(CartItem.objects.count(), 0)  # Ensure cart is cleared
