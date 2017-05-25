from django.db import models
from multiselectfield import MultiSelectField

# Create your models here

class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    tipos = ((0, 'admin'), (1, 'alumno'), (2, 'fijo'), (3, 'ambulante'))
    tipo = models.IntegerField(choices=tipos)
    avatar = models.CharField(max_length=200)
    contraseña = models.CharField(max_length=200)
    activo = models.BooleanField(blank=True);
    litaFormasDePago = (
        (0, 'Tarjeta'),
        (1, 'Efectivo'),
    )
    formasDePago = MultiSelectField(choices=litaFormasDePago,blank=True)
    horario = models.CharField(max_length=200,blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'usuario'




class Comida(models.Model):
    idVendedor = models.IntegerField(default=0);
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
    descripcion = models.CharField(max_length=500)
    stock = models.PositiveSmallIntegerField(default=0)
    precio = models.PositiveSmallIntegerField(default=0)
<<<<<<< HEAD

=======
    imagen = models.CharField(max_length=300)
>>>>>>> cc4d7ac03fced100649cdc4a315d29a4b3412b3f
    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'Comida'


