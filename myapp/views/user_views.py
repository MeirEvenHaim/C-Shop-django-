from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from myapp.serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from myapp.models import Cart
@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    
    if serializer.is_valid():
        # Extract validated data
        validated_data = serializer.validated_data
        
        # Create a new user instance
        user = User(
            username=validated_data['username'],
        )
        
        # Set the password
        user.set_password(validated_data['password'])
        
        # Save the user
        user.save()
        
        return Response({'id': user.id, 'username': user.username}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is not None and user.is_active:
        refresh = RefreshToken.for_user(user)

        # Ensure the user has a cart
        Cart.objects.get_or_create(user=user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

    return Response({'error': 'Invalid credentials or inactive account'}, status=status.HTTP_401_UNAUTHORIZED)

# Retrieve all users (Admin-only access)
@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def list_all_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

# Retrieve the logged-in user's profile
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_profile(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated]) # type: ignore
def update_user_profile(request, id=None):
    # If an id is provided, check if the user is an admin
    if id:
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        user = get_object_or_404(User, id=id)
    else:
        # Update the current user's profile
        user = request.user

    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_user(request, id):
    user = get_object_or_404(User, id=id)
    user.delete()
    return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)