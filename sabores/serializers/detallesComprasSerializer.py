from rest_framework import serializers
from ..models import DetallesCompras,Productos, Compras
# from .comprasSerializer import ComprasSerializer
from .serializer import ProductosSerializer

        
class DetallesComprasSerializer(serializers.ModelSerializer):

    # idcompras = serializers.PrimaryKeyRelatedField(
    #     queryset=Compras.objects.all(), 
    #     write_only=True) 
    # compras = ComprasSerializer(source='idcompras', read_only=True)

    idproducto = serializers.PrimaryKeyRelatedField(
        queryset=Productos.objects.all(), write_only=True) 
    producto = ProductosSerializer(source='idproducto', read_only=True)

    class Meta:
        model = DetallesCompras
        fields = ["id", "idproducto", "producto", "cantidad"]#"idcompras", "compras",

    