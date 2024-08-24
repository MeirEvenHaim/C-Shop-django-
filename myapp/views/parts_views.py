from rest_framework import viewsets, permissions
from myapp.models import Part
from myapp.serializers import PartSerializer

class PartViewSet(viewsets.ModelViewSet):#creates the crude for the parts table
    queryset = Part.objects.all()
    serializer_class = PartSerializer

    def get_permissions(self):
        if self.action in ['destroy']:#provides the premission to delete the data from the parts tables for admins only (privet method)
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]
