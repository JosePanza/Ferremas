from django.contrib import messages
from django.contrib.auth import login as auth_login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .models import articulo, Carrito
from django.http import JsonResponse,HttpResponse
from .forms import ProductosForm
from transbank.webpay.webpay_plus.transaction import Transaction, WebpayOptions
import hashlib
from django.conf import settings
from transbank.common.integration_type import IntegrationType
from django.urls import reverse




@login_required
def profile_view(request):
    user = request.user
    context = {'user': user}
    return render(request, 'profile.html', context)

def Productos_view(request):
    return render(request, 'Productos.html')

def Pintura_view(request):
    return render(request, 'Pintura.html')

def Seguridad_view(request):
    return render(request, 'Seguridad.html')

def inicio(request):
    return render(request, 'inicio.html')

def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html', {'form': AuthenticationForm()})
    elif request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('inicio')
        return render(request, 'login.html', {'form': form, 'error': 'Nombre de usuario o contraseña incorrectos'})

def registro_view(request):
    if request.method == 'GET':
        return render(request, 'registro.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1']
                )
                user.save()
                auth_login(request, user)  # Autenticar al usuario después de registrarse
                messages.success(request, '¡Te has registrado correctamente!')
                return redirect('inicio')
            except IntegrityError:
                return render(request, 'registro.html', {
                    'form': UserCreationForm(),
                    'error': 'El usuario ya existe'
                })
        return render(request, 'registro.html', {
            'form': UserCreationForm(),
            'error': 'Las contraseñas no coinciden'
        })

def logout_view(request):
    logout(request)
    return redirect('inicio')
    


def mostrar_carrito(request):
    articulos = articulo.objects.all()  # Obtienes todos los artículos, ajusta según tu lógica de negocio.
    total = sum(float(articulo.precio) for articulo in articulos)  # Calcula el total.
    print("Artículos:", articulos)
    print("Total:", total)
    return render(request, 'Carrito.html', {'articulos': articulos, 'total': total})



def vaciar_carrito(request):
    if request.method == "POST":
        # Elimina todos los artículos del carrito
        articulo.objects.all().delete()

        # Redirecciona al usuario a donde desees
        return redirect(request.META.get('HTTP_REFERER', 'Productos'))

    # Maneja el caso si la solicitud no es POST
    # (puedes agregar más lógica aquí si es necesario)
    return redirect('Productos')


@login_required
def agregar_al_carrito(request):
    if request.method == "POST":
        nombre = request.POST.get('nombre')
        precio = request.POST.get('precio')

        # Obtener o crear el carrito del usuario
        carrito, creado = Carrito.objects.get_or_create(usuario=request.user)

        # Crear un nuevo artículo
        nuevo_articulo = articulo(nombre=nombre, precio=precio)

        # Guardar el nuevo artículo en la base de datos
        nuevo_articulo.save()

        # Agregar el artículo al carrito del usuario
        carrito.articulos.add(nuevo_articulo)

        # Redireccionar al usuario a donde desees
        return redirect(request.META.get('HTTP_REFERER', 'Productos'))

    # Maneja el caso si la solicitud no es POST
    # (puedes agregar más lógica aquí si es necesario)
    return redirect('Productos')

def iniciar_pago(request):
    if request.method == "POST":
        # Obtener el carrito del usuario actual
        carrito, creado = Carrito.objects.get_or_create(usuario=request.user)

        # Obtener los productos en el carrito
        productos = carrito.articulos.all()
        
        # Calcular el total
        total = sum(producto.precio for producto in productos)
        
        if total > 0:
            session_key = request.session.session_key
            buy_order = hashlib.md5(session_key.encode()).hexdigest()[:26]
            session_id = f"sesion_{session_key}"
            amount = total
            return_url = request.build_absolute_uri(reverse('confirmar_pago'))

            tx = Transaction(WebpayOptions(settings.TRANBANK_COMMERCE_CODE, settings.TRANBANK_API_KEY, IntegrationType.TEST))
            try:
                response = tx.create(buy_order, session_id, amount, return_url)
                if response:
                    return redirect(response['url'] + "?token_ws=" + response['token'])
                else:
                    return HttpResponse("No se recibió respuesta de Transbank.")
            except Exception as e:
                return HttpResponse(f"Error interno: {str(e)}")
        else:
            return HttpResponse("El carrito está vacío.")
    else:
        return HttpResponse("Método no permitido.", status=405)
    
    
def confirmar_pago(request):
    token_ws = request.GET.get('token_ws')
    if not token_ws:
        return HttpResponse("Token no proporcionado.")

    try:
        tx = Transaction(WebpayOptions(settings.TRANBANK_COMMERCE_CODE, settings.TRANBANK_API_KEY, IntegrationType.TEST))
        response = tx.commit(token_ws)
        if response and response['status'] == 'AUTHORIZED':

            # Obtener el carrito de la sesión
            carrito = request.session.get('carrito', {})
            
            for producto_id, cantidad in carrito.items():
                producto = articulo.objects.get(id_articulo=producto_id)
                print(f"Producto: {producto.nombre}, Cantidad: {cantidad}")
            
         

            return render(request, 'confirmacion_pago.html', {'response': response})
        else:
            return HttpResponse("No se recibió respuesta de Transbank.")
    except Exception as e:
        return HttpResponse(f"Error interno: {str(e)}")

