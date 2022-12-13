from django.contrib import admin

# Register your models here.
from django.contrib import admin
from api.models import User, Prestamo, Ahorro, Abono

# Register your models here.

# Registramos las tablas que se crearon en los modelos
admin.site.register(User)
admin.site.register(Ahorro)
admin.site.register(Prestamo)
admin.site.register(Abono)
