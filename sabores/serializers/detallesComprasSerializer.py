from rest_framework import serializers
from ..models import DetallesCompras,Productos, Compras
# from .comprasSerializer import ComprasSerializer
from .productosSerializer import ProductosSerializer

        
class DetallesComprasSerializer(serializers.ModelSerializer):

    idproducto = serializers.PrimaryKeyRelatedField(
        queryset=Productos.objects.all(), write_only=True) 
    producto = ProductosSerializer(source='idproducto', read_only=True)

    class Meta:
        model = DetallesCompras
        fields = ["id", "idproducto", "producto", "cantidad"]


    