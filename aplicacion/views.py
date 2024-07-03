from datetime import timezone
from os import remove, path
from django.conf import settings
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from .models import CantidadProducto, Comanda, Delivery, Pedido, Producto,Usuario
from django.shortcuts import get_object_or_404
from .forms import DeliveryForm, ProductoForm, RegistroUsuarioForm, UpdProductoForm,DeliveryForm, frmCrearCuenta,AgregarPedido
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.views import LoginView
from django.contrib.auth import login as auth_login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone  
from .tipo import *





# Create your views here.



def index(request):
            return render(request,'aplicacion/index.html')


def carta(request):

    products = Producto.objects.all()
    return render(request,'aplicacion/carta.html', {'products':products})



def pedidos(request):
    pedidos = Pedido.objects.filter(usuario=request.user)
    cantidadProduct = CantidadProducto.objects.all()
    producto = Producto.objects.all()
    datos={
        'producto' : producto,
        'pedidos' : pedidos, 
        'cantidadProductos' : cantidadProduct
    }
    return render(request,'aplicacion/pedidos.html',datos)

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

#login
class CustomLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = 'registration/login.html'

    def form_valid(self, form):
        user = form.get_user()
        
        # Verificar si el usuario está bloqueado
        try:
            usuario = Usuario.objects.get(usuario=user)
            if usuario.bloqueado:
                # Mostrar un mensaje de cuenta bloqueada
                messages.error(self.request, 'Tu cuenta está temporalmente bloqueada. Contacta al administrador.')
                return redirect('login')  # Redirigir nuevamente al formulario de login
        except Usuario.DoesNotExist:
            messages.error(self.request, 'No hay cuenta asosciada a estas credenciales')

        auth_login(self.request, user)
        
        # Redirigir según el tipo de usuario
        if user.is_staff:
            return redirect('index')
        else:
            messages.success(self.request, f'Bienvenido {user.username}')
            return redirect('index')

def login(request):
    return render (request,'aplicacion/login.html')

def pedidos(request):
    pedido=Pedido.objects.all()
    delivery=Delivery.objects.all()
    cantidad=CantidadProducto.objects.all()
    producto=Producto.objects.all() # Asegúrate de tener esta URL configurada
    datos={
        'pedido':pedido,
        'delivery':delivery,
        'cantidad':cantidad,
        'producto':producto
    }
    return render(request,'aplicacion/pedidos.html',datos)

def tabla_pedidos(request):
    pedido=Pedido.objects.all()
    delivery=Delivery.objects.all()
    cantidad=CantidadProducto.objects.all()
    producto=Producto.objects.all()
    datos={
        'pedido':pedido,
        'delivery':delivery,
        'cantidad':cantidad,
        'producto':producto
    }
    return render(request,'aplicacion/tabla_pedidos.html',datos)

def cambiar_estado(request,id):
    if request.method == 'POST':
        pedido = get_object_or_404(Pedido, id_pedido=id)
        nuevo_estado = request.POST.get('nuevo_estado')
        if nuevo_estado in dict(ESTADO_PRODUCTO):
            pedido.estado = nuevo_estado
            pedido.save()
            return redirect('tabla_pedidos')
        else:
            return redirect('tabla_pedidos')
    return redirect('tabla_pedidos')

#funcionalidad carrito

def agregar_al_carrito(request, id_producto):
    carrito = request.session.get('carrito', [])

    carrito = [item for item in carrito if isinstance(item, dict) and 'id_producto' in item ]
    producto_existente = next((item for item in carrito if item['id_producto'] == id_producto), None)
    

    if producto_existente:
        producto_existente['cantidad'] += 1
    else:                                                                       
        carrito.append({'id_producto': id_producto, 'cantidad': 1})

    request.session['carrito'] = carrito   
    
    return redirect('carrito')


def carrito(request):
    lista_productos_carrito = request.session.get('carrito', [])
    formulario=DeliveryForm()
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
        'formulario':formulario
    }
    return render(request, 'aplicacion/carrito.html', context)


def crear_pedido(request):
    if request.method == "POST":
        lista_productos_carrito = request.session.get('carrito', [])
        usuario = request.user

        for item in lista_productos_carrito:
            producto = Producto.objects.get(id_producto=item['id_producto'])
            cantidad = item['cantidad']
            precio_total = producto.valor * cantidad

            Pedido.objects.create(
                precio_total=precio_total,
                fecha_pedido=timezone.now(),
                estado='Pendiente', 
                cantidad=cantidad,
                usuario=usuario
            )

        # Limpia el carrito después de crear el pedido
        request.session['carrito'] = []

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

