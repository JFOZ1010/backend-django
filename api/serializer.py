from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Usuario
from django.utils.translation import gettext as _


class UserSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    nombre = serializers.CharField()
    apellido = serializers.CharField()
    email = serializers.EmailField()
    rol = serializers.CharField()
    enabled = serializers.BooleanField()
    password = serializers.CharField(required=False)

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
