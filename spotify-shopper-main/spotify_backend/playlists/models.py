# import dependencies
from django.db import models
from accounts.models import User # carts and playlists are associated with one user

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Associates cart to user

class CartItem(models.Model): # A cart item is the equivalent of a song. It is mapped to a cart?
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    song_id = models.CharField(max_length=50)
    song_name = models.CharField(max_length=255)
    artist_name = models.CharField(max_length=255)


# I believe this tracks user's past playlists created...
class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    playlist_id = models.CharField(max_length=50)
    playlist_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
