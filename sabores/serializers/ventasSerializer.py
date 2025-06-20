from rest_framework import serializers
from ..models import Ventas, DetallesVentas, Productos
from .productosSerializer import ProductosSerializer
from .detallesVentasSerializer import DetallesVentasSerializer

class VentasSerializer(serializers.ModelSerializer):

    detallesVentas = DetallesVentasSerializer(many=True)

    class Meta:
        model = Ventas
        fields = ["id", "fecha", "total", "detallesVentas"]


    def create(self, validated_data):
        detalles_data = validated_data.pop('detallesVentas')

        total = 0

        for detalle in detalles_data:
            producto = detalle["idproducto"]
            cantidad = detalle['cantidad']

            total = total + (producto.precio * cantidad)

        ventas = Ventas.objects.create(**validated_data, total=total)

        for detalle in detalles_data:
            DetallesVentas.objects.create(idventa=ventas, **detalle)
            producto = detalle['idproducto']
            cantidad = detalle['cantidad']

            ProductosSerializer.reducir_cantidad_inventario(producto.id, cantidad)


        return ventas
