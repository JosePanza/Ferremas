from django.contrib import messages
from django.contrib.auth import login as auth_login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .models import Producto
from django.http import JsonResponse,HttpResponse
from .forms import ProductoForm



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
    


def Carrito_views(request):
    if request.method == 'POST':
        producto_id = request.POST.get('producto_id')
        if producto_id:
            if 'carrito' not in request.session:
                request.session['carrito'] = []
            request.session['carrito'].append(producto_id)
            request.session.modified = True
        return redirect('Carrito')
    else:
        # Si la solicitud no es POST, simplemente renderiza la página del carrito con los productos actuales
        productos = Producto.objects.all()
        return render(request, 'Carrito.html', {'productos': productos})

def agregar_al_carrito(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Producto agregado exitosamente'})
    else:
        form = ProductoForm()
    return JsonResponse({'error': 'Error al procesar la solicitud'}, status=400)