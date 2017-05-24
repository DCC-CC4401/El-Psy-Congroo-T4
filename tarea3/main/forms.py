from django import forms

from .models import UsuarioAlumno

class PostForm(forms.ModelForm):

    class Meta:
        model = UsuarioAlumno
        fields = ('id','nombre', 'email','tipo','avatar','contraseña',)