from rest_framework import viewsets, filters
from ..models import Compras, DetallesCompras
from ..serializers.comprasSerializer import ComprasSerializer
from ..serializers.detallesComprasSerializer import DetallesComprasSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction


class ComprasView(viewsets.ModelViewSet):
    queryset = Compras.objects.all()
    serializer_class = ComprasSerializer 

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre', 'estado', "email"]

