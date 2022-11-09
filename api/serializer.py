from django.utils import timezone
from rest_framework import serializers
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from api.models import Usuario


class UserSerializer(serializers.Serializer):

    """
        A serializer to display and create a Participant
    """
    nombre = serializers.CharField()
    apellido = serializers.CharField()
    email = serializers.EmailField()
    rol = serializers.CharField()
    enabled = serializers.BooleanField()
    password = serializers.CharField(required=False)

    def to_representation(self, instance: User):
        ret = {}
        p: Usuario = instance.profile
        ret['nombre'] = instance.first_name
        ret['apellido'] = instance.last_name
        ret['email'] = instance.username
        ret['rol'] = p.rol
        ret['enabled'] = instance.is_active

        return ret
