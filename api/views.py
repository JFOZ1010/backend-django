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
from django.contrib import auth
from django.utils import timezone

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
        try:
            return self.request.user.usuario.rol == Rol.ADMIN
        except Exception as e:
            print(repr(e))
            return JsonResponse({"msg": 'Falló el test'})

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
            return JsonResponse({"msg": 'Ocurrio un error'})

    # POST:Registro
    def post(self, request):

        response = {}

        try:
            content = json.loads(request.body.decode('utf-8'))
            action = content["action"]
            dataUser = {
                "username": content["email"], "first_name": content["nombre"], "last_name": content["apellido"],
                "is_active": bool(content["enabled"]), "email": content["email"], "password": content["password"],
            }
            dataUsuario = {
                "rol": content["rol"], "fechaNacimiento": content["fechaNacimiento"]
            }
            if action == 'create':
                response = createUser(dataUser, dataUsuario)
            else:
                response = modifyUser(dataUser, dataUsuario)
        except IntegrityError as ie:
            print(repr(ie))
            response["status"] = False
            response["msg"] = "Ya existe un usuario con dicho correo"
        except Exception as e:
            response["status"] = False
            print(repr(e))
            response["msg"] = "Formato Incorrecto"
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


@method_decorator(csrf_exempt, name='dispatch')
class Auth(View):

    def post(self, request):
        try:
            res = {}
            data = json.loads(request.body.decode('utf-8'))
            username = data["email"]
            password = data["password"]
            user = auth.authenticate(username=username, password=password)
            res["status"] = user is not None
            print(user)
            if res["status"]:
                res["msg"] = UserSerializer(user).data
                auth.login(request, user)
            else:
                res["msg"] = "No pudo logearse"
            return JsonResponse(res)
        except Exception as e:
            print(repr(e))
            return JsonResponse({"err": "User not authenticated"})

    def delete(self, request):
        try:
            auth.logout(request)
            return JsonResponse({"res": True})
        except Exception as e:
            print(repr(e))
            return JsonResponse({"res": False, "message": "Ocurrio un error en el logout"})


def createUser(dataUser, dataUsuario):
    dataUser["date_joined"] = timezone.now()
    print(dataUsuario)
    up = Usuario(**dataUsuario)
    u = User(**dataUser)
    up.user = u
    u.usuario = up
    if not u.usuario.checkData():
        return {"status": False, "msg": u.usuario.getErrors()}
    u = User.objects.create_user(**dataUser)
    for attr, value in dataUsuario.items():
        setattr(u.usuario, attr, value)
    u.save()
    return {"status": True, "msg": "Usuario creado"}


def modifyUser(dataUser, dataUsuario):
    try:
        newPass = dataUser.pop("password", None)
        u: User = User.objects.get(username=dataUser["username"])
        User.objects.filter(username=dataUser["username"])
        if newPass != "" or newPass is None:
            u.password = newPass
        for attr, value in dataUser.items():
            setattr(u, attr, value)
        for attr, value in dataUsuario.items():
            setattr(u.usuario, attr, value)
        if u.usuario.checkData():
            if newPass != "" or newPass is None:
                u.set_password(newPass)
            u.save()
            return {"status": True, "msg": "Usuario modificado correctamente"}
        else:
            return {"status": False, "msg": u.usuario.getErrors()}

    except Exception as e:
        print(repr(e))
        return {"status": False, "msg": "No existe el usuario"}
