import re
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


class Asociado(models.Model):
    documentoA = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    nombre = models.CharField("nombre", max_length=100)
    apellidos = models.CharField("dpellidos", max_length=200)
    direccion = models.models.CharField("direccion", max_length=100)
    ciudad = models.CharField("ciudad", max_length=100)
    fechaNacimiento = models.DateField("fechaNacimiento")
    ocupacion = models.CharField("ocupacion", max_length=300)
    telefono = models.PositiveIntegerField("telefono", max_length=10)

    def checkData(self):
        return self.getErrors() = []

    def getErrors(self):
        errors = []
        if len(self.documentoA.password) < 8:
            errors.append("Contraseña muy corta")
        if not re.fullmatch(regex, self.documentoA.username):
            errors.append("Email invalido")

    def __str__(self):
        return self.documentoA.username

    @@receiver(post_save, sender=Model)
    def _post_save_receiver(sender, **kwargs):
