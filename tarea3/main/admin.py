from django.contrib import admin

from .models import Usuario
from .models import Comida

admin.site.register(Usuario)
admin.site.register(Comida)