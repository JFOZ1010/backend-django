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
from api.models import Abono, User, Ahorro, Prestamo, Multa, Reunion, ReunionVirtual, ReunionPresencial, Cliente
from api.serializer import UserSerializer, AhorroSerializer, PrestamoSerializer, AbonoSerializer, SancionSerializer, ReunionSerializer, ReunionPresencialSerializer, ReunionVirtualSerializer, ClienteSerializer
from .tokens import create_jwt_pair_for_user

# modulos nuevos que importo del framework DRF.
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status, generics
from rest_framework import authentication, permissions
from rest_framework.exceptions import NotFound


# View de User.

@method_decorator(csrf_exempt, name='dispatch')
class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request: Request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "message": "Usuario creado correctamente",
                "data": serializer.data
            }
            return Response(response)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class UserView(generics.GenericAPIView):
    serializer_class = UserSerializer
    model = User
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, documento):
        try:
            return self.model.objects.get(documento=documento)
        except self.model.DoesNotExist:
            raise Http404("El usuario no existe")

    def get(self, *args, **kwargs):
        documento = self.kwargs.get("documento")
        user = self.get_object(documento)
        serializer = self.serializer_class(user, many=False)
        return Response(data=serializer.data)

    def delete(self, *args, **kwargs):
        documento = self.kwargs.get("documento")
        user = self.get_object(documento)
        if user.delete():
            return Response(status=status.HTTP_200_OK, data={"Borrado con éxito"})
        return Response(status=status.HTTP_204_NO_CONTENT)


@method_decorator(csrf_exempt, name='dispatch')
class ListUserAllView(generics.ListAPIView):
    serializer_class = UserSerializer
    model = User
    permission_classes = [permissions.IsAuthenticated]
    queryset = model.objects.all()


@method_decorator(csrf_exempt, name='dispatch')
class UpdateClienteView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    model = User
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return self.model.objects.get(documento=pk)
        except self.model.DoesNotExist:
            raise Http404("El usuario no existe")

    def put(self, request: Response, pk):
        user = self.get_object(pk)
        serializer = self.serializer_class(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# View de Cliente


@method_decorator(csrf_exempt, name='dispatch')
class CreateClienteView(generics.CreateAPIView):
    serializer_class = ClienteSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request: Request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "message": "Cliente creado correctamente",
                "data": serializer.data
            }
            return Response(response)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class ClienteView(generics.GenericAPIView):
    serializer_class = ClienteSerializer
    model = Cliente
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, documento):
        try:
            return self.model.objects.get(documento=documento)
        except self.model.DoesNotExist:
            raise Http404("El cliente no existe")

    def get(self, *args, **kwargs):
        documento = self.kwargs.get("documento")
        cliente = self.get_object(documento)
        serializer = self.serializer_class(cliente, many=False)
        return Response(data=serializer.data)

    def delete(self, *args, **kwargs):
        documento = self.kwargs.get("documento")
        cliente = self.get_object(documento)
        if cliente.delete():
            return Response(status=status.HTTP_200_OK, data={"Borrado con éxito"})
        return Response(status=status.HTTP_204_NO_CONTENT)


@method_decorator(csrf_exempt, name='dispatch')
class ListClientetAllView(generics.ListAPIView):
    serializer_class = ClienteSerializer
    model = Cliente
    permission_classes = [permissions.IsAuthenticated]
    queryset = model.objects.all()


