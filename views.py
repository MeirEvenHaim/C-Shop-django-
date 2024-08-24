# from django.shortcuts import get_object_or_404
# from rest_framework import status, viewsets, permissions 
# from rest_framework.response import Response
# from rest_framework.decorators import api_view , permission_classes 
# from rest_framework_simplejwt.tokens import RefreshToken
# from .models import Computer, Part, Game, Cart, Shop
# from rest_framework.permissions import IsAuthenticated, IsAdminUser
# from .serializers import ComputerSerializer, PartSerializer, GameSerializer, CartSerializer, ShopSerializer, UserSerializer
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.contrib.auth import authenticate 
# from django.contrib.auth.models import User

# class ComputerViewSet(viewsets.ModelViewSet):
#     queryset = Computer.objects.all()
#     serializer_class = ComputerSerializer

#     def get_permissions(self):
#         """
#         Return the permission classes based on the action being performed.
#         """
#         if self.action == 'destroy':
#             # Only admins can delete computers
#             return [permissions.IsAdminUser()]
#         # For other actions, authenticated users can access
#         return [permissions.IsAuthenticated()]

#     def perform_create(self, serializer):
#         """
#         Save the user who is creating the computer if authenticated.
#         """
#         if self.request.user.is_authenticated:
#             serializer.save(user=self.request.user)
#         else:
#             serializer.save(user=None)

# class PartViewSet(viewsets.ModelViewSet):#creates the crude for the parts table
#     queryset = Part.objects.all()
#     serializer_class = PartSerializer

#     def get_permissions(self):
#         if self.action in ['destroy']:#provides the premission to delete the data from the parts tables for admins only (privet method)
#             return [permissions.IsAdminUser()]
#         return [permissions.IsAuthenticated()]

# class GameViewSet(viewsets.ModelViewSet):#creates the crude for the GAMES table
#     queryset = Game.objects.all()
#     serializer_class = GameSerializer

#     def get_permissions(self):
#         if self.action in ['destroy']:#provides the premission to delete the data from the games tables for admins only (privet method)
#             return [permissions.IsAdminUser()]
#         return [permissions.IsAuthenticated()]


# @api_view(['POST'])
# def create_cart(request):
#     """
#     Create a new Cart instance.
#     """
#     serializer = CartSerializer(data=request.data)
#     if serializer.is_valid():
#         # Save the Cart instance to get an ID
#         cart = serializer.save()

#         # Handle many-to-many relationships
#         parts_ids = request.data.get('parts', [])
#         if parts_ids:
#             # Fetch parts by IDs and add them to the cart
#             parts = Part.objects.filter(id__in=parts_ids)
#             cart.parts.set(parts)
#             cart.save()  # Ensure the changes are saved

#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET'])
# def list_carts(request):
#     """
#     List all Cart instances.
#     """
#     carts = Cart.objects.all()
#     serializer = CartSerializer(carts, many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def retrieve_cart(request, pk):
#     """
#     Retrieve a single Cart instance by ID.
#     """
#     try:
#         cart = Cart.objects.get(pk=pk)
#     except Cart.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
    
#     serializer = CartSerializer(cart)
#     return Response(serializer.data)

# @api_view(['PUT'])
# def update_cart(request, pk):
#     """
#     Update a Cart instance by ID.
#     """
#     try:
#         cart = Cart.objects.get(pk=pk)
#     except Cart.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     serializer = CartSerializer(cart, data=request.data)
#     if serializer.is_valid():
#         # Save the cart instance
#         cart = serializer.save()

#         # Handle many-to-many relationships
#         parts_ids = request.data.get('parts', [])
#         if parts_ids:
#             # Fetch parts by IDs and add them to the cart
#             parts = Part.objects.filter(id__in=parts_ids)
#             cart.parts.set(parts)
#             cart.save()  # Ensure the changes are saved

#         return Response(serializer.data)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['PATCH'])
# def partial_update_cart(request, pk):
#     """
#     Partially update a Cart instance by ID.
#     """
#     try:
#         cart = Cart.objects.get(pk=pk)
#     except Cart.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     serializer = CartSerializer(cart, data=request.data, partial=True)
#     if serializer.is_valid():
#         # Save the cart instance
#         cart = serializer.save()

#         # Handle many-to-many relationships
#         parts_ids = request.data.get('parts', [])
#         if parts_ids:
#             # Fetch parts by IDs and add them to the cart
#             parts = Part.objects.filter(id__in=parts_ids)
#             cart.parts.set(parts)
#             cart.save()  # Ensure the changes are saved

#         return Response(serializer.data)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['DELETE'])
# def delete_cart(request, pk):
#     """
#     Delete a Cart instance by ID.
#     """
#     try:
#         cart = Cart.objects.get(pk=pk)
#     except Cart.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     cart.delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)


# class ShopViewSet(viewsets.ModelViewSet):
#     queryset = Shop.objects.all()
#     serializer_class = ShopSerializer

#     def get_permissions(self):
#         if self.action in ['destroy']:
#             return [permissions.IsAdminUser()]
#         return [permissions.IsAuthenticated()]

# @api_view(['POST'])
# def register_user(request):
#     serializer = UserSerializer(data=request.data)
    
#     if serializer.is_valid():
#         # Extract validated data
#         validated_data = serializer.validated_data
        
#         # Create a new user instance
#         user = User(
#             username=validated_data['username'],
#         )
        
#         # Set the password
#         user.set_password(validated_data['password'])
        
#         # Save the user
#         user.save()
        
#         return Response({'id': user.id, 'username': user.username}, status=status.HTTP_201_CREATED)
    
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# def login_user(request):
#     username = request.data.get('username')
#     password = request.data.get('password')
    
#     user = authenticate(username=username, password=password)
    
#     if user is not None and user.is_active:
#         refresh = RefreshToken.for_user(user)
#         return Response({
#             'refresh': str(refresh),
#             'access': str(refresh.access_token),
#         })
    
#     return Response({'error': 'Invalid credentials or inactive account'}, status=status.HTTP_401_UNAUTHORIZED)

# # Retrieve all users (Admin-only access)
# @api_view(['GET'])
# @permission_classes([permissions.IsAdminUser])
# def list_all_users(request):
#     users = User.objects.all()
#     serializer = UserSerializer(users, many=True)
#     return Response(serializer.data)

# # Retrieve the logged-in user's profile
# @api_view(['GET'])
# @permission_classes([permissions.IsAuthenticated])
# def user_profile(request):
#     user = request.user
#     serializer = UserSerializer(user)
#     return Response(serializer.data)

# @api_view(['PUT', 'PATCH'])
# @permission_classes([IsAuthenticated])
# def update_user_profile(request, id=None):
#     # If an id is provided, check if the user is an admin
#     if id:
#         if not request.user.is_staff:
#             return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
#         user = get_object_or_404(User, id=id)
#     else:
#         # Update the current user's profile
#         user = request.user

#     serializer = UserSerializer(user, data=request.data, partial=True)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['DELETE'])
# @permission_classes([IsAdminUser])
# def delete_user(request, id):
#     user = get_object_or_404(User, id=id)
#     user.delete()
#     return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)