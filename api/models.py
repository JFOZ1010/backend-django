from django.db import models


# Create your models here.

#se creara el modelo de usuario, que cuenta con los atrivbutos: idUsuario, correoUsr, admin (booleano), y una contraseña. 
class Usuario(models.Model):
    idUsuario = models.AutoField(primary_key=True) #AutoField, es un campo que se autoincrementa, es decir, que se le asigna un valor automaticamente, en este caso, el idUsuario.
    correoUsr = models.CharField(max_length=70)
    admin = models.BooleanField(default=False)
    contrasena = models.CharField(max_length=50)
    #fechaNacimiento = models.models.DateTimeField(_("fechaNacimiento"), auto_now=False, auto_now_add=False)


class Asociado(Usuario): 
    #documentoAsociado = models.models.IntegerField(_("DocumentoA"), primary_key=True, on_delete=models.CASCADE)
    #correoAsociado = models.CharField(max_length=70)
    idAsociado = models.AutoField(primary_key=True) #coloco una llave primaria de prueba
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=70)
    ciudad = models.CharField(max_length=50)
    #fechaNacimiento = models.models.DateTimeField(_("fechaNacimiento"), auto_now=False, auto_now_add=False)
    ocupacion = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50) #telefono con varchar, no necesitamos hacer nada con ese integer como telefono. 

class Cliente(Usuario):

    #documentoCliente = models.IntegerField(_("DocumentoC"), primary_key=True)
    idCliente = models.AutoField(primary_key=True) #coloco una llave primaria de prueba
    asociadoVinculado = models.ForeignKey(Asociado, on_delete=models.CASCADE)
    #correoCliente = models.CharField(max_length=70)
    nombre = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50)