from rest_framework import serializers
from ..models import Compras, Proveedores, DetallesCompras
from .proveedoresSerializer import ProveedoresSerializer
from .detallesComprasSerializer import DetallesComprasSerializer

class ComprasSerializer(serializers.ModelSerializer):
    idproveedor = serializers.PrimaryKeyRelatedField(
        queryset=Proveedores.objects.all(), 
        write_only=True
    ) 
    proveedor = ProveedoresSerializer(source='idproveedor', read_only=True)
    detallesCompra = DetallesComprasSerializer(many=True)

    class Meta:
        model = Compras
        fields = ["id", "idproveedor", "proveedor", "subtotal", "fecha", "detallesCompra"]


    def validate(self, data):
        idproveedor = data.get('idproveedor')
        subtotal = data.get('subtotal')
        fecha = data.get('fecha')

        instance_id = self.instance.id if self.instance else None

        if Compras.objects.filter(
            idproveedor=idproveedor, subtotal=subtotal, fecha=fecha
        ).exclude(id=instance_id).exists():
            raise serializers.ValidationError("Ya existe una compra con esos campos")

        return data

    def create(self, validated_data):
        detalles_data = validated_data.pop('detallesCompra')  # quitar antes de crear Compra

        subtotal = 0

        for detalle in detalles_data:
            producto = detalle['idproducto']
            cantidad = detalle['cantidad']
            subtotal += producto.precio * cantidad  # calcula subtotal

        compra = Compras.objects.create(**validated_data)

        for detalle in detalles_data:
            DetallesCompras.objects.create(idcompra=compra, **detalle)

        return compra
