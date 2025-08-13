from rest_framework import serializers
from ..models import Proveedores, Categorias
from ..models import Productos
from django.contrib.auth.models import User
from .proveedoresSerializer import ProveedoresSerializer
from .categoriasSerializer import CategoriasSerializer

        
class ProductosSerializer(serializers.ModelSerializer):
    proveedorid = serializers.PrimaryKeyRelatedField(
        queryset=Proveedores.objects.all()) 
    proveedor = ProveedoresSerializer(source='proveedorid', read_only=True)

    categoriaid = serializers.PrimaryKeyRelatedField(
    queryset=Categorias.objects.all(), 
    write_only=True)
    categoria = CategoriasSerializer(source='categoriaid', read_only=True)

    id = serializers.IntegerField(required=False)

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
        try:
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
        except Exception as e:
            return e

    def reducir_cantidad_inventario(idproducto, cantidad_reducir):
        producto = Productos.objects.get(id=idproducto)

        if producto:
            producto.cantidad_actual = producto.cantidad_actual - cantidad_reducir

            producto.save()
        else:
         raise serializers.ValidationError("No existe ese producto con esas caracteristicas")
        
        
    def aumentar_cantidad_inventario(idproducto, cantidad_aumentar):
        producto = Productos.objects.get(id=idproducto)

        if producto:
            producto.cantidad_actual = producto.cantidad_actual + cantidad_aumentar

            producto.save()
        else:
         raise serializers.ValidationError("No existe ese producto con esas caracteristicas")
        
    def aumentar_cantidad_inicial_inventario(idproducto, cantidad_aumentar):
        producto = Productos.objects.get(id=idproducto)

        if producto:
            print("producto", producto.cantidad_actual)
            if producto.cantidad_actual == 0:
                producto.cantidad_inicial = cantidad_aumentar
            else:
                producto.cantidad_inicial = producto.cantidad_actual + cantidad_aumentar

            producto.save()
        else:
         raise serializers.ValidationError("No existe ese producto con esas caracteristicas")
        
    def reducir_cantidad_inicial_inventario(idproducto, cantidad_reducir):
        producto = Productos.objects.get(id=idproducto)

        if producto:
            producto.cantidad_inicial = producto.cantidad_inicial - cantidad_reducir
            producto.save()
        else:
            raise serializers.ValidationError("No existe ese producto con esas caracteristicas")
                
    
    # def guardar_tope_minim(idproducto):
    #     producto = Productos.objects.get(id=idproducto)

    #     if producto:
    #         producto.cantidad_actual = producto.cantidad_actual - cantidad_reducir

    #         producto.save()
    #     else:
    #      raise serializers.ValidationError("No existe ese producto con eses caracteristicas")