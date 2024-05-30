from django.contrib import admin
from .models import articulo

# Register your models here.

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id_articulo', 'nombre', 'precio')  

admin.site.register(articulo, ProductoAdmin)