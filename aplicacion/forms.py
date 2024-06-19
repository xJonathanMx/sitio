from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password
from .models import Usuario
from itertools import cycle
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UsernameField
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ("nom_producto", "descripcion", "valor", "imagen")
class UProductoForm(forms.ModelForm):
    class Meta:
        model =Producto
        fields= ("nom_producto", "descripcion", "valor", "imagen")


class RegistroUsuarioForm(forms.ModelForm):
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ['rut', 'nombre', 'apellido', 'correo']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password2

    def clean_correo(self):
        correo = self.cleaned_data.get('correo')
        if Usuario.objects.filter(correo=correo).exists():
            raise forms.ValidationError("El correo electrónico ya está en uso.")
        return correo
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Usuario.objects.filter(username=username).exists():
            raise forms.ValidationError("Este usuario ya está en uso.")
        return username

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')

        def validar_rut(rut):
            rut = rut.replace(".", "").replace("-", "").upper()  # Elimina puntos y guiones y convierte a mayúsculas
            rut, verificador = rut[:-1], rut[-1]  # Separa el número del verificador

            if not rut.isdigit() or len(rut) < 7:
                return False  # El RUT debe contener al menos 7 dígitos

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



