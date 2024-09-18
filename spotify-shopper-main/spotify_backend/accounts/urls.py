from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('login/', views.spotify_login, name='spotify_login'),
    path('callback/', views.spotify_callback, name='spotify_callback'),
    path('me/', views.get_user_data, name='get_user_data'),
]

urlpatterns += router.urls