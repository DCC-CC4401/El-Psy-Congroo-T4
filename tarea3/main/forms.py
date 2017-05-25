from django import forms

<<<<<<< HEAD
=======
from .models import UsuarioAlumno, Comida

>>>>>>> cc4d7ac03fced100649cdc4a315d29a4b3412b3f


<<<<<<< HEAD
from django import forms

class LoginForm(forms.Form):
   user = forms.CharField(max_length = 100)
   password = forms.CharField(widget = forms.PasswordInput())

=======
    class Meta:
        model = UsuarioAlumno
        fields = ('id','nombre', 'email','tipo','avatar','contraseña',)

class GestionProductosForm(forms.ModelForm):

    class Meta:
        model = Comida
        fields = ('idVendedor','nombre','categorias','descripcion','stock','precio','imagen')
>>>>>>> cc4d7ac03fced100649cdc4a315d29a4b3412b3f
