import re

from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

# from django.core.exceptions import ValidationError
# from django.utils import timezone

# Create your models here.

# metodo global, que valide que el correo sea valido
'''
def validate_email(email):
    if not re.match(r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$", email):
        raise ValidationError("Invalid email")

    return email
#metodo global, para validar que el documento sea valido
def validate_document(document):
    if not re.match(r"^[0-9]{8,10}$", document):
        raise ValidationError("Invalid document")

    return document
#metodo global, para validar la fecha de nacimiento
def validate_date(birthdate):
    if birthdate > timezone.now().date():
        raise ValidationError("Invalid birthdate")

    return birthdate
'''

# se creara el modelo de usuario, que cuenta con los atrivbutos: idUsuario, correoUsr, admin (booleano), y una contraseña.


class Rol(models.TextChoices):
    ADMIN = 'admin'
    CLIENTE = 'cliente'
    ASOCIADO = 'asociado'


class Usuario(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE)
    fechaNacimiento = models.DateField(
        ("fechaNacimiento"), auto_now=False, auto_now_add=False, blank=True)
    rol = models.CharField(max_length=20, choices=Rol.choices, blank=True)

    def checkData(self):
        return self.getErrors() == []

    def getErrors(self):
        errors = []
        if self.rol not in Rol.values:
            errors.append("Rol inexistente")
        if len(self.user.password) < 8:
            errors.append("Password no permitida")
        if not re.fullmatch(regex, self.user.username):
            errors.append("Email invalido")
        return errors

    def __str__(self):
        return self.user.username + " " + self.rol

    @receiver(post_save, sender=User)
    def create_user_usuario(sender, instance, created, **kwargs):
        if created:
            Usuario.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_Usuario(sender, instance, **kwargs):
        instance.usuario.save()


"""
Author: Juan Felipe Osorio
se creara el modelo de Asociado, que cuenta con los atributos: documentoAsociado, correoAsociado, nombre,
direccion, ciudad, fechanacimento, ocupacion, telefono.
"""


class Asociado(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, blank=True)
    # correoAsociado = models.CharField(max_length=70)
    documentoAsociado = models.CharField(max_length=10, primary_key=True)
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=70)
    ciudad = models.CharField(max_length=50)
    # fechaNacimiento = models.models.DateTimeField(_("fechaNacimiento"), auto_now=False, auto_now_add=False)
    ocupacion = models.CharField(max_length=50)
    # telefono con varchar, no necesitamos hacer nada con ese integer como telefono.
    telefono = models.CharField(max_length=50)
    '''
    def clean(self):
        #self.correoAsociado = validate_email(self.correoAsociado)
        self.documentoAsociado = validate_document(self.documentoAsociado)
        #self.fechaNacimiento = validate_date(self.fechaNacimiento)

    '''

    def __str__(self):
        return self.documentoAsociado


class Cliente(models.Model):

    usuario = models.OneToOneField(
        Usuario, on_delete=models.CASCADE)
    documentoCliente = models.CharField(max_length=10, primary_key=True)
    asociadoVinculado = models.ForeignKey(Asociado, on_delete=models.CASCADE)
    # correoCliente = models.CharField(max_length=70)
    nombre = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50)
    '''
    def clean(self):
        #self.correoCliente = validate_email(self.correoCliente)
        self.documentoCliente = validate_document(self.documentoCliente)
    '''

    def __str__(self):
        return self.documentoCliente
