from datetime import date
from rest_framework import serializers
from ..models import Compras, Proveedores, DetallesCompras
from .proveedoresSerializer import ProveedoresSerializer
from .detallesComprasSerializer import DetallesComprasSerializer
from .productosSerializer import ProductosSerializer


class ComprasSerializer(serializers.ModelSerializer):
    # idproveedor = serializers.PrimaryKeyRelatedField(
    #     queryset=Proveedores.objects.all(), 
    #     write_only=True
    # ) 
    # proveedor = ProveedoresSerializer(source='idproveedor', read_only=True)
    detallesCompra = DetallesComprasSerializer(many=True)

    class Meta:
        model = Compras
        fields = ["id", "subtotal", "fecha", "detallesCompra"]


    def create(self, validated_data):
        try:
            detalles_data = validated_data.pop('detallesCompra')
                
            for detalle in detalles_data:
                producto = detalle['idproducto']
                cantidad = detalle['cantidad']

            compra = Compras.objects.create(**validated_data)

            for detalle in detalles_data:

                DetallesCompras.objects.create(idcompra=compra, **detalle)
                
                producto = detalle['idproducto']
                cantidad = detalle['cantidad']
                ProductosSerializer.aumentar_cantidad_inventario(producto.id, cantidad)
                ProductosSerializer.aumentar_cantidad_inicial_inventario(producto.id, cantidad)

            return compra
        except Exception as e:
            return {"Error": e};
