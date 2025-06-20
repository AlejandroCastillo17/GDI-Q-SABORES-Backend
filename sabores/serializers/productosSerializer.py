from rest_framework import serializers
from ..models import Usuario, Proveedores, Categorias
from ..models import Productos
from django.contrib.auth.models import User
from .proveedoresSerializer import ProveedoresSerializer

        
class ProductosSerializer(serializers.ModelSerializer):
    proveedorid = serializers.PrimaryKeyRelatedField(
        queryset=Proveedores.objects.all()) 
    proveedor = ProveedoresSerializer(source='proveedorid', read_only=True)

    categoriaid = serializers.PrimaryKeyRelatedField(
    queryset=Categorias.objects.all(), 
    write_only=True)
    categoria = ProveedoresSerializer(source='categoriaid', read_only=True)

    class Meta:
        model = Productos
        fields = [
            'id',
            'nombre',
            'precio',
            'cantidad_actual',
            'cantidad_inicial',
            'foto',
            'topeMin',
            'categoriaid',
            'categoria',
            'proveedorid',
            'proveedor']
        

    def validate(self, data):
        nombre = data.get('nombre')
        categoriaid = data.get('categoriaid')
        proveedorid = data.get('proveedorid')

        # Al actualizar, excluirse a sí mismo de la validación
        instance_id = self.instance.id if self.instance else None

        if Productos.objects.filter(
            nombre=nombre, categoriaid=categoriaid, proveedorid=proveedorid
        ).exclude(id=instance_id).exists():
            raise serializers.ValidationError("Ya existe un producto con ese nombre, categoría y proveedor.")
        
        return data
    

    def reducir_cantidad_inventario(idproducto, cantidad_reducir):
        producto = Productos.objects.get(id=idproducto)

        if producto:
            producto.cantidad_actual = producto.cantidad_actual - cantidad_reducir

            producto.save()
        else:
         raise serializers.ValidationError("No existe ese producto con eses caracteristicas")
        
    
    def guardarTopeMinim(idproducto, cantidad_reducir):
        producto = Productos.objects.get(id=idproducto)

        if producto:
            producto.cantidad_actual = producto.cantidad_actual - cantidad_reducir

            producto.save()
        else:
         raise serializers.ValidationError("No existe ese producto con eses caracteristicas")