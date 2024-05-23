from .models import  Doctor, Usuario
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse



@login_required
def profile_view(request):
   
    user = request.user
    
   
    
    context = {
        'user': user,
        
    }
    
    return render(request, 'profile.html', context)


def Productos_view(request):
    return render(request, 'Productos.html')

def Pintura_view(request):
    return render(request, 'Pintura.html')

def Seguridad_view(request):
    return render(request, 'Seguridad.html')


def patient_list(request, patient_id):
    patient = patient.objects.all()
    return render(request, 'patient_list.html', {'patient': patient})

def inicio(request):
    return render(request, 'inicio.html')

def login (request):
    return render(request, "login.html")

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
        # Si la autenticación falla, redirigir al usuario a la página de inicio de sesión con un mensaje de error.
        return render(request, 'login.html', {'form': form, 'error': 'Nombre de usuario o contraseña incorrectos'})
def registro_view(request):
    if request.method == 'GET':
        return render(request, 'registro.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
                try:
                    user = User.objects.create_user(
                    username=request.POST['username'],
                    password =request.POST['password1'])
                    user.save()
                    login(request)
                    return redirect('inicio')
                except IntegrityError:
                    return render(request, 'registro.html', {
                    'form': UserCreationForm,
                    "error" : 'Usuario ya existe'
                })
            
        return render(request, 'registro.html', {
                    'form': UserCreationForm,
                    "error" : 'La contraseña no coincide'
                })
def logout_view(request):
    logout(request)
    return redirect('inicio')

#test
def forms(request):
    if request.method == 'POST':
        formulario = usuariosform(request.POST, request.FILES)
        if formulario.is_valid():
            formulario.save()  # Guarda el usuario en la base de datos
            messages.success(request, '¡Usuario creado exitosamente!')
            return redirect('inicio')  # Reemplaza 'exito' con el nombre de la URL de tu página de éxito
    else:
        formulario = usuariosform()
        messages.success(request,'cita no creada, 1')
    
    return render(request, 'form.html', {'formulario': formulario})

def cita_list(request):
 
    usuarios = Usuario.objects.all()
    print(usuarios)
    return render(request, 'cita_list.html', {'usuarios': usuarios})




    







    
    


