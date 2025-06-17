from rest_framework import routers
from django.urls import path,include

from sabores.views import authView, comprasView, productosView, gastosView, proveedoresView, categoriasView, ventasView


router = routers.DefaultRouter()
router.register(r'productos', productosView.ProductoView ,'productos')
router.register(r'usuarios', authView.UserView,'usuarios')
router.register(r'gastos', gastosView.GastoView,'gastos')
router.register(r'proveedores', proveedoresView.ProveedoresView,'proveedores')
router.register(r'categorias', categoriasView.CategoriasView,'categorias')
router.register(r'compras', comprasView.ComprasView,'compras')
router.register(r'ventas', ventasView.VentasView,'ventas')

urlpatterns = [
    path("api/v1/",include(router.urls)),
]
