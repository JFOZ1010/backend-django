from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.utils.translation import gettext as _
from api.models import Ahorro, Prestamo, User
from rest_framework.validators import ValidationError
from django.db import models


class UserSerializer(serializers.ModelSerializer):

    # "is_staff": true (admin en Django)
    # "is_active": true, (activo en Django)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password",
                  "rol", "first_name", "last_name", "is_active"]
        constraints = [
            models.UniqueConstraint(fields=['email'], condition=models.Q(
                is_deleted=False), name='unique_undeleted_name')
        ]

    def validate(self, attrs):
        email_exists = User.objects.filter(email=attrs["email"]).exists()
        if email_exists:
            raise ValidationError('Email has already been used')
        return super().validate(attrs)

    def update(self, instance, validated_data):
        email = validated_data.get('email', '')

        if User.objects.exclude(pk=instance.pk).filter(email=email):
            raise serializers.ValidationError(
                'User with this email already exists.')
        return super().update(instance, validated_data)


# Serializacion para prestamos


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

    # un serializador para el modelo de Ahorro
    idAhorro = serializers.IntegerField()
    fecha = serializers.DateField()
    descripcion = serializers.CharField()
    monto = serializers.IntegerField()
    firmaDigital = serializers.CharField()
    tipoConsignacion = serializers.CharField()

    def create(self, validated_data):
        return Ahorro.objects.create(**validated_data)
