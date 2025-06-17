from rest_framework import serializers
from ..models import Ventas, DetallesVentas
from .proveedoresSerializer import ProveedoresSerializer
from .detallesVentasSerializer import DetallesVentasSerializer

class VentasSerializer(serializers.ModelSerializer):

    detallesVentas = DetallesVentasSerializer(many=True)

    class Meta:
        model = Ventas
        fields = ["id","fecha","total", "detallesVentas"]
        # fields = ["id", "idproveedor", "proveedor", "subtotal", "fecha", "detallesCompra"]


    # def validate(self, data):
    #     idproveedor = data.get('idproveedor')
    #     subtotal = data.get('subtotal')
    #     fecha = data.get('fecha')

    #     instance_id = self.instance.id if self.instance else None

    #     if Ventas.objects.filter(
    #         idproveedor=idproveedor, subtotal=subtotal, fecha=fecha
    #     ).exclude(id=instance_id).exists():
    #         raise serializers.ValidationError("Ya existe una compra con esos campos")

    #     return data

    def create(self, validated_data):
        detalles_data = validated_data.pop('detallesVentas')

        total = 0

        for detalle in detalles_data:
            producto = detalle['idproducto']
            cantidad = detalle['cantidad']
            total += producto.precio * cantidad

        ventas = Ventas.objects.create(**validated_data)

        for detalle in detalles_data:
            DetallesVentas.objects.create(idventa=ventas, **detalle)

        return ventas
