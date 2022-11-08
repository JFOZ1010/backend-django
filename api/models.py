import re

from django.db import models
#from django.contrib.auth.models import User
#from django.core.exceptions import ValidationError
#from django.utils import timezone

# Create your models here.

#metodo global, que valide que el correo sea valido
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

#se creara el modelo de usuario, que cuenta con los atrivbutos: idUsuario, correoUsr, admin (booleano), y una contraseña. 
class Usuario(models.Model):
    idUsuario = models.AutoField(primary_key=True, max_length=100, blank=True)
    correoUsr = models.CharField(max_length=70)
    admin = models.BooleanField(default=False)
    contrasena = models.CharField(max_length=50)
    fechaNacimiento = models.DateTimeField(("fechaNacimiento"), auto_now=False, auto_now_add=False)

    '''
    def clean(self):
        self.correoUsr = validate_email(self.correoUsr)
        self.fechaNacimiento = validate_date(self.fechaNacimiento)
    '''
    '''
    class Meta:
        abstract = True
        #db_table = "Usuario"
    '''
    def __str__(self):
        return self.correoUsr

"""
Author: Juan Felipe Osorio
se creara el modelo de Asociado, que cuenta con los atributos: documentoAsociado, correoAsociado, nombre, 
direccion, ciudad, fechanacimento, ocupacion, telefono.
"""
class Asociado(Usuario): 
    documentoAsociado = models.IntegerField( primary_key=True, blank=True, max_length=10, null=True)
    #correoAsociado = models.CharField(max_length=70)
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=70)
    ciudad = models.CharField(max_length=50)
    #fechaNacimiento = models.models.DateTimeField(_("fechaNacimiento"), auto_now=False, auto_now_add=False)
    ocupacion = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50) #telefono con varchar, no necesitamos hacer nada con ese integer como telefono. 
    '''
    def clean(self):
        #self.correoAsociado = validate_email(self.correoAsociado)
        self.documentoAsociado = validate_document(self.documentoAsociado)
        #self.fechaNacimiento = validate_date(self.fechaNacimiento)
        
    '''
    def __str__(self):
        return self.documentoAsociado 

"""
Author: Juan Felipe Osorio
se crea el modelo de Ahorro, que cuenta con los atributos: idAhorro (Primary Key), idAsociado (Foreign Key), fecha (DateTimeField), 
descripcion (varchar), monto (float), firmaDigital (varchar), y tipoConsignacion (varchar).
"""
class Ahorro(models.Model):
    idAhorro = models.AutoField(primary_key=True)
    idAsociado = models.ForeignKey(Asociado, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now=False, auto_now_add=False)
    descripcion = models.CharField(max_length=50)
    monto = models.FloatField()
    firmaDigital = models.CharField(max_length=50)
    tipoConsignacion = models.CharField(max_length=50)

    def __str__(self):
        return self.idAhorro


"""
se crea el modelo de Multa que es un modelo para establecer las multas a los usuarios que no cumplan con los requisitos de la cooperativa, 
cuenta con los atributos: idMulta (primary Key), idAsociado (Foreign Key), motivo (varchar), fecha (DateTimeField), costo (int), estadoMulta (booleano).
"""
class Multa(models.Model):
    idMulta = models.AutoField(primary_key=True)
    idAsociado = models.ForeignKey(Asociado, on_delete=models.CASCADE)
    motivo = models.CharField(max_length=50)
    fecha = models.DateTimeField(auto_now=False, auto_now_add=False)
    costo = models.IntegerField()
    estadoMulta = models.BooleanField(default=False)

    def __str__(self):
        return self.idMulta


"""
Author: Juan Felipe Osorio
se crea el modelo de CuotaManejo, que cuenta con los atributos: idCuotaManejo (primary Key), idAsociado (Foreign Key),
fechaComieno (DateTimeField), FechaFin (DateTimeField), tasaInteres (int). 
"""
class CuotaManejo(models.Model):
    idCuotaManejo = models.AutoField(primary_key=True)
    idAsociado = models.ForeignKey(Asociado, on_delete=models.CASCADE)
    fechaComienzo = models.DateTimeField(auto_now=False, auto_now_add=False)
    fechaFin = models.DateTimeField(auto_now=False, auto_now_add=False)
    tasaInteres = models.IntegerField()

    def __str__(self):
        return self.idCuotaManejo


