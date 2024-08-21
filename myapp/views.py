from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Computer, Part, Game, Cart, Shop
from .serializers import ComputerSerializer, PartSerializer, GameSerializer, CartSerializer, ShopSerializer, UserSerializer

class ComputerViewSet(viewsets.ModelViewSet): #creates the crude for the computer table
    queryset = Computer.objects.all()
    serializer_class = ComputerSerializer

    def get_permissions(self):#provides the premission to delete the data from the computer tables for admins only (privet method)
        if self.action in ['destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

class PartViewSet(viewsets.ModelViewSet):#creates the crude for the parts table
    queryset = Part.objects.all()
    serializer_class = PartSerializer

    def get_permissions(self):
        if self.action in ['destroy']:#provides the premission to delete the data from the parts tables for admins only (privet method)
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

class GameViewSet(viewsets.ModelViewSet):#creates the crude for the GAMES table
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def get_permissions(self):
        if self.action in ['destroy']:#provides the premission to delete the data from the games tables for admins only (privet method)
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

class CartViewSet(viewsets.ModelViewSet):#creates the crude for the Cart table
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_permissions(self):
        if self.action in ['destroy']:#provides the premission to delete the data from the cart tables for admins only (privet method)
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]

    def perform_destroy(self, instance):
        if instance.user != self.request.user and not self.request.user.is_staff:
            self.permission_denied(self.request)
        super().perform_destroy(instance)

class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer

    def get_permissions(self):
        if self.action in ['destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({'id': user.id, 'username': user.username}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_user(request):
    from rest_framework_simplejwt.tokens import RefreshToken
    from django.contrib.auth import authenticate

    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
