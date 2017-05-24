from django.contrib import admin

from .models import UsuarioAlumno
from .models import UsuarioAdmin
from .models import UsuarioVFijo
from .models import UsuarioVAmbulante
from .models import Comida

admin.site.register(UsuarioAlumno)
admin.site.register(UsuarioAdmin)
admin.site.register(UsuarioVFijo)
admin.site.register(UsuarioVAmbulante)
admin.site.register(Comida)