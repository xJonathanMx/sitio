from os import remove, path
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Producto,Usuario
from django.shortcuts import get_object_or_404
from .forms import DeliveryForm, ProductoForm, RegistroUsuarioForm, UpdProductoForm,DeliveryForm, frmCrearCuenta
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import JsonResponse
from django.contrib.auth.views import LoginView
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm





# Create your views here.



def index(request):
            return render(request,'aplicacion/index.html')

def carta(request):

    products = Producto.objects.all()
    return render(request,'aplicacion/carta.html', {'products':products})



def pedidos(request):
    return render(request,'aplicacion/pedidos.html')

def pagar(request):
    return render(request,'aplicacion/pagar.html')


def registro_usuario(request):
    if request.method == 'POST':
        formDatos = RegistroUsuarioForm(request.POST)
        form = frmCrearCuenta(request.POST)
        if form.is_valid() and formDatos.is_valid():
            try:
                form.save()
                datoDjango = form.cleaned_data
                usuario = User.objects.get(username =  datoDjango.get("username"))
                datos = formDatos.cleaned_data
                user = Usuario()
                user.rut = datos.get("rut")
                user.usuario = usuario
                user.save()
                return redirect('index')
            except IntegrityError:
                form.add_error('correo', 'El correo electrónico ya está en uso.')
    else:
        formDatos = frmCrearCuenta()
        form = RegistroUsuarioForm()
    return render(request, 'aplicacion/registro-usuario.html', {'form': form, 'form2' : formDatos})


class CustomLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = 'registration/login.html'

    def form_valid(self, form):
        user = form.get_user()
        auth_login(self.request, user)
        if user.is_staff:
            return redirect('admins')
        else:
            return redirect('index')

def login(request):
    return render (request,'aplicacion/login.html')

def tabla_pedidos(request):
    return render(request,'aplicacion/tabla_pedidos.html')


#funcionalidad carrito

def agregar_al_carrito(request, id_producto):
    carrito = request.session.get('carrito', [])

    carrito = [item for item in carrito if isinstance(item, dict) and 'id_producto' in item]
    producto_existente = next((item for item in carrito if item['id_producto'] == id_producto), None)

    if producto_existente:
        producto_existente['cantidad'] += 1
    else:                                                                       
        carrito.append({'id_producto': id_producto, 'cantidad': 1})

    request.session['carrito'] = carrito
    return redirect('carrito')


def carrito(request):
    lista_productos_carrito = request.session.get('carrito', [])
    formulario=DeliveryForm
    productos = Producto.objects.filter(id_producto__in=[item['id_producto'] for item in lista_productos_carrito])
    productos_carrito = []

    for producto in productos:
        for item in lista_productos_carrito:
            if item['id_producto'] == producto.id_producto:
                productos_carrito.append({
                    'producto': producto,
                    'cantidad': item['cantidad'],
                    'subtotal': producto.valor * item['cantidad']
                })
                break

    total = sum(item['subtotal'] for item in productos_carrito)

    context = {
        'productos_carrito': productos_carrito,
        'total': total,
        'fomulario':formulario
    }
    return render(request, 'aplicacion/carrito.html', context)


def eliminar_del_carrito(request, id_producto):
    carrito = request.session.get('carrito', [])

    carrito_copy = carrito.copy()

    for item in carrito_copy:
        if isinstance(item, dict) and item.get('id_producto') == id_producto:
            if item['cantidad'] > 1:
                item['cantidad'] -= 1
            else:
                carrito.remove(item)
            break

    request.session['carrito'] = carrito
    return redirect('carrito')



def admin(request):
    return render(request,'aplicacion/admin_usuario.html')



def gestion_usuario(request):
    usuarios=Usuario.objects.all()
        
    datos = {
        "usuario": usuarios,
        
    }
    return render(request,'aplicacion/gestion_usuarios.html',datos)


def Carta_admin(request):
    producto=Producto.objects.all()
    formulario = ProductoForm()
        
    datos = {
        "producto": producto,
        "formulario":formulario
    }

    return render(request,'aplicacion/admin_carta_agregar.html',datos)


def Agregar_Producto (request):

    
    if request.method == "POST":
        formulario = ProductoForm(request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Producto agregado exitosamente")
            return redirect('AdminCarta')
        else:
            messages.error(request,"Error al agregar el producto")
            return redirect('AdminCarta')
    



def admin_Carta_M (request,id):
    producto=get_object_or_404(Producto,id_producto=id)
    formU=UpdProductoForm(instance=producto)

    if request.method=='POST':
        formU=UpdProductoForm(request.POST, files=request.FILES, instance=producto)
        if formU.is_valid():
            formU.save()
            messages.set_level(request,messages.WARNING)
            messages.warning(request,"Producto Modificado")
            return redirect('AdminCarta')   
    datos={
        'formU':formU,
        'producto':producto
    }
    return render(request,'aplicacion/admin_Carta_M.html',datos)

def admin_Carta_E(request,id):
    producto=get_object_or_404(Producto,id_producto=id)
    if request.method=="POST":
        producto.delete()
        remove(path.join(str(settings.MEDIA_ROOT).replace('/media','')+str(producto.imagen.url).replace('/','\\')))
        messages.set_level(request,messages.WARNING)
        messages.warning(request,'Producto eliminado correctamente')
        return redirect('AdminCarta')
    
    datos={
        'productos':producto
    }
    return render(request,'aplicacion/admin_Carta_E.html',datos)    
    

def detalle(request,id):
    producto=get_object_or_404(Producto,id_producto=id)
    datos={
        "producto":producto
    }
    return render(request,'aplicacion/detalle.html',datos)  
