from django.shortcuts import render
from optparse import Values
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.contrib.auth.models import User
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from api.models import Usuario, Rol
import json
from django.db.utils import IntegrityError
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from api.serializer import UserSerializer
from django.db.models.functions import Lower

# Create your views here.

# creacion de una vista que implementara los requests


class DesarrolloView(LoginRequiredMixin, UserPassesTestMixin, View):

    # Metodo que nos servira para saltar el error de csrf
    @method_decorator(csrf_exempt)
    # csrf: Es un mecanismo para evitar falsificación entre peticiones de frontend contra backend
    # Metodo para despachar o enviar, cuando se hace una petición
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        return self.request.user.usuario.rol == Rol.ADMIN

    # GET
    def get(self, request):

        try:
            list = User.objects.select_related(
                'usuario').order_by(Lower('first_name'))

            users = []
            for user in list:
                u: User = user
                if u.usuario.rol != Rol.PAR:
                    users.append(UserSerializer(u).data)
            return JsonResponse({"data": users}, safe=False)
        except Exception as e:
            print(repr(e))
            return JsonResponse({"msg": 'an error occured'})

    # POST:Registro
    def post(self, request):

        response = {}

        try:
            # print(request.body)
            # jason data
            # Convierte los datos que se registran en un diccionario python
            jd = json.loads(request.body)
            print(jd)

            if (jd['type'] == 'asociado'):

                responde = Usuario.objects.create(
                    correoUsr=jd['correoUsr'],
                    admin=jd['admin'],
                    contrasena=jd['contrasena'],
                    fechaNacimiento=jd['fechaNacimiento']
                )

                datos = {'Mensaje': 'Registro exitoso'}
                return JsonResponse(response)

            elif (jd['action'] == 'cliente'):
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
