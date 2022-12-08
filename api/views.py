# Modulos DJANGO
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.utils import IntegrityError
from django.utils import timezone
from django.contrib.auth import authenticate
from django.db.models.functions import Lower
from django.http import JsonResponse
from django.http import Http404

# Modulos locales
from api.models import User, Ahorro, Prestamo
from api.serializer import UserSerializer, AhorroSerializer, PrestamoSerializer
from .tokens import create_jwt_pair_for_user

# modulos nuevos que importo del framework DRF.
from rest_framework.request import Request
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status, generics
from rest_framework import authentication, permissions


# Create your views here.


class SignUpView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = []
    queryset = User.objects.all()

    def get_object(self, pk):
        try:
            return User.objects.get(id=pk)
        except User.DoesNotExist:
            raise Http404("El usuario no existe")

    def get(self, request: Response, pk=0):
        # Note the use of `get_queryset()` instead of `self.queryset`
        if pk > 0:
            user = self.get_object(pk)
            serializer = UserSerializer(user, many=False)
            return Response(data=serializer.data)
        else:
            queryset = self.get_queryset()
            serializer = UserSerializer(queryset, many=True)
            return Response(data=serializer.data)

    def post(self, request: Request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "message": "User Created Successfully",
                "data": serializer.data
            }
            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        if user.delete():
            return Response(status=status.HTTP_200_OK, data={"Borrado con éxito"})
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserUpdate(generics.UpdateAPIView):
    serializer_class = UserSerializer
    model = User
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()

    def get_object(self, pk):
        try:
            return User.objects.get(id=pk)
        except User.DoesNotExist:
            raise Http404("El usuario no existe")

    def put(self, request: Response, pk):
        user = self.get_object(pk)
        serializer = self.serializer_class(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = []

    def post(self, request: Request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)
        if user is not None:
            tokens = create_jwt_pair_for_user(user)
            response = {"message": "Login Successfull", "tokens": tokens}
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            return Response(data={"message": "Invalid email or password"})

    def get(self, request):
        content = {
            "user": str(request.user)
        }
        return Response(data=content, status=status.HTTP_200_OK)


# View prestamos:

class PrestamoCreate(APIView):
    serializerClass = PrestamoSerializer
    model = Prestamo
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = PrestamoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Pendiente:


class PrestamoList(APIView):
    serializer_class = PrestamoSerializer
    model = Prestamo
    permission_classes = [permissions.AllowAny]
    #queryset = Prestamo.objects.all()

    def get(self, request):
        prestamos = list(Prestamo.objects.values())
        if len(prestamos) > 0:
            datos = {'mensaje': 'exitoso', 'prestamos': prestamos}
        else:
            datos = {'mensaje': 'prestamos no encontrados'}
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
