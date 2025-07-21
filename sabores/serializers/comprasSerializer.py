from rest_framework import serializers
from ..models import Compras, DetallesCompras, Productos
from .detallesComprasSerializer import DetallesComprasSerializer
from .productosSerializer import ProductosSerializer
from django.db import transaction
from datetime import timedelta
from django.utils import timezone

class ComprasSerializer(serializers.ModelSerializer):
    detallesCompra = DetallesComprasSerializer(many=True)

    class Meta:
        model = Compras
        fields = ["id", "subtotal", "fecha", "detallesCompra"]

    def create(self, validated_data):
        detalles_data = validated_data.pop('detallesCompra', [])
        compra = Compras.objects.create(**validated_data)

        for detalle in detalles_data:
            producto = detalle['idproducto']
            cantidad = detalle['cantidad']
            DetallesCompras.objects.create(idcompra=compra, **detalle)

            ProductosSerializer.aumentar_cantidad_inventario(producto.id, cantidad)
            ProductosSerializer.aumentar_cantidad_inicial_inventario(producto.id, cantidad)

        return compra

    def update(self, instance, validated_data):
        try:
            with transaction.atomic():  # Todas las operaciones son atómicas
                detalles_data = validated_data.pop('detallesCompra', [])
                # Validación básica de los datos entrantes
                if not detalles_data:
                    raise serializers.ValidationError({"detallesCompra": "Debe proporcionar al menos un detalle de compra."})
                
                # Actualizar campos simples de la compra
                instance.subtotal = validated_data.get('subtotal', instance.subtotal)
                instance.fecha = validated_data.get('fecha', instance.fecha)
                instance.save()

                # Procesar detalles de compra
                self._procesar_detalles_compra(instance, detalles_data)
                
                # Refrescar la instancia para incluir los cambios
                instance.refresh_from_db()
                return {
                'status': 'success',
                'code': 200,
                'data': {
                    'id': instance.id,
                    'subtotal': instance.subtotal,
                    'fecha': instance.fecha,
                    'detalles': [self._serializar_detalle(d) for d in instance.detallesCompra.all()]
                }
            }
                
        except Exception as e:
        # Registra el error completo (útil para depuración)
            print(f"Error en update: {str(e)}")#, exc_info=True)
            raise serializers.ValidationError({
                'status': 'error',
                'code': 400,
                'message': str(e),
                'details': getattr(e, 'detail', None)
            })

 
    def _procesar_detalles_compra(self, instance, detalles_data):

        print("detalles_data", detalles_data)
        detalles_existentes = {d.id: d for d in instance.detallesCompra.all()}
        print("detalles_existentes", detalles_existentes)


        for detalle_data in detalles_data:
            detalle_id = detalle_data.get('id')
            if not detalle_id:
                continue  # ignorar sin ID
            
            if detalle_id in detalles_existentes:
                self._actualizar_detalle_existente(detalles_existentes[detalle_id], detalle_data)
            else:
                raise serializers.ValidationError({
                    "id": f"Detalle con ID {detalle_id} no pertenece a esta compra."
                })


    def _actualizar_detalle_existente(self, detalle, detalle_data):
        """Actualizar un detalle existente (sin crear ni eliminar)"""
        producto = detalle.idproducto
        producto_nuevo = detalle_data.get('idproducto', producto)
        cantidad_original = detalle.cantidad
        cantidad_nueva = detalle_data.get('cantidad', cantidad_original)

        producto_nuevo_id = producto_nuevo.id if hasattr(producto_nuevo, 'id') else producto_nuevo
        producto_id = producto.id if hasattr(producto, 'id') else producto

        # Para comparar productos correctamente
        diferente_producto = producto_nuevo_id != producto_id

        ahora = timezone.now()
        hace_24h = detalle.created_at + timedelta(hours=24)
        modificar_inventario = (
            ahora <= hace_24h and (
                cantidad_nueva != cantidad_original or diferente_producto
            )
        )
        print("cantidad", cantidad_original, cantidad_nueva)
        if modificar_inventario:
            ProductosSerializer.reducir_cantidad_inventario(producto_id, cantidad_original)
            ProductosSerializer.reducir_cantidad_inicial_inventario(producto_id, cantidad_original)

        for attr, value in detalle_data.items():
            setattr(detalle, attr, value)
        detalle.save()
        print("modificar_inventario", modificar_inventario)
        if modificar_inventario:
            # Aplicar nueva cantidad al inventario
            ProductosSerializer.aumentar_cantidad_inventario(producto_nuevo_id, cantidad_nueva)
            ProductosSerializer.aumentar_cantidad_inicial_inventario(producto_nuevo_id, cantidad_nueva)

    
    def delete(self, instance):
        # Revertir cambios en inventario al eliminar compra
        for detalle in instance.detallesCompra.all():
            ProductosSerializer.reducir_cantidad_inventario(detalle.idproducto.id, detalle.cantidad)
            ProductosSerializer.reducir_cantidad_inicial_inventario(detalle.idproducto.id, detalle.cantidad)
        
        instance.delete()

    def _serializar_detalle(self, detalle):
        return {
            'id': detalle.id,
            'idproducto': detalle.idproducto.id,
            'producto_nombre': detalle.idproducto.nombre,  # Asume que existe
            'cantidad': detalle.cantidad
        }

