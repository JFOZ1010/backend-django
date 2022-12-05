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
        #fields = ('__all__')
        fields = ('id', 'monto', 'fecha', 'cliente', 'asociado')


    def create(self,validated_data):
        return Ahorro.objects.create(**validated_data)
"""
    

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