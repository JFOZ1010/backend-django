from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import ValidationError
from django.utils.translation import gettext as _
from api.models import Ahorro, Prestamo, User, Abono, Multa, Reunion, ReunionPresencial, ReunionVirtual, Cliente, Rol
from django.contrib.auth.hashers import make_password
from django.db import models


class UserSerializer(serializers.ModelSerializer):

    # "is_staff": true (admin en Django)
    # "is_active": true, (activo en Django)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "rol",
            "first_name",
            "last_name",
            "is_active",
            "fechaNacimiento",
            "documento",
            "ciudad",
            "direccion",
            "ocupacion",
            "telefono"
        ]
        constraints = [
            models.UniqueConstraint(fields=['email'], condition=models.Q(
                is_deleted=False), name='unique_undeleted_name')
        ]

    def validate(self, attrs):

        user_exist = self.Meta.model.objects.filter(
            documento=attrs['documento']).exists()
        if user_exist:
            my_user = self.Meta.model.objects.get(documento=attrs['documento'])
            if not attrs['password'] == my_user.password:
                attrs['password'] = make_password(attrs['password'])
        else:
            attrs['password'] = make_password(attrs['password'])

        return super().validate(attrs)

    def update(self, instance, validated_data):

        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)
        instance.rol = validated_data.get('rol', instance.rol)
        instance.first_name = validated_data.get(
            'first_name', instance.first_name)
        instance.last_name = validated_data.get(
            'last_name', instance.last_name)
        instance.is_active = validated_data.get(
            'is_active', instance.is_active)
        instance.fechaNacimiento = validated_data.get(
            'fechaNacimiento', instance.fechaNacimiento)
        instance.documento = validated_data.get(
            'documento', instance.documento)
        instance.ciudad = validated_data.get('ciudad', instance.ciudad)
        instance.direccion = validated_data.get(
            'direccion', instance.direccion)
        instance.ocupacion = validated_data.get(
            'ocupacion', instance.ocupacion)
        instance.telefono = validated_data.get('telefono', instance.telefono)
        instance.save()

        return instance


class ClienteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cliente
        fields = [
            "id",
            "email",
            "password",
            "rol",
            "asociadoVinculado",
            "first_name",
            "last_name",
            "is_active",
            "documento",
            "telefono"
        ]

    def validate(self, attrs):

        # Validación como usuario
        user_exist = User.objects.filter(
            documento=attrs['documento']).exists()
        if user_exist:
            my_user = User.objects.get(documento=attrs['documento'])
            if not attrs['password'] == my_user.password:
                attrs['password'] = make_password(attrs['password'])
        else:
            attrs['password'] = make_password(attrs['password'])

        # Validación como cliente
        user_asociado_exist = User.objects.filter(
            documento=attrs['asociadoVinculado']).exists

        if not user_asociado_exist:
            raise ValidationError(
                'El asociado no existe'
            )
        if not User.objects.get(documento=attrs['asociadoVinculado']).rol == Rol.ASOCIADO:
            raise ValidationError(
                'No es asociado'
            )
        if not attrs['rol'] == Rol.CLIENTE:
            raise ValidationError(
                'No se está registrando como Cliente'
            )

        return super().validate(attrs)

    def update(self, instance, validated_data):

        instance.asociadoVinculado = validated_data.get(
            'asociadoVinculado', instance.asociadoVinculado)
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)
        instance.rol = validated_data.get('rol', instance.rol)
        instance.first_name = validated_data.get(
            'first_name', instance.first_name)
        instance.last_name = validated_data.get(
            'last_name', instance.last_name)
        instance.is_active = validated_data.get(
            'is_active', instance.is_active)
        instance.fechaNacimiento = validated_data.get(
            'fechaNacimiento', instance.fechaNacimiento)
        instance.documento = validated_data.get(
            'documento', instance.documento)
        instance.telefono = validated_data.get('telefono', instance.telefono)
        instance.save()

        return instance


# Serializacion para prestamos

class PrestamoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Prestamo
        fields = '__all__'

    def create(self, validated_data):
        return Prestamo.objects.create(**validated_data)


#####################


class AhorroSerializer(serializers.ModelSerializer):

    # un serializador para el modelo de Ahorro

    class Meta:
        model = Ahorro
        fields = ["idAhorro", "DocAsociado", "fecha", "monto",
                  "descripcion", "firmaDigital", "tipoConsignacion", "autorizado"]

    def create(self, validated_data):
        return Ahorro.objects.create(**validated_data)


# Serialización de Abono

class AbonoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Abono
        fields = '__all__'

    # def validate(self, attrs):
    ##    monto_nat = attrs["monto"] <= 0
    # print(attrs["cuentaAhorro"])
    # if (attrs["cuentaPrestamo"]):
    # raise ValidationError(
    ##            "Hay prestamo"
    # )
    # if (attrs["cuentaAhorro"] and attrs["cuentaSancion"]):
    # raise ValidationError(
    ##            "Debe abonar solo a una cuenta"
    # )
    # if (attrs["cuentaPrestamo"] and attrs["cuentaSancion"]):
    # raise ValidationError(
    ##            "Debe abonar solo a una cuenta"
    # )
    # abona_exist = User.objects.filter(
    # documento=attrs["abona"]
    # ).exists()
    # prestamos_exist = Prestamo.objects.filter(
    # solicitudPrestamo=attrs["cuentaPrestamo"]
    # ).exists()
    # ahorro_exist = Ahorro.objects.filter(
    # idAhorro=attrs["cuentaAhorro"]
    # ).exists()
    # multa_exist = Multa.objects.filter(
    # idMulta=attrs["cuentaSancion"]
    # ).exists()
    # if abona_exist:
    # raise ValidationError(
    ##            "El abonador no existe"
    # )
    # if prestamos_exist:
    # raise ValidationError(
    ##            "El prestamo no existe"
    # )
    # if ahorro_exist:
    # raise ValidationError(
    ##            "No existe la cuenta de ahorro"
    # )
    # if multa_exist:
    # raise ValidationError(
    ##            "No existe la cuenta de sancion"
    # )
    # if monto_nat:
    # raise ValidationError(
    ##            "Ingrese un monto válido"
    # )
    # return super().validate(attrs)


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
