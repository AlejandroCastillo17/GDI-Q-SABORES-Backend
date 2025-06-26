from rest_framework import serializers
from ..models import Ventas, DetallesVentas, Notificaciones
from .productosSerializer import ProductosSerializer
from .detallesVentasSerializer import DetallesVentasSerializer
from .notificacionesSerializer import NotificacionesSerializer

class VentasSerializer(serializers.ModelSerializer):

    detallesVentas = DetallesVentasSerializer(many=True)

    class Meta:
        model = Ventas
        fields = ["id", "fecha", "total", "detallesVentas"]


    def create(self, validated_data):
        detalles_data = validated_data.pop('detallesVentas')

        total = 0

        for detalle in detalles_data:
            producto = detalle["idproducto"]
            cantidad = detalle['cantidad']

            if cantidad > producto.cantidad_actual:
                raise ValueError(f"Stock insuficiente para el producto ({producto.nombre})")
            
            total = total + (producto.precio * cantidad)
        
        ventas = Ventas.objects.create(**validated_data, total=total)

        for detalle in detalles_data:
            DetallesVentas.objects.create(idventa=ventas, **detalle)
            producto = detalle['idproducto']
            cantidad = detalle['cantidad']

            ProductosSerializer.reducir_cantidad_inventario(producto.id, cantidad)
            NotificacionesSerializer.verificar_tope_minimo(producto)
            # if producto.cantidad_actual <= producto.topeMin:
            #     Notificaciones.objects.create(
            #         productoId=producto,
            #         mensaje=f"El producto '{producto.nombre}' ha alcanzado su tope mínimo, la cantidad actual es: ({producto.cantidad_actual})",
            #     )

        ventas.total = total
        ventas.save()
        return ventas
