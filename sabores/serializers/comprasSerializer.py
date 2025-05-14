from rest_framework import serializers
from ..models import Compras, Proveedores
from .proveedoresSerializer import ProveedoresSerializer
   
class ComprasSerializer(serializers.ModelSerializer):

    idproveedor = serializers.PrimaryKeyRelatedField(
        queryset=Proveedores.objects.all(), 
        write_only=True) 
    proveedor = ProveedoresSerializer(source='idproveedor', read_only=True)

    class Meta:
        model = Compras
        fields = ["id","idproveedor", "proveedor", "subtotal", "fecha"]

    def validate(self, data):
        idproveedor = data.get('idproveedor')
        subtotal = data.get('subtotal')
        fecha = data.get('fecha')
        
        instance_id = self.instance.id if self.instance else None

        if Compras.objects.filter(
            idproveedor=idproveedor, subtotal=subtotal, fecha=fecha
        ).exclude(id=instance_id).exists():
            raise serializers.ValidationError("Ya existe un proveedor con ese nombre, email y telefono.")
                
        return data
    