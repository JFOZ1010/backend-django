from django.contrib import admin
from .models import Usuario
# Register your models here.

#Registramos las tablas que se crearon en los modelos
admin.site.register(Usuario)