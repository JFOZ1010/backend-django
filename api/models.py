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


# se creara el modelo de usuario, que cuenta con los atrivbutos: idUsuario, correoUsr, admin (booleano), y una contraseña.


class Rol(models.TextChoices):
    ADMIN = 'admin'
    CLIENTE = 'cliente'
    ASOCIADO = 'asociado'


class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fechaNacimiento = models.DateField(
        "fechaNacimiento", auto_now=False, auto_now_add=False, blank=True)
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

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return self.user.username + " " + self.rol

    @receiver(post_save, sender=User)
    def create_user_usuario(sender, instance, created, **kwargs):
        if created:
            Usuario.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_usuario(sender, instance, **kwargs):
        instance.usuario.save()


"""
Author: Juan Felipe Osorio
se creara el modelo de Asociado, que cuenta con los atributos: documentoAsociado, correoAsociado, nombre,
direccion, ciudad, fechanacimento, ocupacion, telefono.
"""


class Asociado(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
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


class Ahorro(models.Model):

    idAhorro = models.AutoField(primary_key=True)
    idAsociado = models.ForeignKey(Asociado, on_delete=models.CASCADE)
    fecha = models.DateField()
    descripcion = models.CharField(max_length=200)
    monto = models.IntegerField()
    firmaDigital = models.CharField(max_length=200)
    tipoConsignacion = models.CharField(max_length=200)

    def __str__(self):
        return self.idAhorro


class Cliente(models.Model):

    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    documentoCliente = models.CharField(max_length=10, primary_key=True)
    asociadoVinculado = models.ForeignKey(Asociado, on_delete=models.CASCADE)
    # correoCliente = models.CharField(max_length=70)
    nombre = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50)

    def __str__(self):
        return self.documentoCliente


#se creará el modelo de multa, que es un modelo en los casos en los que un usuario no cumpla con los pagos, 
#cuenta con los atributos, idMulta (primary key), idAsociado que es integer, motivo que es varchar, fecha que es date, costo que es integer, 
#estadoMulta que es booleano. 

class Multa(models.Model):

    idMulta = models.AutoField(primary_key=True)
    idAsociado = models.ForeignKey(Asociado, on_delete=models.CASCADE)
    motivo = models.CharField(max_length=200)
    fecha = models.DateField()
    costo = models.IntegerField()
    estadoMulta = models.BooleanField()

    def __str__(self):
        return self.idMulta


class CuotaManejo(models.Model): 
    idCuotaManejo = models.AutoField(primary_key=True)
    idAsociado = models.ForeignKey(Asociado, on_delete=models.CASCADE)
    fechaComienzo = models.DateField(auto_now=False, auto_now_add=False)
    fechaFin = models.DateField(auto_now=False, auto_now_add=False)
    tasaInteres = models.IntegerField()

    def __str__(self): 
        return self.idCuotaManejo



#modelo de reunion , el cual es modelo padre de
# reunion virtual y reunion presencial
class Reunion(models.Model):
    idReunion = models.AutoField(primary_key=True)
    #asociado es una llave foranea de asociado de tipo onetoone Field
    asociado = models.ForeignKey(Asociado, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now=False, auto_now_add=False)
    hora = models.CharField(max_length=30)
    motivo = models.CharField(max_length=60)    
    tipoReunion = models.CharField(max_length=10)
    asistencia = models.BooleanField(default=False)


    def __str__(self):
        return self.idReunion

class ReunionPresencial(Reunion):
    sitio = models.CharField(max_length=50)
    costo = models.IntegerField()

    def __str__(self):
        return self.idReunion

class ReunionVirtual(Reunion):
    enlace = models.CharField(max_length=50)
    costo = models.IntegerField()

    def __str__(self):
        return self.idReunion



class Prestamo(models.Model): 
    solicitudPrestamo = models.CharField(primary_key=True, max_length=30)
    #codeudor es una llave foranea de asociado 
    codeudor = models.ForeignKey(Asociado, on_delete=models.CASCADE)
    #deudor es una llave foranea de cliente
    deudor = models.ForeignKey(Cliente, on_delete=models.CASCADE)    
    monto = models.IntegerField()
    fecha = models.DateField(auto_now=False, auto_now_add=False)
    estadoPrestamo = models.BooleanField(default=False)
    interes = models.FloatField()
    comision = models.IntegerField()

    def checkErrors(self): 
        return self.montoValido() == [] 

    def montoValido(self):
        #array para almacenar los errores
        errors = []
        if self.monto > 0:
            return errors.append("Monto valido")
        else:
            return errors.append("Monto no valido")

    def __str__(self):
        return self.solicitudPrestamo + " a: " + self.deudor



class Abono(models.Model):
    idAbono = models.AutoField(primary_key=True)
    idPrestamo = models.ForeignKey(Prestamo, on_delete=models.CASCADE)
    monto = models.IntegerField()
    fecha = models.DateField()
    descripcion = models.CharField(max_length=200)

    def __str__(self): 
        return self.idAbono 


