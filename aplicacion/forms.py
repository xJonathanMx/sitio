from django import forms
from sitio.aplicacion.models import Producto

    

class ProductoAGForm(forms.ModelForm):
    id=forms.CharField(required=True)
    
    
    class Meta:
        model = Producto
        fields = ("id_producto","nom_producto","descripcion","valor","imagen")
