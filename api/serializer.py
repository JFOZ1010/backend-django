from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import ValidationError
from django.utils.translation import gettext as _
from api.models import Ahorro, Prestamo, User, Abono, Multa, Reunion, ReunionPresencial, ReunionVirtual
from django.contrib.auth.hashers import make_password
from django.db import models


class UserSerializer(serializers.ModelSerializer):

    # "is_staff": true (admin en Django)
    # "is_active": true, (activo en Django)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password",
                  "rol", "first_name", "last_name", "is_active", "fechaNacimiento", "documento", "ciudad", "direccion", "ocupacion", "telefono"]
        constraints = [
            models.UniqueConstraint(fields=['email'], condition=models.Q(
                is_deleted=False), name='unique_undeleted_name')
        ]

    def validate(self, attrs):
        email_exists = User.objects.filter(email=attrs["email"]).exists()
        doc_exists = User.objects.filter(id=attrs["documento"]).exists()
        if email_exists and doc_exists:
            raise ValidationError(
                'Ya hay un usuario con su correo y documento')
        attrs['password'] = make_password(attrs['password'])
        return super().validate(attrs)

    def update(self, instance, validated_data):
        email = validated_data.get('email', '')

        if User.objects.exclude(pk=instance.pk).filter(email=email):
            raise serializers.ValidationError(
                'User with this email already exists.')
        return super().update(instance, validated_data)


# Serializacion para prestamos


class PrestamoSerializer(serializers.ModelSerializer):
    '''    
solicitudPrestamo = serializers.CharField()
    codeudor_id = serializers.IntegerField()
    deudor_id = serializers.IntegerField()
    monto = serializers.IntegerField()
    fecha = serializers.DateField()
    estadoPrestamo = serializers.BooleanField()
    interes = serializers.FloatField()
    comision = serializers.IntegerField()'''

    class Meta:
        model = Prestamo
        fields = ["solicitudPrestamo", "codeudor", "deudor", "monto",
                  "fecha", "estadoPrestamo", "interes","comision"]

    def create(self, validated_data):
        return Prestamo.objects.create(**validated_data)


class AhorroSerializer(serializers.ModelSerializer):

    # un serializador para el modelo de Ahorro

    class Meta:
        model = Ahorro
        fields = ["idAhorro", "DocAsociado", "fecha", "monto",
                  "descripcion", "firmaDigital", "tipoConsignacion"]

    def create(self, validated_data):
        return Ahorro.objects.create(**validated_data)


# Serialización de Abono

class AbonoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Abono
        fields = ["idAbono", "idPrestamo", "cuentaAhorro", "abona",
                  "monto", "fecha", "descripcion"]

        def validate(self, attrs):
            abona_exist = User.objects.filter(
                documento=attrs["abona"]).exists()
            prestamos_exist = Prestamo.objects.filter(
                idPrestamo=attrs["prestamo"]).exists()
            ahorro_exist = Ahorro.objects.filter(
                idAhorro=attrs["cuentaAhorro"]).exists()
            monto_nat = attrs["monto"] <= 0

            if abona_exist:
                raise ValidationError(
                    "El abonador no existe"
                )
            if prestamos_exist:
                raise ValidationError(
                    "El prestamo no existe"
                )
            if ahorro_exist:
                raise ValidationError(
                    "No existe la cuenta de ahorro"
                )
            if monto_nat:
                raise ValidationError(
                    "Ingrese un monto válido"
                )
            return super().validate(attrs)


class SancionSerializer(serializers.ModelSerializer):

    class Meta:

        model = Multa
        #fields = ["asociadoReferente", "motivo", "costo", "estadoMulta"]
        fields = "__all__"

    def create(self, validated_data):
        return Multa.objects.create(**validated_data)


class ReunionPresencialSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReunionPresencial
        fields = '__all__'

    def validate(self, attrs):

        asociado_exist = User.objects.filter(
            documento=attrs["reunionAsociado"]).exists()
        if asociado_exist:
            raise ValidationError(
                "El asociado no existe"
            )
        if attrs["costo"] < 0:
            raise ValidationError(
                "Monto no válido"
            )
        return super().validate(attrs)

    def update(self, instance, validated_data):

        instance.reunionAsociado = validated_data.get(
            'reunionAsociado', instance.reunionAsociado)
        instance.fecha = validated_data.get('fecha', instance.fecha)
        instance.hora = validated_data.get('hora', instance.hora)
        instance.motivo = validated_data.get('motivo', instance.motivo)
        instance.asistencia = validated_data.get(
            'asistencia', instance.asistencia)
        instance.sitio = validated_data.get('sitio', instance.sitio)
        instance.costo = validated_data.get('costo', instance.costo)
        instance.save()

        return instance


class ReunionVirtualSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReunionVirtual
        fields = '__all__'

    def validate(self, attrs):

        asociado_exist = User.objects.filter(
            documento=attrs["reunionAsociado"]).exists()
        if asociado_exist:
            raise ValidationError(
                "El asociado no existe"
            )
        if attrs["enlace"] == '':
            raise ValidationError(
                "Ingrese un enlace para la reunión virtual"
            )

        return super().validate(attrs)

    def update(self, instance, validated_data):
        instance.reunionAsociado = validated_data.get(
            'reunionAsociado', instance.reunionAsociado)
        instance.fecha = validated_data.get('fecha', instance.fecha)
        instance.hora = validated_data.get('hora', instance.hora)
        instance.motivo = validated_data.get('motivo', instance.motivo)
        instance.asistencia = validated_data.get(
            'asistencia', instance.asistencia)
        instance.enlace = validated_data.get('enlace', instance.enlace)
        instance.save()

        return instance


class ReunionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reunion
        fields = "__all__"

    def validate(self, attrs):

        asociado_exist = User.objects.filter(
            documento=attrs["reunionAsociado"]).exists()
        if asociado_exist:
            raise ValidationError(
                "El asociado no existe"
            )
        if attrs["tipoReunion"] == "Virtual" or attrs["tipoReunion"] == "Presencial":
            raise ValidationError(
                "El tipo de reunión no es válido"
            )

        return super().validate(attrs)

    def update(self, instance, validated_data):

        instance.reunionAsociado = validated_data.get(
            'reunionAsociado', instance.reunionAsociado)
        instance.fechaCreacion = validated_data.get(
            'fechaCreacion', instance.fechaCreacion)
        instance.fecha = validated_data.get('fecha', instance.fecha)
        instance.hora = validated_data.get('hora', instance.hora)
        instance.motivo = validated_data.get('motivo', instance.motivo)
        instance.tipoReunion = validated_data.get(
            'tipoReunion', instance.tipoReunion)
        instance.asistencia = validated_data.get(
            'asistencia', instance.asistencia)
        instance.save()

        return instance
