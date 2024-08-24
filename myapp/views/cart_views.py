from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, permissions
from rest_framework.response import Response 
from rest_framework.decorators import api_view
from myapp.models import Cart
from myapp.serializers import CartSerializer
from rest_framework.permissions import IsAuthenticated



@api_view(['POST'])
def create_cart(request):
    serializer = CartSerializer(data=request.data)
    if serializer.is_valid():
        # Save the Cart instance first
        cart = serializer.save(user=request.user)
        # Handle ManyToManyField separately
        parts = request.data.get('parts', [])
        if parts:
            cart.parts.set(parts)
        cart.save()  # Save again to ensure the parts are set
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Save the Cart instance first
        cart = serializer.save(user=self.request.user)
        # Handle ManyToManyField separately
        parts = request.data.get('parts', [])
        if parts:
            cart.parts.set(parts)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        # Save the updated Cart instance
        self.perform_update(serializer)
        # Handle ManyToManyField separately
        parts = request.data.get('parts', [])
        if parts:
            instance.parts.set(parts)
        return Response(serializer.data)