@method_decorator(csrf_exempt, name='dispatch')
class UpdateClienteView(generics.UpdateAPIView):
    serializer_class = ClienteSerializer
    model = Cliente
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return self.model.objects.get(documento=pk)
        except self.model.DoesNotExist:
            raise Http404("El usuario no existe")

    def put(self, request: Response, pk):
        user = self.get_object(pk)
        serializer = self.serializer_class(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    permission_classes = []

    def post(self, request: Request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)
        if user is not None:
            tokens = create_jwt_pair_for_user(user)
            serializer = UserSerializer(user, many=False)
            response = {
                "status": True,
                "message": "Logueado correctamente",
                "tokens": tokens,
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(data={
                "status": False,
                "message": "Invalid email or password"
            })

    def get(self, request):
        content = {
            "user": str(request.user),
            "auth": str(request.auth)
        }
        return Response(data=content, status=status.HTTP_200_OK)

# View prestamos:


@method_decorator(csrf_exempt, name='dispatch')
class PrestamoCreate(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]

# crear un metodo POST con un try except para el manejo de errores
    def post(self, request):
        # crear un objeto de la clase PrestamoSerializer, pasandole como parametro el request.data
        serializer = PrestamoSerializer(data=request.data)
    # si el serializer es valido
        if serializer.is_valid():
            # guardar el serializer
            serializer.save()
        # retornar el serializer.data, y el status de la peticion
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    # si el serializer no es valido, retornar el serializer.errors, y el status de la peticion
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Pendiente:

# Lista de prestamos
class PrestamoList(generics.ListAPIView):
    serializer_class = PrestamoSerializer
    model = Prestamo
    permission_classes = [permissions.AllowAny]
    # queryset = Prestamo.objects.all()

    def get(self, request):
        prestamos = list(Prestamo.objects.values())
        if len(prestamos) > 0:
            datos = {'mensaje': 'Si existen prestamos', 'prestamos': prestamos}
        else:
            datos = {'mensaje': 'prestamos no encontrados'}
        return JsonResponse(datos)

# Prestamos filtrados por su id:


@method_decorator(csrf_exempt, name='dispatch')
class PrestamoId(generics.GenericAPIView):

    serializer_class = PrestamoSerializer
    model = Prestamo
    permission_classes = [permissions.AllowAny]
    queryset = Prestamo.objects.all()

    def getPrestamo(self, idPrestamo):
        try:
            return Prestamo.objects.get(id=idPrestamo)
        except Prestamo.DoesNotExist:
            raise Http404("El Prestamo no existe")

    def get(self, request: Response, idPrestamo=0):

        prestamo = self.getPrestamo(idPrestamo)
        serializer = PrestamoSerializer(prestamo, many=False)
        return Response(data=serializer.data)

# Busqueda del prestamo por documentos
# Codeudor
@method_decorator(csrf_exempt, name='dispatch')
class IdCodeudor(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PrestamoSerializer
    model = Prestamo

    def get_queryset(self):
        user= self.kwargs['codeudor']
        print(user)
        return Prestamo.objects.filter(codeudor_id=user).all()

# Busqueda del prestamo por documentos
# Deudor
@method_decorator(csrf_exempt, name='dispatch')
class IdDeudor(generics.ListAPIView):

    permission_classes = [permissions.AllowAny]
    serializer_class = PrestamoSerializer
    model = Prestamo

    def get_queryset(self):
        user= self.kwargs['deudor']
        print(user)
        print(len(Prestamo.objects.filter(deudor_id=user).all()))
        return Prestamo.objects.filter(deudor_id=user).all()



# Delete Prestamo


class deletePrestamo(generics.GenericAPIView):

    serializer_class = PrestamoSerializer
    model = Prestamo
    permission_classes = [permissions.AllowAny]
    queryset = Prestamo.objects.all()

    def getPrestamo(self, idPrestamo):
        try:
            return Prestamo.objects.get(id=idPrestamo)
        except Prestamo.DoesNotExist:
            raise Http404("El Prestamo no existe")

    def delete(self, request, idPrestamo=0, format=None):
        prestamo = self.getPrestamo(idPrestamo)

        if prestamo.delete():
            return Response(status=status.HTTP_200_OK, data={"Borrado con éxito"})
        return Response(status=status.HTTP_204_NO_CONTENT)

# Actualizar o Put Prestamo


@method_decorator(csrf_exempt, name='dispatch')
class updatePrestamo(generics.UpdateAPIView):
    serializer_class = PrestamoSerializer
    model = Prestamo
    permission_classes = [permissions.AllowAny]

    def getPrestamo(self, idPrestamo):
        try:
            return Prestamo.objects.get(id=idPrestamo)
        except Prestamo.DoesNotExist:
            raise NotFound(detail='Prestamo no existe')

    def put(self, *args, **kwargs):
        soliPrestamo = self.kwargs.get('idPrestamo')
        print(soliPrestamo)
        prestamo = self.getPrestamo(soliPrestamo)
        serializer = self.serializer_class(prestamo, data=self.request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""SESION DEDICADA A AHORROS, Y TODO LO RELACIONADO CON ESTE"""

# crear una vista para crear Ahorros, con el metodo post tomando como la APIView


@method_decorator(csrf_exempt, name='dispatch')
class AhorrosCreate(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]

    # crear un metodo POST con un try except para el manejo de errores
    def post(self, request):
        # crear un objeto de la clase AhorroSerializer, pasandole como parametro el request.data
        serializer = AhorroSerializer(data=request.data)
        # si el serializer es valido
        if serializer.is_valid():
            # guardar el serializer
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# CLASE LISTAR
class AhorrosList(generics.ListAPIView):
    serializer_class = AhorroSerializer
    model = Ahorro
    permission_classes = [permissions.AllowAny]
    queryset = Ahorro.objects.all()


# un ahorro list de un user especifico con un filter.
class AhorroListUser(generics.RetrieveAPIView):
    serializer_class = AhorroSerializer
    model = Ahorro
    permission_classes = [permissions.IsAuthenticated]

    def get(self, *args, **kwargs):
        documento = self.kwargs.get('documento')
        queryset = Ahorro.objects.filter(DocAsociado=documento).all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)


# CLASE ACTUALIZAR
class AhorrosUpdate(generics.UpdateAPIView):
    serializer_class = AhorroSerializer
    model = Ahorro
    permission_classes = [permissions.IsAuthenticated]
    # queryset = Ahorro.objects.all()

    def get_object(self, pk):
        try:
            return Ahorro.objects.get(pk=pk)
        except Ahorro.DoesNotExist:
            raise NotFound(detail="El ahorro no existe")

    def put(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        ahorro = self.get_object(pk)
        serializer = self.serializer_class(ahorro, data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# CLASE ELIMINAR
class AhorrosDelete(generics.DestroyAPIView):
    serializer_class = AhorroSerializer
    model = Ahorro
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Ahorro.objects.get(pk=pk)
        except Ahorro.DoesNotExist:
            raise NotFound(detail="El ahorro no existe")

    def delete(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        ahorro = self.get_object(pk)
        if ahorro.delete():
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response(data={
                "No existe el ahorro"
            }, status=status.HTTP_204_NO_CONTENT)


# Sección de abono


# Creación de abono
@ method_decorator(csrf_exempt, name='dispatch')
class AbonoView(generics.GenericAPIView):
    serializer_class = AbonoSerializer
    model = Abono
    permission_classes = [permissions.AllowAny]

    def get_object(self, pk):
        try:
            return self.model.objects.get(idAbono=pk)
        except self.model.DoesNotExist:
            raise NotFound(detail="El abono no existe")

    def post(self, request: Response):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_204_NO_CONTENT)

    def get(self, *args, **kwargs):
        documento = self.kwargs.get('documento')
        queryset = self.model.objects.filter(abona=documento).all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)

    def put(self, request: Request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        abono = self.get_object(pk)
        serializer = self.serializer_class(instance=abono, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_204_NO_CONTENT)

    def delete(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        abono = self.get_object(pk)
        if abono.delete():
            return Response(status=status.HTTP_200_OK, data={"Borrado con éxito"})
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


@ method_decorator(csrf_exempt, name='dispatch')
class AbonoListAll(generics.ListAPIView):
    serializer_class = AbonoSerializer
    model = Abono
    permission_classes = [permissions.AllowAny]
    queryset = model.objects.all()


""" SESIÓN DEDICADA SOLO A SANCIONES. """


class SancionCreate(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    # crear un metodo POST con un try except para el manejo de errores
    def post(self, request):
        # crear un objeto de la clase SancionSerializer, pasandole como parametro el request.data
        serializer = SancionSerializer(data=request.data)
        # si el serializer es valido
        if serializer.is_valid():
            # guardar el serializer
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# una class de sancion list


class SancionList(generics.ListAPIView):
    serializer_class = SancionSerializer
    model = Multa
    permission_classes = [permissions.IsAuthenticated]
    queryset = Multa.objects.all()

# una class de sancion list de un user especifico con un filter (asociado Referente)


class SancionListUser(generics.RetrieveAPIView):
    serializer_class = SancionSerializer
    model = Multa
    permission_classes = [permissions.IsAuthenticated]

    def get(self, *args, **kwargs):
        documento = self.kwargs.get('documento')
        queryset = Multa.objects.filter(asociadoReferente=documento).all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)

# una class de sancion update


class SancionUpdate(generics.UpdateAPIView):
    serializer_class = SancionSerializer
    model = Multa
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Multa.objects.get(pk=pk)
        except Multa.DoesNotExist:
            raise NotFound(detail="La sanción no existe")

    def put(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        sancion = self.get_object(pk)
        serializer = self.serializer_class(sancion, data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# una class de sancion delete


class SancionDelete(generics.DestroyAPIView):
    serializer_class = SancionSerializer
    model = Multa
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Multa.objects.get(pk=pk)
        except Multa.DoesNotExist:
            raise NotFound(detail="La sanción no existe")

    def delete(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        sancion = self.get_object(pk)
        if sancion.delete():
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response(data={
                "No existe la sanción"
            }, status=status.HTTP_204_NO_CONTENT)


################## Sección de reuniones ##################

# Creación de reunión
@ method_decorator(csrf_exempt, name='dispatch')
class ReunionVirtualCreateView(generics.CreateAPIView):
    serializer_class = ReunionVirtualSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request: Request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "message": "Reunion creada correctamente",
                "data": serializer.data
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReunionPresencialCreateView(generics.CreateAPIView):
    serializer_class = ReunionPresencialSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request: Request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "message": "Reunion creada correctamente",
                "data": serializer.data
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class ReunionPresencialListAll(generics.ListAPIView):
    serializer_class = ReunionPresencialSerializer
    model = ReunionPresencial
    permission_classes = [permissions.AllowAny]
    queryset = model.objects.all()


@method_decorator(csrf_exempt, name='dispatch')
class ReunionVirtualListAll(generics.ListAPIView):
    serializer_class = ReunionVirtualSerializer
    model = ReunionVirtual
    permission_classes = [permissions.AllowAny]
    queryset = model.objects.all()


@method_decorator(csrf_exempt, name='dispatch')
class ReunionPresencialUpdateView(generics.UpdateAPIView):
    serializer_class = ReunionPresencialSerializer
    model = ReunionPresencial
    permission_classes = [permissions.AllowAny]

    def get_object(self, id):
        try:
            return self.model.objects.get(pk=id)
        except self.model.DoesNotExist:
            raise Http404("La reunión no existe")

    def put(self, request: Request, id):
        reunionPresencial = self.get_object(id)
        serializer = self.serializer_class(
            instance=reunionPresencial, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class ReunionVirtualUpdateView(generics.UpdateAPIView):
    serializer_class = ReunionVirtualSerializer
    model = ReunionVirtual
    permission_classes = [permissions.AllowAny]

    def get_object(self, id):
        try:
            return self.model.objects.get(pk=id)
        except self.model.DoesNotExist:
            raise Http404("La reunión no existe")

    def put(self, request: Request, id):
        reunionPresencial = self.get_object(id)
        serializer = self.serializer_class(
            instance=reunionPresencial, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class ReunionPresencialDeleteView(generics.DestroyAPIView):
    serializer_class = ReunionPresencialSerializer
    model = ReunionPresencial
    permission_classes = [permissions.AllowAny]

    def get_object(self, id):
        try:
            return self.model.objects.get(pk=id)
        except self.model.DoesNotExist:
            raise Http404("La reunión no existe")

    def delete(self, request: Request, id):
        user = self.get_object(id)
        if user.delete():
            return Response(status=status.HTTP_200_OK, data={"Borrado con éxito"})
        return Response(status=status.HTTP_204_NO_CONTENT)


@method_decorator(csrf_exempt, name='dispatch')
class ReunionVirtualDeleteView(generics.DestroyAPIView):
    serializer_class = ReunionVirtualSerializer
    model = ReunionVirtual
    permission_classes = [permissions.AllowAny]

    def get_object(self, id):
        try:
            return self.model.objects.get(pk=id)
        except self.model.DoesNotExist:
            raise Http404("La reunión no existe")

    def delete(self, request: Request, id):
        user = self.get_object(id)
        if user.delete():
            return Response(status=status.HTTP_200_OK, data={"Borrado con éxito"})
        return Response(status=status.HTTP_204_NO_CONTENT)
