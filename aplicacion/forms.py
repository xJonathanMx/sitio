from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password
from .models import Pedido, Usuario
from django.contrib.auth.models import User
from itertools import cycle
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UsernameField
from .models import Producto,Delivery


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ("nom_producto", "descripcion", "valor", "imagen")
class UpdProductoForm(forms.ModelForm):
    class Meta:
        model =Producto
        fields= ("nom_producto", 'stock',"descripcion", "valor", "imagen")
class DeliveryForm(forms.ModelForm):
    class Meta:
        model =Delivery
        fields=("direccion","telefono","referencia","comentario")

class frmCrearCuenta(UserCreationForm):
    class Meta:
        model=User
        fields=["username","first_name", "last_name","email", "password1","password2"]

class AgregarPedido(forms.ModelForm):
    class Meta:
        model=Pedido
        fields=("precio_total","estado")     


class RegistroUsuarioForm(forms.ModelForm):

    class Meta:
        model = Usuario
        fields = ['rut']

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')

        def validar_rut(rut):
            rut = rut.replace(".", "").replace("-", "").upper()  
            rut, verificador = rut[:-1], rut[-1]  

            if not rut.isdigit() or len(rut) < 7:
                return False  

            suma = sum(int(digit) * int(factor) for digit, factor in zip(reversed(rut), cycle(range(2, 8))))
            dv_esperado = (-suma) % 11

            if dv_esperado == 10:
                dv_esperado = "K"
    
            return str(dv_esperado) == verificador

        if not validar_rut(rut):
            raise forms.ValidationError("El RUT ingresado no es válido")
        return rut

    def save(self, commit=True):
        user = super(RegistroUsuarioForm, self).save(commit=False)
        user.contraseña = make_password(self.cleaned_data["password1"])  # Encriptar la contraseña
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(RegistroUsuarioForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Registrar'))