def Delivery_Guardar(request):
    if request.method == "POST":
        formulario = DeliveryForm(request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Datos guardados")
            return redirect('carrito')
        else:
            messages.error(request,"Error al guardar tus datos")
            return redirect('carrito')
    

def admin(request):
    delivery=Delivery.objects.all()
    comanda=Comanda.objects.all()
    cant_prod=CantidadProducto.objects.all()
    datos={
        "delivery":delivery,
        "cant_prod":cant_prod,
        "comanda":comanda,
    }
    
    # Renderizar el template 'admin_usuario.html' con los datos
    return render(request, 'aplicacion/admin_usuario.html', datos)


def gestion_usuario(request):
    # Obtener todos los usuarios y sus entregas asociadas
    usuarios = Usuario.objects.all()

    # Crear una lista para almacenar los detalles de entrega de cada usuario
    detalles_entrega = []
    for usuario in usuarios:
        # Obtener las entregas asociadas a cada usuario
        entregas_usuario = Delivery.objects.filter(propietario=usuario)
        detalles_entrega.append({
            'usuario': usuario,
            'entregas': entregas_usuario,
        })

    datos = {
        "detalles_entrega": detalles_entrega,
    }
    
    return render(request, 'aplicacion/gestion_usuarios.html', datos)


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


@login_required
def user_profile(request):
    return render(request, 'user_profile.html', {'user': request.user})


def custom_logout(request):
    logout(request)
    return redirect('index')



@login_required
def Delivery_Guardar(request):
    if request.method == "POST":
        formulario = DeliveryForm(request.POST, files=request.FILES)
        if formulario.is_valid():
            delivery_data = formulario.cleaned_data
            request.session['delivery_data'] = delivery_data
            print(delivery_data)
            messages.success(request, "Datos de entrega guardados.")
            return redirect('carrito')
        else:
            messages.error(request, "Error al guardar los datos de entrega.")
            return redirect('carrito')
        
@login_required
def crear_pedido(request):
    if request.method == "POST":
        lista_productos_carrito = request.session.get('carrito', [])

        if not lista_productos_carrito:
            messages.error(request, "No hay productos en el carrito para procesar el pedido.")
            return redirect('carrito')

        usuario = request.user
        delivery_data = request.session.get('delivery_data', None)

        if not delivery_data:
            messages.error(request, "Debe proporcionar los datos de entrega antes de pagar.")
            return redirect('carrito')

        # Crear el objeto Delivery
        delivery = Delivery.objects.create(
            direccion=delivery_data['direccion'],
            telefono=delivery_data['telefono'],
            referencia=delivery_data.get('referencia', ''),
            comentario=delivery_data.get('comentario', ''),
            propietario=usuario.perfil 
        )

        for item in lista_productos_carrito:
            producto = Producto.objects.get(id_producto=item['id_producto'])
            cantidad = item['cantidad']
            precio_total = producto.valor * cantidad

            # Crear el objeto CantidadProducto
            cantidad_producto = CantidadProducto.objects.create(
                cant_producto=cantidad,
                producto=producto
            )

            # Crear el objeto Pedido y asignar el objeto Delivery
            pedido = Pedido.objects.create(
                precio_total=precio_total,
                fecha_pedido=timezone.now(),
                estado='Pendiente',
                usuario=usuario,
                Cantidad=cantidad_producto,
                delivery=delivery  # Asigna el objeto Delivery creado
            )

            # Crear el objeto Comanda
            Comanda.objects.create(
                fecha_emision=timezone.now(),
                pedido=pedido,
                direccion=delivery
            )

        # Limpiar el carrito y los datos de entrega en la sesión
        request.session['carrito'] = []
        request.session['delivery_data'] = None

        messages.success(request, "Pedido creado exitosamente.")
        return redirect('index')

    return redirect('carrito')


def terminar_comanda(request, comanda_id):
    comanda = get_object_or_404(Comanda, id_comanda=comanda_id)
    comanda.terminada = True  # Marca la comanda como terminada
    comanda.save()
    
    # Redirige de vuelta a la página de administración
    return redirect('admins')



def bloquear_usuario(request, rut):
    usuario = Usuario.objects.get(rut=rut)

    if usuario.bloqueado:
        usuario.bloqueado = False
    else:
        usuario.bloqueado = True

    usuario.save()  

    return redirect('Usuarios')