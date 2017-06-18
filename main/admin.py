from django.contrib import admin

from .models import *

admin.site.register(Usuario)
admin.site.register(Vendedor)
admin.site.register(FormasDePago)
admin.site.register(Comida)
admin.site.register(Transacciones)