from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from api.models import Usuario, Rol, Asociado, Ahorro, Prestamo
import json
from django.db.utils import IntegrityError
from api.serializer import UserSerializer, AhorroSerializer, AsociadoSerializer, PrestamoSerializer
from django.contrib import auth
from django.utils import timezone
from django.contrib.auth import authenticate
from .tokens import create_jwt_pair_for_user



# modulos nuevos que importo del framework DRF.
from rest_framework.request import Request
from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status, generics
from rest_framework import authentication, permissions
from django.http import JsonResponse
from django.contrib import auth

from django.db.models.functions import Lower

# Create your views here.

# creacion de una vista que implementara los requests


# creacion de una vista que implementara los requests


class Users(APIView):

    # Metodo que nos servira para saltar el error de csrf
    @method_decorator(csrf_exempt)
    # csrf: Es un mecanismo para evitar falsificación entre peticiones de frontend contra backend
    # Metodo para despachar o enviar, cuando se hace una petición
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # GET

    def get(self, request, id=0):
        try:
            if id > 0:
                myUser = User.objects.all().filter(id=id)
                print(myUser)
                serializer = UserSerializer(myUser, many=True)
                return JsonResponse(serializer.data, safe=False)
            else:
                users = User.objects.all()
                serializer = UserSerializer(users, many=True)
                return JsonResponse(serializer.data, safe=False)
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

    # PUT: Actualización
    def put(self, request, idUsuario):

        # datos cargados
        # Diccionario de los datos de json enviados
        jd = json.loads(request.body)
        # usuarios = list(Usuario.objects.filter(idUsuario=idUsuario).values())
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

    # DELETE: Desactivar
    def delete(self, request, idUsuario):
        usuarios = list(Usuario.objects.filter(idUsuario=idUsuario).values())

        if len(usuarios) > 0:
            Usuario.objects.filter(idUsuario=idUsuario).delete()
            datos = {'Mensaje': 'Usuario Eliminado'}
        else:
            datos = {'Mensaje': 'Usuario no encontrado'}

        return JsonResponse(datos)


class Auth(APIView):
    permission_classes = []

    # Login
    def post(self, request: Request):
        username = request.data.get("email")
        password = request.data.get("password")

        print(repr(username))

        user = authenticate(username=username, password=password)

        if user is not None:

            tokens = create_jwt_pair_for_user(user)

            response = {"message": "Login Successfull",
                        "user": username, "tokens": tokens}
            return Response(data=response, status=status.HTTP_200_OK)

        else:
            return Response(data={"message": "Invalid email or password"})

    # Validate
    def get(self, request: Response, format=None):
        content = {
            "user": str(request.user),
            "auth": str(request.auth)
        }
        return Response(data=content, status=status.HTTP_200_OK)


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


#View prestamos:

class PrestamoCreate(APIView):
    serializerClass= PrestamoSerializer 
    model = Prestamo
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = PrestamoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

##Pendiente: 
class PrestamoList(APIView):
    serializer_class = PrestamoSerializer
    model = Prestamo
    permission_classes = [permissions.AllowAny]
    #queryset = Prestamo.objects.all()
    def get(self, request):
        prestamos= list(Prestamo.objects.values())
        if len(prestamos)>0:
            datos = {'mensaje':'exitoso', 'prestamos':prestamos}
        else:
            datos = {'mensaje':'prestamos no encontrados'}
        return JsonResponse(datos)


"""SESION DEDICADA A AHORROS, Y TODO LO RELACIONADO CON ESTE"""


# crear una clase based view para ahorros que herede de la clase View, y tome el serializador de ahorros

"""
@method_decorator(csrf_exempt, name='dispatch')
class AhorrosView(View):
    #GET: Obtener
    def get(self, request):
        ahorros = list(Ahorro.objects.all().values())
        return JsonResponse(ahorros, safe=False)
"""

# CLASE CREAR
"""
class AhorrosCreate(generics.CreateAPIView):
    serializer_class = AhorroSerializer
    model = Ahorro
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = AhorroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""

# crear una vista para crear Ahorros, con el metodo post tomando como la APIView


@method_decorator(csrf_exempt, name='dispatch')
class AhorrosCreate(APIView):
    permission_classes = [permissions.AllowAny]

    # crear un metodo POST con un try except para el manejo de errores
    def post(self, request):
        try:
            # crear un objeto de la clase AhorroSerializer, pasandole como parametro el request.data
            serializer = AhorroSerializer(data=request.data)
            # si el serializer es valido
            if serializer.is_valid():
                # guardar el serializer
                serializer.save()
                # retornar el serializer.data, y el status de la peticion
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            # si el serializer no es valido, retornar el serializer.errors, y el status de la peticion
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # si ocurre un error, retornar un JsonResponse con el mensaje de error
        except Exception as e:
            return JsonResponse({"err": repr(e)})


# CLASE LISTAR
class AhorrosList(generics.ListAPIView):
    serializer_class = AhorroSerializer
    model = Ahorro
    permission_classes = [permissions.AllowAny]
    queryset = Ahorro.objects.all()


# CLASE ACTUALIZAR
class AhorrosUpdate(generics.UpdateAPIView):
    serializer_class = AhorroSerializer
    model = Ahorro
    permission_classes = [permissions.AllowAny]
    queryset = Ahorro.objects.all()

    def put(self, request, pk):
        ahorro = self.get_object(pk)
        serializer = self.serializer_class(ahorro, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# CLASE ELIMINAR


class AhorrosDelete(generics.DestroyAPIView):
    serializer_class = AhorroSerializer
    model = Ahorro
    permission_classes = [permissions.AllowAny]
    queryset = Ahorro.objects.all()

    def delete(self, request, pk):
        ahorro = self.get_object(pk)
        ahorro.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#crear una vista para Asociado, con el metodo post tomando como la APIView
@method_decorator(csrf_exempt, name='dispatch')
class AsociadoCreate(APIView):
    permission_classes = [permissions.AllowAny]

    # crear un metodo POST con un try except para el manejo de errores
    def post(self, request):
        try:
            # crear un objeto de la clase AsociadoSerializer, pasandole como parametro el request.data
            serializer = AsociadoSerializer(data=request.data)
            # si el serializer es valido
            if serializer.is_valid():
                # guardar el serializer
                serializer.save()
                # retornar el serializer.data, y el status de la peticion
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            # si el serializer no es valido, retornar el serializer.errors, y el status de la peticion
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # si ocurre un error, retornar un JsonResponse con el mensaje de error
        except Exception as e:
            return JsonResponse({"err": repr(e)})
        
#crear una vista para Asociado, para listar todos los asociados
class AsociadoList(generics.ListAPIView):
    serializer_class = AsociadoSerializer
    model = Asociado
    permission_classes = [permissions.AllowAny]
    queryset = Asociado.objects.all()
