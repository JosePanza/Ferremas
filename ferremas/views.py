from django.contrib import messages
from django.contrib.auth import login as auth_login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .models import Productos
from django.http import JsonResponse,HttpResponse
from .forms import ProductosForm





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
    carrito = request.session.get('carrito', {})
    if not isinstance(carrito, dict):
        carrito = {}

    # Filtrar claves válidas y convertir a enteros
    claves_validas = [int(key) for key in carrito.keys() if key.isdigit()]

    productos = Productos.objects.filter(id_producto__in=claves_validas)
    cantidades = {int(k): v for k, v in carrito.items() if k.isdigit()}
    total = sum(producto.precio * cantidades[producto.id_producto] for producto in productos)

    return render(request, 'Carrito.html', {
        'productos': productos,
        'cantidades': cantidades,
        'total': total,
    })

def vaciar_carrito(request):
    if 'carrito' in request.session:
        del request.session['carrito']
    return redirect('mostrar_carrito')

def agregar_al_carrito(request):
    if request.method == "POST":
        id_producto = request.POST.get('id_producto')
        print(f"Producto ID recibido: {id_producto}")
        
        if not id_producto:
            messages.error(request, "No se pudo añadir el producto al carrito. ID del producto no recibido.")
            return redirect('Pintura')
        
        carrito = request.session.get('carrito', {})
        total_productos = sum(carrito.values())
        print(f"Total de productos antes de añadir: {total_productos}")
        print(f"Contenido del carrito antes de añadir: {carrito}")

        if total_productos < 10:
            if id_producto in carrito:
                carrito[id_producto] += 1
            else:
                carrito[id_producto] = 1
            request.session['carrito'] = carrito
            messages.success(request, "Producto añadido al carrito.")
        else:
            messages.error(request, "No puedes añadir más de 10 productos en una sola compra.")
        
        print(f"Contenido del carrito después de añadir: {carrito}")
        
    return redirect('Pintura')