from rest_framework import serializers
from ..models import Usuario, Proveedores
from ..models import Productos
from django.contrib.auth.models import User

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['__all__']

class ProveedoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedores
        fields = ['id', 'nombre']
        
class ProductosSerializer(serializers.ModelSerializer):
    proveedorid = serializers.PrimaryKeyRelatedField(
        queryset=Proveedores.objects.all(), 
        write_only=True) 
    proveedor = ProveedoresSerializer(source='proveedorid', read_only=True)

    class Meta:
        model = Productos
        fields = ['id',
            'nombre',
            'categoria',
            'precio',
            'cantidad_actual',
            'cantidad_inicial',
            'foto',
            'topeMin',
            'proveedorid',
            'proveedor']

    def validate(self, data):
        nombre = data.get('nombre')
        categoria = data.get('categoria')
        proveedorid = data.get('proveedorid')

        # Al actualizar, excluirse a sí mismo de la validación
        instance_id = self.instance.id if self.instance else None

        if Productos.objects.filter(
            nombre=nombre, categoria=categoria, proveedorid=proveedorid
        ).exclude(id=instance_id).exists():
            raise serializers.ValidationError("Ya existe un producto con ese nombre, categoría y proveedor.")
        
        return data
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {
            'password': {'write_only': True}
        }