from django.db import models

# Create your models here.

class Comuna(models.Model):
    id_comuna = models.AutoField(primary_key=True)
    nomb_comuna = models.CharField(max_length=100)

    def __str__(self):
        return self.nomb_comuna

class Usuario(models.Model):
    rut = models.CharField(max_length=12, primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField(max_length=100)
    contraseña = models.CharField(max_length=100)
    esadmin = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nom_producto = models.CharField(max_length=100)
    descripcion = models.TextField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    imagen=models.ImageField(upload_to='producto/',null=True)


    def __str__(self):
        return self.nom_producto

class Pedido(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    nombre_producto = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pedido = models.DateField()
    estado = models.CharField(max_length=50)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)

    def __str__(self):
        return f"Pedido {self.id_pedido} - {self.nombre_producto}"

class Comanda(models.Model):
    id_comanda = models.AutoField(primary_key=True)
    nomb_comanda = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    fecha_emision = models.DateField()
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)

    def __str__(self):
        return self.nomb_comanda

class CantidadProducto(models.Model):
    id_cant_prod = models.AutoField(primary_key=True)
    nom_producto = models.CharField(max_length=100)
    cant_producto = models.PositiveIntegerField()
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nom_producto} - {self.cant_producto}"

    #makemigrations en la consola transformarlo en codigo cada vez que se hace una tabla
    #migrations para poder pasarlo a la base de datos 
    #se puede agregar los datos en la pagina de admin en django y por el sql viewer