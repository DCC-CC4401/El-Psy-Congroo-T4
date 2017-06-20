from django import forms

from main.models import Usuario


class SignUpForm(forms.Form):
    account_type = forms.ChoiceField(label='Tipo de Usuario',
                                     choices=[(1, "Alumno"), (2, "Vendedor Ambulante"), (3, "Vendedor Fijo")])
    fullname = forms.CharField(label='Ingresa tu nombre')
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput)
    password = forms.CharField(label='Ingresa tu contraseña', widget=forms.PasswordInput)
    password_check = forms.CharField(label='Repite tu contraseña', widget=forms.PasswordInput)

    opening_time = forms.TimeField(label='Hora de apertura', widget=forms.TimeInput(), required=False, initial='8:00')
    closing_time = forms.TimeField(label='Hora de cierre', widget=forms.TimeInput(), required=False, initial='18:00')

    # falta agregar pagos

    def clean_password_check(self):
        if 'password' in self.cleaned_data:
            password = self.cleaned_data['password']
            password_check = self.cleaned_data['password_check']
            if password == password_check:
                return password_check
        raise forms.ValidationError('Las contraseñas no coinciden')

    # cambiar a inglés?
    class Meta:
        model = Usuario
        fields = ('tipo', 'nombre')


class LoginForm(forms.Form):
    email = forms.EmailField(label='Ingresa tu e-mail', widget=forms.EmailInput)
    password = forms.CharField(label='Ingresa tu contraseña', widget=forms.PasswordInput())


class ProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField(label='Ingresa tu e-mail', widget=forms.EmailInput)
    # pagos
    opening_time = forms.TimeField(label='Hora de apertura', widget=forms.TimeInput(), required=False)
    closing_time = forms.TimeField(label='Hora de cierre', widget=forms.TimeInput(), required=False)
    # avatar
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)


class GestionProductosForm(forms.Form):
    idVendedor = 0
    nombre = forms.CharField(max_length=200)
    categoria = forms.IntegerField()
    descripcion = forms.CharField(max_length=500)
    stock = forms.IntegerField()
    precio = forms.IntegerField()


class editarProductosForm(forms.Form):
    foto = forms.FileField()
