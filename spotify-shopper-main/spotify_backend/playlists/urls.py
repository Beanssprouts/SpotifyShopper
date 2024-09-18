from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CartViewSet, CartItemViewSet, PlaylistViewSet, search_songs, create_playlist
# URL API
router = DefaultRouter()
router.register(r'carts', CartViewSet)
router.register(r'cart-items', CartItemViewSet)
router.register(r'playlists', PlaylistViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('search/', search_songs, name='search_songs'),
    path('create-playlist/', create_playlist, name='create_playlist'),
]
