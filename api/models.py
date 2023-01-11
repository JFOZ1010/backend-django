from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now
from django.core.validators import MinValueValidator
from datetime import date


class Rol(models.TextChoices):
    ADMIN = 'admin'
    CLIENTE = 'cliente'
    ASOCIADO = 'asociado'


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser has to have is_staff being True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser has to have is_superuser being True")

        return self.create_user(email=email, password=password, **extra_fields)


class User(AbstractUser):
    email = models.CharField(
        max_length=80, unique=True)
    username = models.CharField(max_length=45)
    rol = models.CharField(max_length=20, choices=Rol.choices, null=False)
    documento = models.CharField(max_length=15, null=False, unique=True)
    ciudad = models.CharField(max_length=100, null=True)
    direccion = models.CharField(max_length=100, null=True)
    ocupacion = models.CharField(max_length=100, null=True)
    telefono = models.CharField(max_length=50, null=True)
    fechaNacimiento = models.DateField(null=True)

    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["rol", "password", "documento"]

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.email


class Ahorro(models.Model):

    idAhorro = models.AutoField(primary_key=True)
    DocAsociado = models.ForeignKey(
        User, on_delete=models.CASCADE, to_field="documento")
    fecha = models.DateField(auto_now_add=True, null=False)
    descripcion = models.CharField(max_length=200, null=True)
    monto = models.IntegerField(null=False)
    firmaDigital = models.CharField(max_length=200)
    tipoConsignacion = models.CharField(max_length=200)

    def __str__(self):
        return self.idAhorro


class Multa(models.Model):

    idMulta = models.AutoField(primary_key=True)
    asociadoReferente = models.ForeignKey(
        User, on_delete=models.CASCADE, to_field='documento', name="asociadoReferente")
    motivo = models.CharField(max_length=200)
    fecha = models.DateField(auto_now_add=True)
    costo = models.IntegerField()
    estadoMulta = models.BooleanField()

    def __str__(self):
        return self.idMulta


class CuotaManejo(models.Model):
    idCuotaManejo = models.AutoField(primary_key=True)
    #idAsociado = models.ForeignKey(User, on_delete=models.CASCADE)
    fechaComienzo = models.DateField(auto_now=False, auto_now_add=False)
    fechaFin = models.DateField(auto_now=False, auto_now_add=False)
    tasaInteres = models.IntegerField()

    def __str__(self):
        return self.idCuotaManejo


# modelo de reunion , el cual es modelo padre de
# reunion virtual y reunion presencial
class Reunion(models.Model):
    # asociado es una llave foranea de asociado de tipo onetoone Field
    idReunion = models.AutoField(primary_key=True)
    reunionAsociado = models.ForeignKey(
        User, on_delete=models.CASCADE, to_field="documento")
    fechaCreacion = models.DateTimeField(auto_now_add=True, null=False)
    fecha = models.DateField(null=False)
    hora = models.TimeField(null=False)
    motivo = models.CharField(max_length=300)
    tipoReunion = models.CharField(max_length=10, null=False)
    asistencia = models.BooleanField(default=True, null=False)

    def __str__(self):
        return self.idReunion + self.asociado

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['reunionAsociado', 'idReunion'], name='unique_reunionAsociado_idReunion_combination'
            )
        ]


class ReunionPresencial(Reunion):
    sitio = models.CharField(max_length=100)
    costo = models.IntegerField(null=False, validators=[MinValueValidator(3)])

    def __str__(self):
        return self.id_reunionPresencial


class ReunionVirtual(Reunion):
    enlace = models.CharField(max_length=200, null=False)

    def __str__(self):
        return self.id_reunionVirtual


class Prestamo(models.Model):
    solicitudPrestamo = models.CharField(primary_key=True, max_length=30)
    # codeudor es una llave foranea de asociado
    codeudor = models.ForeignKey(
        User, name='codeudor', null=False, on_delete=models.CASCADE, related_name='prestamoCodeudor')
    # deudor es una llave foranea de cliente
    deudor = models.ForeignKey(
        User, name='deudor', null=False, on_delete=models.CASCADE, related_name='prestamoDeudor')
    monto = models.IntegerField()
    fecha = models.DateField(default=now().date(), null=False)
    estadoPrestamo = models.BooleanField(default=False)
    interes = models.FloatField()
    comision = models.IntegerField()

    def checkErrors(self):
        return self.montoValido() == []

    def montoValido(self):
        # array para almacenar los errores
        errors = []
        if self.monto > 0:
            return errors.append("Monto valido")
        else:
            return errors.append("Monto no valido")

    def __str__(self):
        return self.solicitudPrestamo + " a: " + self.deudor  # Cambiara por deudor luego

    class Meta:
        verbose_name = 'prestamo'
        verbose_name_plural = 'prestamos'


####
'''
#Estado de cuenta
class EstadoCuenta(models.Model):
    idEstado= models.AutoField(primary_key=True),
    #Llave foranea a User:
    idAsociado= models.ForeignKey(
        User, name='asociado', null=False, on_delete=models.CASCADE, related_name='estadoAsociado'),
    #Llaves foraneas a Ahorro:
    montoAhorrado= models.ForeignKey(Ahorro, name='monto',null=False, on_delete=models.CASCADE, related_name='montoAhorrado'),
    fechaAhorro=models.ForeignKey(Ahorro, name='fecha',null=False, on_delete=models.CASCADE, related_name='fechaAhorro'),
    #Llave foranea a Prestamo:
    prestamosActivos= models.ForeignKey(
    Prestamo, name='prestamo', null=False, on_delete=models.CASCADE, related_name='prestamosActivos'),
    #Nuevos campos:
    fechaGenerada=models.DateField(default=now().date(), null=False),
    retiroGanancia= models.IntegerField(null=False),
    montoActual= models.IntegerField(null=False),
    gananciaActual= models.IntegerField(null=False)
####
'''


class Abono(models.Model):
    idAbono = models.AutoField(primary_key=True)
    idPrestamo = models.ForeignKey(Prestamo, on_delete=models.CASCADE)
    abona = models.OneToOneField(
        User, name='abona', on_delete=models.CASCADE, null=False, to_field="documento")
    cuentaAhorro = models.OneToOneField(
        Ahorro, name="cuentaAhorro", null=False, to_field="idAhorro", on_delete=models.CASCADE)
    monto = models.IntegerField(null=False)
    fecha = models.DateField(auto_now_add=True, null=False)
    descripcion = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.idAbono

    class Meta:
        verbose_name = 'Abono'
        verbose_name_plural = 'Abonos'
