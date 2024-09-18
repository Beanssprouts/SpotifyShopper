# import dependencies
import requests
from rest_framework import viewsets
from accounts.views import refresh_token
from .models import Cart, CartItem, Playlist
from .serializers import CartSerializer, CartItemSerializer, PlaylistSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.utils import timezone
from datetime import datetime

# For searching Spotify's API
from rest_framework.decorators import api_view
from rest_framework.response import Response

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)
        # Create a mutable copy of the request data
        data = request.data.copy()
        data['cart'] = cart.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    permission_classes = [IsAuthenticated]



# This might not work... fetch songs from Spotify Search API. NOTE: refresh_token import is broken...
@api_view(['GET'])
def search_songs(request):
    query = request.query_params.get('query')
    user = request.user

    if user.token_expiry <= timezone.now():
        access_token = refresh_token(user)
    else:
        access_token = user.spotify_token

    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(f'https://api.spotify.com/v1/search?q={query}&type=track', headers=headers)
    return Response(response.json())

# This piece of code adds the playlist to the user's account - review it again at some point
@api_view(['POST'])
def create_playlist(request):
    user = request.user
    cart = Cart.objects.get(user=user)

    track_uris = [f'spotify:track:{item.song_id}' for item in cart.items.all()]

    if len(track_uris) == 0:
        return Response({'status': 'error', 'message': 'Your cart is empty!'}, status=400)

    if user.token_expiry <= timezone.now():
        access_token = refresh_token(user)
    else:
        access_token = user.spotify_token

    headers = {'Authorization': f'Bearer {access_token}'}
    playlist_name = request.data.get('name', 'My Playlist')
    create_playlist_response = requests.post('https://api.spotify.com/v1/users/{}/playlists'.format(user.username), json={
        'name': playlist_name,
        'description':'Created with Spotify Shopper',
    }, headers=headers)
    
    if create_playlist_response.status_code != 201: # Figure out a potential way to print this out...
        return Response({'status': 'error', 'message': 'Failed to create playlist'}, status=400)

    playlist_data = create_playlist_response.json()
    playlist_id = playlist_data['id']



    add_tracks_response = requests.post(f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks', json={
        'uris': track_uris
    }, headers=headers)


    if add_tracks_response.status_code == 201:
        cart.items.all().delete()  # Clear the cart
        return Response({'status': 'success', 'playlist_id': playlist_id})
    else:
        return Response({'status': 'error', 'message': 'Failed to add tracks to the playlist'}, status=400)