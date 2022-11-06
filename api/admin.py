from django.contrib import admin
from .models import Usuario, Cliente, Asociado
# Register your models here.

#Registramos las tablas que se crearon en los modelos
admin.site.register(Usuario)
admin.site.register(Cliente)
admin.site.register(Asociado)
