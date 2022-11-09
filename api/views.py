from django.shortcuts import render
from optparse import Values
from django import views
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import Usuario
import json
from django.db.utils import IntegrityError
# Create your views here.

# creacion de una vista que implementara los requests


class DesarrolloView(View):

    # Metodo que nos servira para saltar el error de csrf
    @method_decorator(csrf_exempt)
    # csrf: Es un mecanismo para evitar falsificación entre peticiones de frontend contra backend
    # Metodo para despachar o enviar, cuando se hace una petición
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # GET
    def get(self, request, idUsuario=0):

        try:
            # Busqueda por id
            if (not (idUsuario == 0)):

                usuarios = list(Usuario.objects.filter(
                    idUsuario=idUsuario).values())

                if len(usuarios) > 0:
                    # dado que por id solo se busca un usuario, ese usuario estara en posicion 1
                    usuarioGet = usuarios[0]
                    datos = {'mensaje': 'Usuario encontrado',
                             'Usuario': usuarioGet}
                else:
                    datos = {'Mensaje': 'Usuario no encontrado'}
                return JsonResponse(datos)

            # Sino se da el id, se da la lista de usuarios
            else:
                usuarios = list(Usuario.objects.values())

                if len(usuarios) > 0:
                    datos = {'mensaje ': 'Lista de Usuarios',
                             'Usuarios': usuarios}
                else:
                    datos = {'mensaje': 'Usuarios no encontrados'}

                return JsonResponse(datos)

        except Exception as e:
            print(repr(e))
            return JsonResponse({'msg': 'Ocurrio un error'})

    # POST:Registro
    def post(self, request):

        response = {}

        try:
            # print(request.body)
            # jason data
            # Convierte los datos que se registran en un diccionario python
            jd = json.loads(request.body)
            # print(jd)

            responde = Usuario.objects.create(
                correoUsr=jd['correoUsr'],
                admin=jd['admin'],
                contrasena=jd['contrasena']
            )

            datos = {'Mensaje': 'Registro exitoso'}
            return JsonResponse(datos)

        except IntegrityError as ie:
            print(repr(ie))
            response['status'] = False
            response['msg'] = 'Usuario existente con ese correo'

        except Exception as e:
            print(repr(e))
            response['status'] = False
            response['msg'] = 'Formato incorrecto'

        return JsonResponse(response)

    #PUT: Actualización
    def put(self, request, idUsuario):

        # datos cargados
        # Diccionario de los datos de json enviados
        jd = json.loads(request.body)
        #usuarios = list(Usuario.objects.filter(idUsuario=idUsuario).values())
        usuarios = list(Usuario.objects.filter(idUsuario=idUsuario).values())

        if len(usuarios) > 0:
            # Usamos get en vez de filter porque ya estan cargados los datos
            usuarioAct = Usuario.objects.get(idUsuario=idUsuario)

            # Actualización de datos:
            usuarioAct.correoUsr = jd['correoUsr']
            usuarioAct.contrasena = jd['contrasena']
            usuarioAct.save()  # guarda los cambios

            datos = {'Mensaje': 'Actualizacion exitosa'}

        else:
            datos = {'Mensaje': 'Usuario no encontrado'}

        return JsonResponse(datos)

    #DELETE: Eliminar
    def delete(self, request, idUsuario):
        usuarios = list(Usuario.objects.filter(idUsuario=idUsuario).values())

        if len(usuarios) > 0:
            Usuario.objects.filter(idUsuario=idUsuario).delete()
            datos = {'Mensaje': 'Usuario Eliminado'}
        else:
            datos = {'Mensaje': 'Usuario no encontrado'}

        return JsonResponse(datos)
