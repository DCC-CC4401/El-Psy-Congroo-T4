from django import forms

from .models import Usuario, Comida
from django import forms

class LoginForm(forms.Form):
   user = forms.CharField(max_length = 100)
   password = forms.CharField(widget = forms.PasswordInput())

class GestionProductosForm(forms.Form):
    idVendedor = 0
    nombre = forms.CharField(max_length=200)
    categoria = forms.IntegerField()
    descripcion = forms.CharField(max_length=500)
    stock = forms.IntegerField()
    precio = forms.IntegerField()

