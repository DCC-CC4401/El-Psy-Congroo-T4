from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.formats import get_format

from main.choices import *

# Create your models here


class Usuario(models.Model):
    usuario = models.OneToOneField(User, verbose_name='Usuario', related_name='usuario')
    nombre = models.CharField(max_length=200)
    tipo = models.IntegerField(default=1, choices=TiposUsuarios)
    avatar = models.ImageField(upload_to='avatars')

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'


class Vendedor(models.Model):
    nombre = models.CharField(max_length=200)
    avatar = models.ImageField(upload_to='avatars')
    activo = models.BooleanField(default=False)
    formasDePago = models.ManyToManyField('FormasDePago', related_name='formasDePago')
    horarioIni = models.CharField(max_length=200, blank=True, null=True)
    horarioFin = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Vendedor'
        verbose_name_plural = 'Vendedores'


class FormasDePago(models.Model):
    forma = models.CharField(max_length=200)

    def __str__(self):
        return self.forma

    class Meta:
        verbose_name = 'Formas de pago'
        verbose_name_plural = 'Formas de pago'


class Comida(models.Model):
    nombre = models.CharField(max_length=200, primary_key=True)
    categorias = models.IntegerField(default=0, choices=Categorias)
    descripcion = models.CharField(max_length=500)
    stock = models.PositiveSmallIntegerField(default=0)
    precio = models.PositiveSmallIntegerField(default=0)
    imagen = models.ImageField(upload_to="productos")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Comida'
        verbose_name_plural = 'Comida'


class Favoritos(models.Model):
    idAlumno = models.IntegerField()
    idVendedor = models.IntegerField()

    def __str__(self):
        return self.idAlumno

    class Meta:
        verbose_name = 'Favorito'
        verbose_name_plural = 'Favoritos'


class Transacciones(models.Model):
    my_formats = get_format('DATETIME_INPUT_FORMATS')
    nombreComida = models.CharField(max_length=200, blank=True, null=True)
    idVendedor = models.ForeignKey('Usuario', related_name='vendedor')
    precio = models.IntegerField()
    fechaAhora = str(timezone.now()).split(' ', 1)[0]
    fecha = models.CharField(max_length=200, default=fechaAhora)

    def __str__(self):
        return str(self.nombreComida + ' ' + self.idVendedor.nombre)

    class Meta:
        verbose_name = 'Transaccion'
        verbose_name_plural = 'Transacciones'
