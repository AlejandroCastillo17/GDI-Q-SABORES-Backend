from rest_framework import serializers
from ..models import Notificaciones

# from django.db.models.signals import post_save
# from django.dispatch import receiver

class NotificacionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificaciones
        fields = ['id', 'productoId', 'mensaje', 'fecha', 'leida']

        # sabores/signals.py


    # @receiver(post_save, sender=Productos)
    def verificar_tope_minimo(producto):
        try:
            if producto.cantidad_actual <= producto.topeMin:
                notificacion_existente = Notificaciones.objects.filter(
                    productoId=producto,
                    leida=False
                ).exists()

                if not notificacion_existente:
                    Notificaciones.objects.create(
                        productoId=producto,
                        mensaje=f"El producto '{producto.nombre}' ha alcanzado su tope mínimo, la cantidad actual es: ({producto.cantidad_actual})"
                    )
                else:
                    Notificaciones.objects.update(
                        productoId=producto,
                        mensaje=f"El producto '{producto.nombre}' ha alcanzado su tope mínimo, la cantidad actual es: ({producto.cantidad_actual})"
                    )
            else:
                Notificaciones.objects.filter(
                    productoId=producto,
                    leida=False
                ).update(leida=True)

        except Exception as e:
            print(e)
            return e
