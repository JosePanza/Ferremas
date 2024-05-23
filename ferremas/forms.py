from django.forms import ModelForm
from django import forms
from .models import Usuario

class usuariosform(forms.ModelForm):
    class Meta:
        model = Usuario
        #fields = ['user,'ID_usuario', 'nombre_usuario', 'descripcion', 'img'] 
   
        fields = '__all__' 




