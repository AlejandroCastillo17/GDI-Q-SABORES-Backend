from rest_framework import routers
from django.urls import path,include

from sabores.views import authView, productosView, gastosView, proveedoresView


router = routers.DefaultRouter()
router.register(r'productos', productosView.ProductoView ,'productos')
router.register(r'usuarios', authView.UserView,'usuarios')
router.register(r'gastos', gastosView.GastoView,'gastos')
router.register(r'proveedores', proveedoresView.ProveedoresView,'proveedores')

urlpatterns = [
    path("api/v1/",include(router.urls)),
]
