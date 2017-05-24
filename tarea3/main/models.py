from django.db import models
from multiselectfield import MultiSelectField

# Create your models here

class UsuarioAlumno(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    tipo = models.IntegerField(default=1, editable=False)
    avatar = models.CharField(max_length=200)
    contraseña = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

class UsuarioAdmin(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    tipo = models.IntegerField(default=0, editable=False)
    avatar = models.CharField(max_length=200)
    contraseña = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

class Comida(models.Model):
    nombre = models.CharField(max_length=200,primary_key=True)
    listaCategorias = (
        (0, 'Cerdo'),
        (1, 'Chino'),
        (2, 'Completos'),
        (3, 'Egipcio'),
        (4, 'Empanadas'),
        (5, 'Ensalada'),
        (6, 'Japones'),
        (7, 'Pan'),
        (8, 'Papas fritas'),
        (9, 'Pasta'),
        (10, 'Pescado'),
        (11, 'Pollo'),
        (12, 'Postres'),
        (13, 'Sushi'),
        (14, 'Vacuno'),
        (15, 'Vegano'),
        (16, 'Vegetariano'),
    )
    categorias = MultiSelectField(choices=listaCategorias)
    descriptcion = models.CharField(max_length=500)
    stock = models.PositiveSmallIntegerField(default=0)
    precio = models.PositiveSmallIntegerField(default=0)
    def __str__(self):
        return self.nombre


