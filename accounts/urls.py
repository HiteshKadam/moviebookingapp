from django.urls import path
from rest_framework import routers
from .views import UserViewSet,AdminViewSet


router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='users')


urlpatterns = [
    path('register/', UserViewSet.as_view({'post': 'register'}), name='register'),
    path('login/', UserViewSet.as_view({'post': 'login'}), name='login'),
    path('logout/', UserViewSet.as_view({'get': 'logout'}), name='logout'),
    path('check_admin_status/', AdminViewSet.as_view({'get': 'check_admin_status'}), name='check_admin_status'),
]