"""
Author: Juan Felipe Osorio    
se crea el modelo cliente, que tiene los atributos: documentoCliente, 
asociadoVinculado que es una llave foranea de Asociado, correoCliente, nombre, y un telefono (varchar). 
"""
class Cliente(Usuario):

    documentoCliente = models.IntegerField(("DocumentoC"), primary_key=True, blank=True, max_length=10, null=True)
    asociadoVinculado = models.ForeignKey(Asociado, on_delete=models.CASCADE)
    #correoCliente = models.CharField(max_length=70)
    nombre = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50)
    '''
    def clean(self):
        #self.correoCliente = validate_email(self.correoCliente)
        self.documentoCliente = validate_document(self.documentoCliente)
    '''
    def __str__(self):
        return self.documentoCliente

"""
Author: Juan Felipe Osorio
se crea el modelo de Prestamo que cuenta con una llave primaria llamada solicitudPrestamo que es varchar, una llave foranea llamada codeudor que hace referencia a la tabla Asociado
y una llave foranea llamada deudor que hace referencia a la tabla Cliente, tambien un atributo entero llamado monto, una fecha de tipo date, un estado de prestamo
que es un booleano, y un interes que es un float, por ultimo una comisión que es un integer.
"""
class Prestamo(models.Model):

    solicitudPrestamo = models.CharField(max_length=50, primary_key=True)
    codeudor = models.ForeignKey(Asociado, on_delete=models.CASCADE)
    deudor = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    monto = models.IntegerField("Monto")
    fecha = models.DateField(("Fecha"), auto_now=False, auto_now_add=False)
    estadoPrestamo = models.BooleanField("EstadoPrestamo")
    interes = models.FloatField("Interes")
    comision = models.IntegerField("Comision")

    #metodo para verificar que el monto sea valido
    def montoValido(self):
        if self.monto > 0:
            return True
        else:
            return False

    def __str__(self):
        return self.solicitudPrestamo

"""
Author: Juan Felipe Osorio
se crea el modelo de reunion, que es el modelo que se encarga de registrar las reuniones que se realizan entre el asociado y el cliente,
este modelo cuenta con una llave primaria llamada idReunion que es de tipo varchar, una llave foranea llamada asociado que hace referencia a la tabla
Asociado, una fecha de tipo date, una hora de tipo varchar, un motivo de tipo varchar, un tipo de reunion que es varchar, y una asistencia que es un booleano.
"""
class Reunion(models.Model):
    
        idReunion = models.CharField(max_length=50, primary_key=True)
        asociado = models.ForeignKey(Asociado, on_delete=models.CASCADE)
        fecha = models.DateField(("Fecha"), auto_now=False, auto_now_add=False)
        hora = models.CharField(max_length=50)
        motivo = models.CharField(max_length=50)
        tipoReunion = models.CharField(max_length=50)
        asistencia = models.BooleanField("Asistencia")

        #se añade esta clase, para que se establezca la jerarquia de la tabla siendo una clase padre de las clases hijas (Virtual, Presencial).

        '''
        class Meta: 
            abstract = True
        '''
        def __str__(self):
            return self.idReunion

"""
Author: Juan Felipe Osorio
se crea un modelo que es hijo del modelo Reunion, llamado reunionPresencial, que cuenta con una llave primaria llamada idReunion,
un sitio de tipo varchar, y un costo de tipo integer.
"""
class ReunionPresencial(Reunion):
    sitio = models.CharField(max_length=50)
    costo = models.IntegerField("Costo")

    def __str__(self):
        return self.idReunion


"""
Author: Juan Felipe Osorio
se crea un modelo que es hijo del modelo Reunion, llamado reunionVirtual, que cuenta con una llave primaria llamada enlace, un sitio de tipo int serial. 
"""
class ReunionVirtual(Reunion):
    enlace = models.IntegerField(("Enlace"), primary_key=True)

    def __str__(self):
        return self.idReunion


