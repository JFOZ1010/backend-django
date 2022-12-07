from django.contrib import admin

# Register your models here.
from django.contrib import admin
from api.models import Usuario, Cliente, Asociado, Ahorro, Prestamo

# Register your models here.

# Registramos las tablas que se crearon en los modelos
admin.site.register(Usuario)
admin.site.register(Cliente)
admin.site.register(Asociado)
admin.site.register(Ahorro)
admin.site.register(Prestamo)
