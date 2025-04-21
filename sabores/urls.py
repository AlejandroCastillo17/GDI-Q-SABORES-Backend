from rest_framework import routers
from sabores import authView, productosView
from django.urls import path,include, re_path


router = routers.DefaultRouter()
router.register(r'productos', productosView.ProductoView ,'productos')
router.register(r'usuarios', authView.UserView,'usuarios')

#router.register(r'productos', productosView.actualizar_producto(),'productos')

urlpatterns = [
    path("api/v1/",include(router.urls)),
    path("/api/v1/usuarios/login/", authView.UserView.as_view({"post": "login"})),
    
]
