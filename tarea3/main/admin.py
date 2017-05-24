from django.contrib import admin

from .models import UsuarioAlumno
from .models import UsuarioAdmin
from .models import Comida

admin.site.register(UsuarioAlumno)
admin.site.register(UsuarioAdmin)
admin.site.register(Comida)