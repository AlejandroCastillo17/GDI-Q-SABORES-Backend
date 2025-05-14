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
    serializer_class = DetallesCompras 

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre', 'estado', "email"]

    @action(detail=True, methods=['post'])
    @transaction.atomic
    def crear_compra(request):
        data = request.data
        try:
            compra = Compras.objects.create(
                fecha=data['fecha'],
                subtotal=data['subtotal'],
                idproveedor_id=detalle['idproveedor'],
            )
            detalles = data.get('detalles', [])
            for detalle in detalles:
                DetallesCompras.objects.create(
                    idproducto_id=detalle['idproducto'],
                    idcompra=compra,
                    cantidad=detalle['cantidad']
                )

            return Response({
                'mensaje': 'Compra y detalles creados correctamente',
                'id_compra': compra.id
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)







    # async def crear_compra(request):

    #     comprasSerializer = ComprasSerializer(data=request.data)
        
    #     if comprasSerializer.is_valid():
    #         created_compras = await comprasSerializer.create()
    #         await crear_detalle_compra()
    #         return Response({"compra": comprasSerializer.data}, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(comprasSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    # async def crear_detalle_compra(request):
    #     detalleCompraSerializer = DetallesComprasSerializer(data={request.data})
        
    #     if detalleCompraSerializer.is_valid():
    #         detalleCompraSerializer.create()
    #         return {"compra": detalleCompraSerializer.data} 
    #     else:
    #         return (detalleCompraSerializer.errors)