from django.contrib import admin
from .models import  Delivery, Usuario, Producto, Pedido, Comanda, CantidadProducto

# Register your models here.
#para que salga como una lista en la base de datos
#class adminMascota(admin.ModelAdmin):
    #list_display=['id','nombre','edad','tipo','propietario']
    #list_editable=['rut','nombre','apellido','f_nacto']

##admin.site.register(Persona)



@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('rut', 'nombre', 'apellido', 'correo', 'esadmin')
    search_fields = ('rut', 'nombre', 'apellido', 'correo')
    list_filter = ('esadmin',)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id_producto', 'nom_producto', 'valor')
    search_fields = ('nom_producto', 'descripcion')
    list_filter = ('valor',)

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id_pedido', 'precio_total', 'fecha_pedido', 'estado', 'usuario')# 'nombre_producto', 'precio',
    search_fields = ('estado', 'usuario__nombre')#'nombre_producto', 
    list_filter = ('estado', 'fecha_pedido', 'usuario')

@admin.register(Comanda)
class ComandaAdmin(admin.ModelAdmin):
    list_display = ('id_comanda', 'nomb_comanda', 'direccion', 'fecha_emision', 'pedido')
    search_fields = ('nomb_comanda', 'direccion', 'pedido__id_pedido')
    list_filter = ('fecha_emision',)

@admin.register(CantidadProducto)
class CantidadProductoAdmin(admin.ModelAdmin):
    list_display = ('id_cant_prod', 'nom_producto', 'cant_producto', 'pedido', 'producto')
    search_fields = ('nom_producto', 'pedido__id_pedido')#, 'producto__nom_producto'
    list_filter = ('cant_producto',)

@admin.register(Delivery)
class DeliveryUser(admin.ModelAdmin):
    list_display=('id_delivery','direccion','telefono','referencia','comentario')
    list_filter=['propietario','telefono']
