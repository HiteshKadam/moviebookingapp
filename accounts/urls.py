from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='users')


urlpatterns = [
    path('register/', UserViewSet.as_view({'post': 'register'}), name='register'),
    path('login/', UserViewSet.as_view({'post': 'login'}), name='login'),
    path('logout/', UserViewSet.as_view({'get': 'logout'}), name='logout'),
]
