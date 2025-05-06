from rest_framework import routers
from django.urls import path,include

from sabores.views import authView, productosView, gastosView, proveedoresView, categoriasView


router = routers.DefaultRouter()
router.register(r'productos', productosView.ProductoView ,'productos')
router.register(r'usuarios', authView.UserView,'usuarios')
router.register(r'gastos', gastosView.GastoView,'gastos')
router.register(r'proveedores', proveedoresView.ProveedoresView,'proveedores')
router.register(r'categorias', categoriasView.CategoriasView,'categorias')

urlpatterns = [
    path("api/v1/",include(router.urls)),
]
