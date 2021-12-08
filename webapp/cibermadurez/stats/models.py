from django.db import models

# Create your models here.
class Stat(models.Model):
    componente = models.CharField(max_length=50)
    funcion = models.CharField(max_length=50)
    fecha = models.CharField(max_length=10)
    hora = models.CharField(max_length=10)

    def __str__(self):
        return (self.componente, self.funcion, self.fecha, self.hora) 