from rest_framework import viewsets, permissions
from myapp.models import Game
from myapp.serializers import GameSerializer

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def get_permissions(self):
        if self.action == 'destroy':
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]