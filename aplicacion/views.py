from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Producto

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
    return render(request,'aplicacion/registro-usuario.html')
def login(request):
    return render (request,'aplicacion/login.html')

def tabla_pedidos(request):
    return render(request,'aplicacion/tabla_pedidos.html')


#funcionalidad carrito

def agregar_al_carrito(request, id_producto):
    carrito = request.session.get('carrito', [])

    # Obtener el producto del carrito si existe
    producto_existente = next((item for item in carrito if item['id_producto'] == id_producto), None)

    if producto_existente:
        # Incrementar la cantidad del producto en el carrito
        producto_existente['cantidad'] += 1
    else:                                                                       
        # Agregar el producto al carrito con cantidad 1
        carrito.append({'id_producto': id_producto, 'cantidad': 1})

    request.session['carrito'] = carrito
    return redirect('carrito')


def carrito(request):
    lista_productos_carrito = request.session.get('carrito', [])
    # Filtrar solo los elementos que son diccionarios y tienen la clave 'id_producto'
    productos_carrito = Producto.objects.filter(id_producto__in=[item['id_producto'] for item in lista_productos_carrito if isinstance(item, dict) and 'id_producto' in item])
    context = {
        'productos_carrito': productos_carrito
    }
    return render(request,'aplicacion/carrito.html',context)


def eliminar_del_carrito(request, id_producto):
    carrito = request.session.get('carrito', [])

    # Crear una copia del carrito para evitar problemas al iterar y modificar la lista original
    carrito_copy = carrito.copy()

    # Iterar sobre la copia del carrito y eliminar el diccionario correspondiente al producto
    for item in carrito_copy:
        if item.get('id_producto') == id_producto:
            carrito.remove(item)

    # Actualizar el carrito en la sesión
    request.session['carrito'] = carrito

    # Redirigir al usuario de vuelta al carrito
    return redirect('carrito')

def admin(request):
    return render(request,'aplicacion/admin_usuario.html')

def detalle(request):
    return render(request,'aplicacion/detalle.html')
def gestion_usuario(request):
    return render(request,'aplicacion/gestion_usuarios.html')
def Carta_admin(request):
    return render(request,'aplicacion/admin_carta_agregar.html')