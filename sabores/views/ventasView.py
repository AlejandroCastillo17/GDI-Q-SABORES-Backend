from rest_framework import viewsets, filters
from ..models import Ventas
from ..serializers.ventasSerializer import VentasSerializer;
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

class VentasView(viewsets.ModelViewSet):
    queryset = Ventas.objects.all()
    serializer_class = VentasSerializer 

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    filter_backends = [filters.SearchFilter]
    search_fields = ['fecha', 'producto']

