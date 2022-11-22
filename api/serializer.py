from rest_framework import serializers
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from api.models import Usuario, Ahorro, Asociado


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
        p: Usuario = instance.usuario
        ret['nombre'] = instance.first_name
        ret['apellido'] = instance.last_name
        ret['email'] = instance.username
        ret['rol'] = p.rol
        ret['enabled'] = instance.is_active

        return ret

#crear el serializador para el ahorro 
"""
class AhorroSerializer(serializers.Serializer):
    class Meta:
        model = Ahorro
        fields = ('__all__')
"""
    

class AhorroSerializer(serializers.Serializer):
    
    #A serializer to display and create a Participant

    id = serializers.IntegerField()
    fecha = serializers.DateField()
    monto = serializers.FloatField()
    asociado = serializers.CharField()
    descripcion = serializers.CharField()
    tipo = serializers.CharField()
    estado = serializers.CharField()
    #enabled = serializers.BooleanField()
    #password = serializers.CharField(required=False)

    def to_representation(self, instance: Ahorro):
        ret = {}
        p: Ahorro = instance.ahorro
        ret['id'] = instance.id
        ret['fecha'] = instance.fecha
        ret['monto'] = instance.monto
        ret['asociado'] = instance.asociado
        ret['descripcion'] = instance.descripcion
        ret['tipo'] = instance.tipo
        ret['estado'] = instance.estado
       #ret['enabled'] = instance.is_active

        return ret  
