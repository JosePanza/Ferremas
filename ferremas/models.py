from django.contrib.auth.models import User
from django.db import models

class Carrito(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    articulos = models.ManyToManyField('articulo', related_name='carritos', blank=True)

    def __str__(self):
        return f"Carrito de {self.usuario.username}"

class articulo(models.Model):
    id_articulo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=False, null=False)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre