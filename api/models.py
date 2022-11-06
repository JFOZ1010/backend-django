from django.db import models


# Create your models here.

#se creara el modelo de usuario, que cuenta con los atrivbutos: idUsuario, correoUsr, admin (booleano), y una contraseña. 
class Usuario(models.Model):
    idUsuario = models.AutoField(primary_key=True) #AutoField, es un campo que se autoincrementa, es decir, que se le asigna un valor automaticamente, en este caso, el idUsuario.
    correoUsr = models.CharField(max_length=70)
    admin = models.BooleanField(default=False)
    contrasena = models.CharField(max_length=50)
    #fechaNacimiento = models.models.DateTimeField(_("fechaNacimiento"), auto_now=False, auto_now_add=False)