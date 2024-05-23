from django.db import models
from django.contrib.auth.models import User

class Productos(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    # Otros campos según sea necesario

    def __str__(self):
        return self.nombre
