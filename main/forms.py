from django import forms

from main.models import *


class Formulario_Registro(forms.Form):
    tipo_cuenta = forms.ChoiceField(label='Tipo de Usuario',
                                    choices=[(1, "Alumno"), (2, "Vendedor Fijo"), (3, "Vendedor Ambulante")])
    tipo = forms.ChoiceField(required=False)
    nombre = forms.CharField(label='Ingresa tu nombre')
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput)
    contrasena = forms.CharField(label='Ingresa tu contraseña', widget=forms.PasswordInput)
    chequeo_contrasena = forms.CharField(label='Repite tu contraseña', widget=forms.PasswordInput)

    hora_inicio = forms.TimeField(label='Hora de apertura', widget=forms.TimeInput(), required=False, initial='8:00')
    hora_fin = forms.TimeField(label='Hora de cierre', widget=forms.TimeInput(), required=False, initial='18:00')

    latitud = forms.DecimalField(decimal_places=40, max_digits=42, widget=forms.HiddenInput(), initial='-33.457785')
    longitud = forms.DecimalField(decimal_places=40, max_digits=42, widget=forms.HiddenInput(), initial='-70.663808')

    pagos = forms.ModelMultipleChoiceField(queryset=FormasDePago.objects.all(), widget=forms.SelectMultiple(),
                                           required=False, initial=FormasDePago.objects.none())

    def limpiar_contrasena(self):
        if 'contrasena' in self.cleaned_data:
            contrasena = self.cleaned_data['password']
            chequeo_contrasena = self.cleaned_data['password_check']
            if contrasena == chequeo_contrasena:
                return chequeo_contrasena
        raise forms.ValidationError('Las contraseñas no coinciden')

    class Meta:
        model = Usuario
        fields = ('tipo', 'nombre', 'avatar')


class Formulario_Ingreso(forms.Form):
    correo = forms.EmailField(label='Ingresa tu e-mail', widget=forms.EmailInput)
    contrasena = forms.CharField(label='Ingresa tu contraseña', widget=forms.PasswordInput())

class Formulario_Actualizar_Perfil(forms.Form):
    nombre =  forms.CharField(label='Editar nombre')
    email = forms.EmailField(label='Ingresa tu e-mail', widget=forms.EmailInput)
    avatar = forms.ImageField(label='Avatar', widget=forms.FileInput, required=False, initial=None)
    contrasena = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    pagos = forms.ModelMultipleChoiceField(queryset=FormasDePago.objects.all(), required=False,
                                           initial=FormasDePago.objects.none())
    hora_inicio = forms.TimeField(label='Hora de apertura', widget=forms.TimeInput(), required=False)
    hora_fin = forms.TimeField(label='Hora de cierre', widget=forms.TimeInput(), required=False)

    latitud = forms.DecimalField(decimal_places=40, max_digits=42, widget=forms.HiddenInput(), initial='-33.457785')
    longitud = forms.DecimalField(decimal_places=40, max_digits=42, widget=forms.HiddenInput(), initial='-70.663808')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        if self.user is not None:
            inicial = 0
            final = 0
            if self.user.usuario.tipo == 2:
                inicial = Vendedor.objects.values_list('horario_inicio', flat=True).get(nombre=self.user.username)
                final = Vendedor.objects.values_list('horario_fin', flat=True).get(nombre=self.user.username)

            kwargs.update(initial={'email': self.user.email,
                                   'hora_inicio': inicial,
                                   'hora_fin': final})
        super(Formulario_Actualizar_Perfil, self).__init__(*args, **kwargs)

    class Meta:
        model = Usuario
        exclude = ('username', 'date_joined')


# class Formulario_Gestion_Producto(forms.Form):
#     idVendedor = 0
#     nombre = forms.CharField(max_length=200)
#     categorias = forms.IntegerField()
#     descripcion = forms.CharField(max_length=500)
#     stock = forms.IntegerField()
#     precio = forms.IntegerField()


class Formulario_Producto(forms.ModelForm):
    imagen = forms.ImageField(label='Imagen', widget=forms.FileInput, required=False, initial=None)
    class Meta:
        model = Comida
        fields = ('nombre', 'precio', 'stock', 'categorias', 'descripcion')
