from rest_framework import serializers
from .models import Cart, CartItem, Playlist

# converts models to strings i think
class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'song_id', 'song_name', 'artist_name']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Cart
        fields = ['id', 'user', 'items']

class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ['id', 'user', 'playlist_id', 'playlist_name', 'created_at']
