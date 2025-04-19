from rest_framework import routers
from sabores import views, authView
from django.urls import path,include, re_path


router = routers.DefaultRouter()
router.register(r'usuarios', views.UserView,'usuarios')
router.register(r'productos', views.ProductoView,'productos')


urlpatterns = [
    path("api/v1/",include(router.urls)),
    re_path('login', authView.login),

]
