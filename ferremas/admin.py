from django.contrib import admin
from .models import Productos

# Register your models here.

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id_producto', 'nombre', 'precio')  

admin.site.register(Productos, ProductoAdmin)