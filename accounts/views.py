from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

class UserViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def register(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')

        # Perform validation
        if not username or not password or not email or not first_name or not last_name:
            return Response({'message': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            return Response({'message': 'Username is already taken'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the user
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Perform validation
        if not username or not password:
            return Response({'message': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate the user
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'message': 'User logged in successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['get'])
    def logout(self, request):
        logout(request)
        return Response({'message': 'User logged out successfully'}, status=status.HTTP_200_OK)
