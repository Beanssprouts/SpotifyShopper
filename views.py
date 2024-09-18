import requests
from django.conf import settings
from django.shortcuts import redirect
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from datetime import timedelta
from django.contrib.auth import login
from django.utils import timezone
from playlists.models import Cart
from .models import User
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

def spotify_login(request):
    scope = 'user-read-private user-read-email playlist-modify-public playlist-modify-private'
    auth_url = (
        f'https://accounts.spotify.com/authorize'
        f'?response_type=code'
        f'&client_id={settings.SPOTIFY_CLIENT_ID}'
        f'&redirect_uri={settings.SPOTIFY_REDIRECT_URI}'
        f'&scope={scope}'
    )
    return redirect(auth_url)

def spotify_callback(request):
    code = request.GET.get('code')
    token_url = 'https://accounts.spotify.com/api/token'
    response = requests.post(token_url, data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': settings.SPOTIFY_REDIRECT_URI,
        'client_id': settings.SPOTIFY_CLIENT_ID,
        'client_secret': settings.SPOTIFY_CLIENT_SECRET,
    })
    data = response.json()
    access_token = data.get('access_token')
    refresh_token = data.get('refresh_token')
    token_expiry = data.get('expires_in')

    profile_url = 'https://api.spotify.com/v1/me'
    headers = {'Authorization': f'Bearer {access_token}'}
    profile_response = requests.get(profile_url, headers=headers)
    profile_data = profile_response.json()

    user, created = User.objects.get_or_create(username=profile_data['id'])
    user.email = profile_data['email']
    user.spotify_token = access_token
    user.refresh_token = refresh_token
    user.token_expiry = timezone.now() + timedelta(seconds=token_expiry)
    user.save()

    Cart.objects.get_or_create(user=user)

    login(request, user)

    return JsonResponse({'status': 'success', 'access_token': access_token})

def refresh_token(user):
    token_url = 'https://accounts.spotify.com/api/token'
    response = requests.post(token_url, data={
        'grant_type': 'refresh_token',
        'refresh_token': user.refresh_token,
        'client_id': settings.SPOTIFY_CLIENT_ID,
        'client_secret': settings.SPOTIFY_CLIENT_SECRET,
    })
    data = response.json()
    access_token = data.get('access_token')
    token_expiry = data.get('expires_in')

    user.spotify_token = access_token
    user.token_expiry = timezone.now() + timedelta(seconds=token_expiry)
    user.save()
    return access_token

def get_user_data(request):
    user = request.user
    if user.token_expiry <= timezone.now():
        access_token = refresh_token(user)
    else:
        access_token = user.spotify_token

    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get('https://api.spotify.com/v1/me', headers=headers)
    return JsonResponse(response.json())
