from rest_framework import viewsets, permissions
from myapp.models import Shop
from myapp.serializers import ShopSerializer

class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer

    def get_permissions(self):
        if self.action == 'destroy':
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]