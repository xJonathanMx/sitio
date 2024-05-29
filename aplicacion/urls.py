

from django.urls import path,include
from .views import index,carta,pedidos,pagar,carrito,tabla_pedidos,registro_usuario,login,admin,detalle,gestion_usuario,Carta_admin

urlpatterns = [
    path('',index,name='index'),
    path('carta/',carta,name='carta'),
    path('pedidos/',pedidos,name='pedidos'),
    path('pagar/',pagar,name='pagar'),
    path('carrito/',carrito,name='carrito'),
    path('tabla pedidos/',tabla_pedidos,name='tabla_pedidos'),
    path('registro/',registro_usuario,name='registro_usuario'),
    path('login/',login,name='login'),
    path('admins/',admin,name='admins'),
    path('detalle/',detalle,name='detalle'),
    path('Usuarios/',gestion_usuario,name="Usuarios"),
    path('CartaAdmin/',Carta_admin,name='AdminCarta')
]
