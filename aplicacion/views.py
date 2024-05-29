from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'aplicacion/index.html')

def carta(request):
    return render(request,'aplicacion/carta.html')

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

def carrito(request):
    return render(request,'aplicacion/carrito.html')
def admin(request):
    return render(request,'aplicacion/admin.html')

def detalle(request):
    return render(request,'aplicacion/detalle.html')
