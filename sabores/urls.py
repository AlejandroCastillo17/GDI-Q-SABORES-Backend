from rest_framework import routers
from sabores import views, authView, productosView
from django.urls import path,include, re_path


router = routers.DefaultRouter()
router.register(r'usuarios', views.UserView,'usuarios')
router.register(r'productos', views.ProductoView,'productos')
#router.register(r'productos', productosView.actualizar_producto(),'productos')


urlpatterns = [
    path("api/v1/",include(router.urls)),
    re_path('login', authView.login),
    path('productos', productosView.buscar_productos),
    path('productos', productosView.crear_producto),
    path('productos/<int:id>', productosView.actualizar_producto),
    path('productos/<int:id>/delete', productosView.eliminar_producto),
]
