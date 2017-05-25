from django import forms

from .models import Usuario, Comida
from django import forms

class LoginForm(forms.Form):
   user = forms.CharField(max_length = 100)
   password = forms.CharField(widget = forms.PasswordInput())

class GestionProductosForm(forms.ModelForm):

    class Meta:
        model = Comida
        fields = ('idVendedor','nombre','categorias','descripcion','stock','precio','imagen')