from rest_framework import serializers
from ..models import Compras, Proveedores
from .proveedoresSerializer import ProveedoresSerializer
from .detallesComprasSerializer import DetallesComprasSerializer
   
class ComprasSerializer(serializers.ModelSerializer):

    idproveedor = serializers.PrimaryKeyRelatedField(
        queryset=Proveedores.objects.all(), 
        write_only=True) 
    proveedor = ProveedoresSerializer(source='idproveedor', read_only=True)

    # idDetallesCompras = serializers.PrimaryKeyRelatedField(
    # queryset=DetallesCompras.objects.all(), 
    # write_only=True) 
    detallesCompras = DetallesComprasSerializer(many = True, read_only=True) 

    class Meta:
        model = Compras
        fields = ["id","idproveedor", "proveedor", "subtotal", "fecha", "detallesCompras" ]

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
    