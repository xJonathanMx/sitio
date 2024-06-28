
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import index, carta, pedidos, pagar, carrito, tabla_pedidos, registro_usuario, login, admin, detalle, gestion_usuario, Carta_admin, agregar_al_carrito, eliminar_del_carrito,Agregar_Producto,admin_Carta_M,admin_Carta_E
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', index, name='index'),
    path('carta/', carta, name='carta'),
    path('pedidos/', pedidos, name='pedidos'),
    path('pagar/', pagar, name='pagar'),
    path('carrito/', carrito, name='carrito'),
    path('tabla_pedidos/', tabla_pedidos, name='tabla_pedidos'),
    path('registro/', registro_usuario, name='registro_usuario'),
    path('login/' , login, name='login'),
    path('admins/', admin, name='admins'),
    path('detalle/<id>',detalle, name='detalle'),
    path('Usuarios/', gestion_usuario, name="Usuarios"),
    path('CartaAdmin/', Carta_admin, name='AdminCarta'),
    path("EditarProducto/<id>", admin_Carta_M, name="DetalleAdmin"),
    path("EliminarProducto/<id>", admin_Carta_E, name="Eliminar_Producto"),
    path('agregar-producto/', Agregar_Producto, name='Agregar_Producto'),
    path('agregar_al_carrito/<int:id_producto>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('eliminar_del_carrito/<int:id_producto>/', eliminar_del_carrito, name='eliminar_del_carrito'),
    
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

