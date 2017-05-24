from django.db import models

# Create your models here

class Usuario(models.Model):
    nombre = models.CharField(max_length=200,primary_key=True)
    email = models.CharField(max_length=200)
    tipos = ((0,'admin'),(1,'alumno'),(2,'fijo'),(3,'ambulante'))
    tipo = models.IntegerField(choices=tipos)
    contraseña = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre