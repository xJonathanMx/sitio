from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Producto
from django.shortcuts import get_object_or_404
from .forms import ProductoForm, RegistroUsuarioForm, UProductoForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import JsonResponse





# Create your views here.



def index(request):
            return render(request,'aplicacion/index.html')

def carta(request):

    products = Producto.objects.all()
    return render(request,'aplicacion/carta.html', {'products':products})

def detalle(request,id):
    producto=get_object_or_404(Producto,id_producto=id)
    datos={
        "producto":producto
    }
    return render(request,'aplicacion/detalle.html',datos)  

def pedidos(request):
    return render(request,'aplicacion/pedidos.html')

def pagar(request):
    return render(request,'aplicacion/pagar.html')


def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.is_staff = False
                user.is_superuser = False
                user.save()
                return redirect('index')
            except IntegrityError:
                form.add_error('correo', 'El correo electrónico ya está en uso.')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'aplicacion/registro-usuario.html', {'form': form})


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
        'total': total
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
    return render(request,'aplicacion/gestion_usuarios.html')


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
    return JsonResponse({'success': False, 'error': 'Solicitud inválida'})

def Modificar_Producto (request,id_producto):
    Producto=get_object_or_404(Producto,id=id_producto)
    formU=UProductoForm(instance=Producto)

    if formU.is_valid():
        formU=UProductoForm(request.POST, files=request.FILES, instance=Producto)
        formU.save()
        messages.set_level(request,messages.WARNING)
        messages.warning(request,"Producto Modificado")
        return redirect('AdminCarta')
    else:
            messages.error(request,"Error al Modificar el Producto")
            return redirect('AdminCarta')
    
def Eliminar_Producto (request,id):
    producto=get_object_or_404(Producto,id_producto=id)
    if request.method=="POST":
        producto.delete()
        return redirect(to='AdminCarta')
   
    return redirect('AdminCarta')
    
    


