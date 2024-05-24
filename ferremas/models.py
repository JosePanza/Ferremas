from django.db import models
from django.contrib.auth.models import User

class Productos(models.Model):
    id_producto = models.AutoField(primary_key= True)
    nombre = models.CharField(max_length=100, blank=False, null=False)
    descripcion = models.CharField(max_length=100, blank=False, null=False)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    # Otros campos según sea necesario

    def __str__(self):
        return self.nombre
