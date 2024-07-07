from django.db import models
from django.contrib.auth.models import User
from .tipo import *

# Create your models here.



class Usuario(models.Model):

    usuario=models.OneToOneField(User, unique=True, related_name='perfil', on_delete=models.CASCADE)

    rut = models.CharField(max_length=12, primary_key=True)
    bloqueado = models.BooleanField(default=False)  

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nom_producto = models.CharField(max_length=100)
    descripcion = models.TextField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    imagen=models.ImageField(upload_to='producto/',null=False)
    habilitado = models.BooleanField(default=True)
    stock=models.IntegerField(default=0,null=False)


    def __str__(self):
        return self.nom_producto

class Pedido(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    #nombre_producto = models.CharField(max_length=100)
    #precio = models.DecimalField(max_digits=10, decimal_places=2)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pedido = models.DateField()
    estado = models.CharField(max_length=50,choices=ESTADO_PRODUCTO,default='PREPARACION')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    Cantidad = models.ForeignKey('CantidadProducto', on_delete=models.CASCADE)
    delivery = models.ForeignKey('Delivery', on_delete=models.CASCADE)
    def __str__(self):  
        return f"{self.usuario}-{self.Cantidad}"
    
class Delivery(models.Model):
    id_delivery=models.AutoField(primary_key=True)
    direccion=models.CharField(max_length=100,null=False)
    telefono= models.IntegerField(null=False)
    referencia=models.CharField(max_length=100, null=True)  
    comentario=models.CharField(max_length=150, null=True)
    propietario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.direccion}-{self.referencia}-{self.telefono}"
class Comanda(models.Model):
    id_comanda = models.AutoField(primary_key=True)

    fecha_emision = models.DateTimeField(auto_now_add=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    direccion = models.ForeignKey (Delivery, on_delete=models.CASCADE)
    terminada = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.pedido}-{self.direccion}"

class CantidadProducto(models.Model):
    id_cant_prod = models.AutoField(primary_key=True)
    #nom_producto = models.CharField(max_length=100)
    cant_producto = models.PositiveIntegerField()
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.cant_producto} Promos de {self.producto}"
#compre genera pedido, y de pedido genera comanda