from rest_framework import serializers
from .models import Usuario, Proveedores
from .models import Productos
from django.contrib.auth.models import User

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario, Proveedores
        fields = ['__all__', Proveedores.nombre]

class ProveedoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedores
        fields = ['id', 'nombre']
        
class ProductosSerializer(serializers.ModelSerializer):
    proveedores = ProveedoresSerializer(read_only=True)
    class Meta:
        model = Productos
        fields = ['__all__', "proveedores"] 

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