from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now


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
    fecha = models.DateField(default=now().date(), null=False)
    descripcion = models.CharField(max_length=200, null=True)
    monto = models.IntegerField(null=False)
    firmaDigital = models.CharField(max_length=200)
    tipoConsignacion = models.CharField(max_length=200)

    def __str__(self):
        return self.idAhorro


class Multa(models.Model):

    idMulta = models.AutoField(primary_key=True)
    #idAsociado = models.ForeignKey(User, on_delete=models.CASCADE)
    motivo = models.CharField(max_length=200)
    fecha = models.DateField()
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
    idReunion = models.AutoField(primary_key=True)
    # asociado es una llave foranea de asociado de tipo onetoone Field
    # asociado = models.ForeignKey(User, on_delete=models.CASCADE)
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
    # codeudor es una llave foranea de asociado
    # codeudor = models.ForeignKey(User, on_delete=models.CASCADE)
    # deudor es una llave foranea de cliente
    ## deudor = models.ForeignKey(User, on_delete=models.CASCADE)
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
        return self.solicitudPrestamo + " a: " + self.monto ##Cambiara por deudor luego


class Abono(models.Model):
    idAbono = models.AutoField(primary_key=True)
    idPrestamo = models.ForeignKey(Prestamo, on_delete=models.CASCADE)
    abona = models.OneToOneField(
        User, name='abona', on_delete=models.CASCADE, null=False, to_field="documento")
    monto = models.IntegerField(null=False)
    fecha = models.DateField(default=now().date(), null=False)
    descripcion = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.idAbono

    class Meta:
        verbose_name = 'Abono'
        verbose_name_plural = 'Abonos'
