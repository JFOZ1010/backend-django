from rest_framework import serializers
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from api.models import Usuario, Ahorro, Asociado, Prestamo
from rest_framework.validators import ValidationError


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Usuario
        fields = ['id', 'first_name', 'username', 'rol']

    def validate(self, attrs):

        email_exists = User.objects.filter(email=attrs["email"]).exists()

        if email_exists:
            raise ValidationError('Email has already been used')

        return super().validate(attrs)

    def update(self, instance, validated_data):
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.apellido = validated_data.get('apellido', instance.apellido)
        instance.email = validated_data.get('email', instance.email)
        instance.rol = validated_data.get('rol', instance.rol)
        instance.enabled = validated_data.get('enabled', instance.enabled)
        instance.password = validated_data.get('password', instance.enabled)

        return super().update(instance, validated_data)

    def to_representation(self, instance: User):
        ret = {}
        p: Usuario = instance.usuario
        ret['username'] = instance.username
        ret['nombre'] = instance.first_name
        ret['apellido'] = instance.last_name
        ret['email'] = instance.email
        ret['rol'] = p.rol
        ret['enabled'] = instance.is_active

        return ret

##Serializacion para prestamos

class PrestamoSerializer(serializers.Serializer):
    solicitudPrestamo = serializers.CharField()
    codeudor = serializers.CharField()
    deudor = serializers.CharField()   
    monto = serializers.IntegerField()
    fecha = serializers.DateField()
    estadoPrestamo = serializers.BooleanField()
    interes = serializers.FloatField()
    comision = serializers.IntegerField()

    def to_representation(self, instance: Prestamo):
        ret = {}
        p: Prestamo = instance.Prestamo
        ret['solicitudPrestamo'] = instance.solicitudPrestamo
        ret['codeudor'] = instance.codeudor
        ret['deudor'] = instance.deudor
        ret['monto'] = instance.monto
        ret['fecha'] = instance.fecha
        ret['estadoPrestamo'] = instance.estadoPrestamo
        ret['interes'] = instance.interes
        ret['comision'] = instance.comision

        return ret  

class AhorroSerializer(serializers.Serializer):

    #un serializador para el modelo de Ahorro
    idAhorro = serializers.IntegerField()
    idAsociado = serializers.CharField()
    fecha = serializers.DateField()
    descripcion = serializers.CharField()
    monto = serializers.IntegerField()
    firmaDigital = serializers.CharField()
    tipoConsignacion = serializers.CharField()

    def create(self,validated_data):
        return Ahorro.objects.create(**validated_data)
    

class AsociadoSerializer(serializers.Serializer):

    #un serializador para el modelo de Asociado
    documentoAsociado = serializers.CharField()
    nombre = serializers.CharField()
    direccion = serializers.CharField()
    ciudad = serializers.CharField()
    ocupacion = serializers.CharField()
    telefono = serializers.CharField()

    def create(self,validated_data):
        return Asociado.objects.create(**validated_data)