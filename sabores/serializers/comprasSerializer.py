from rest_framework import serializers
from ..models import Compras, DetallesCompras
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
                print("validated_data", validated_data)
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
            print(f"Error en update: {str(e)}", exc_info=True)
            raise serializers.ValidationError({
                'status': 'error',
                'code': 400,
                'message': str(e),
                'details': getattr(e, 'detail', None)
            })

 
    def _procesar_detalles_compra(self, instance, detalles_data):
        """Solo actualiza los detalles existentes, no crea ni elimina"""
        print("estoy en procesar detalles compras")
        print("detalles_data", detalles_data)
        detalles_existentes = {d.id: d for d in instance.detallesCompra.all()}
        print("detalles_existentes", detalles_existentes)


        for detalle_data in detalles_data:
            detalle_id = detalle_data.get('id')
            print("detalle", detalle_data)#EL PROBLEMA ES QUE AQUI NO ESTÁ TRAYENDO EL ID, SI LO MANDA EL FRONTEND PERO EL BACKEND NO LO ESTÁ GESTIONANDO BIEN
            if not detalle_id:
                continue  # ignorar sin ID
            
            if detalle_id in detalles_existentes:
                print("entra")
                self._actualizar_detalle_existente(detalles_existentes[detalle_id], detalle_data)
            else:
                raise serializers.ValidationError({
                    "id": f"Detalle con ID {detalle_id} no pertenece a esta compra."
                })


    def _actualizar_detalle_existente(self, detalle, detalle_data):
        """Actualizar un detalle existente (sin crear ni eliminar)"""
        producto = detalle.idproducto
        cantidad_original = detalle.cantidad
        cantidad_nueva = detalle_data.get('cantidad', cantidad_original)

        # Solo modificar inventario si han pasado menos de 24 horas desde la creación
        ahora = timezone.now()
        hace_24h = detalle.created_at + timedelta(hours=24)
        print("hace_24h", hace_24h)
        modificar_inventario = ahora <= hace_24h and cantidad_nueva != cantidad_original

        if modificar_inventario:
            # Revertir cantidad anterior
            ProductosSerializer.reducir_cantidad_inventario(producto.id, cantidad_original)
            ProductosSerializer.reducir_cantidad_inicial_inventario(producto.id, cantidad_original)

        # Actualizar campos del detalle
        for attr, value in detalle_data.items():
            setattr(detalle, attr, value)
        detalle.save()

        if modificar_inventario:
            # Aplicar nueva cantidad al inventario
            ProductosSerializer.aumentar_cantidad_inventario(producto.id, detalle.cantidad)
            ProductosSerializer.aumentar_cantidad_inicial_inventario(producto.id, detalle.cantidad)

    
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



    # def _crear_nuevo_detalle(self, instance, detalle_data):
    #     """Crear un nuevo detalle de compra"""
    #     if 'idproducto' not in detalle_data:
    #         raise serializers.ValidationError({"idproducto": "Este campo es requerido."})

    # def _revertir_cambios_inventario(self, detalle):
    #     """Revertir cambios en el inventario para un detalle"""
    #     ProductosSerializer.reducir_cantidad_inventario(detalle.idproducto.id, detalle.cantidad)
    #     ProductosSerializer.reducir_cantidad_inicial_inventario(detalle.idproducto.id, detalle.cantidad)

        
    #     detalle = DetallesCompras.objects.create(idcompra=instance, **detalle_data)
    #     ProductosSerializer.aumentar_cantidad_inventario(detalle.idproducto.id, detalle.cantidad)
    #     ProductosSerializer.aumentar_cantidad_inicial_inventario(detalle.idproducto.id, detalle.cantidad)
