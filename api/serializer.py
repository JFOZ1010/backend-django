from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Usuario, Ahorro, Asociado
from django.utils.translation import gettext as _
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
