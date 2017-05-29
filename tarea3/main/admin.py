from django.contrib import admin

from .models import Usuario
from .models import Comida
from .models import Imagen

admin.site.register(Usuario)
admin.site.register(Comida)
admin.site.register(Imagen)