from django import forms

from .models import UsuarioAlumno, Comida


class PostForm(forms.ModelForm):

    class Meta:
        model = UsuarioAlumno
        fields = ('id','nombre', 'email','tipo','avatar','contraseña',)

class GestionProductosForm(forms.ModelForm):

    class Meta:
        model = Comida
        fields = ('idVendedor','nombre','categorias','descripcion','stock','precio','imagen')
