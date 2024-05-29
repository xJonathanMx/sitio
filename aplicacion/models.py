from django.db import models

# Create your models here.








#class Persona(models.Model):
    #rut=models.CharField(max_length=10, primary_key=True)
    #nombre=models.CharField( max_length=50,null=False)
    #apellido=models.CharField(max_length=50,null=False)
    #f_nacto=models.DateField(max_length=50,)
    
    
    #def __str__(self):
        #return f"{self.rut}-{self.nombre}-{self.apellido}-{self.f_nacto}"
    
# #class Mascota(models.Model):
#         #nombre=models.CharField( max_length=50,null=False)
#         edad=models.IntegerField()
#         tipo=models.CharField(max_length=20) 
#         #Dueño de la mascota
#         propietario=models.ForeignKey(Persona, on_delete=models.PROTECT)
        
#         def __str__(self):
#             return self.nombre +"-"+self.tipo
        
    


    
    



    #makemigrations en la consola transformarlo en codigo cada vez que se hace una tabla
    #migrations para poder pasarlo a la base de datos 
    #se puede agregar los datos en la pagina de admin en django y por el sql viewer