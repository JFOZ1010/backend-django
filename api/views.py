from optparse import Values
from django import views
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import Usuario
import json
# Create your views here.

#creacion de una vista que implementara los requests
class DesarrolloView(View):

    @method_decorator(csrf_exempt) #Metodo que nos servira para saltar el error de csrf
    #csrf: Es un mecanismo para evitar falsificación entre peticiones de fron end contra backend

    #Metodo para despachar o enviar, cuando se hace una petición
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    #GET
    def get(self, request, idUsuario=0):

        #Busqueda por id
        if (idUsuario>0):
            
            usuarios=list(Usuario.objects.filter(idUsuario=idUsuario).values())

            if len(usuarios)>0:
                usuarioGet= usuarios[0] #dado que por id solo se busca un usuario, ese usr estara en posicion 1
                datos={'mensaje':'Usuario encontrado', 'Usuario':usuarioGet}
            else:
                datos={'Mensaje':'Usuario no encontrado'}
            return JsonResponse(datos)

        #Sino se da el id, se da la lista de usuarios    
        else:
            usuarios=list(Usuario.objects.values())
        
            if len(usuarios)>0:
                datos= {'mensaje ': 'Lista de Usuarios', 'Usuarios': usuarios}
            else:
                datos = {'mensaje': 'Usuarios no encontrados'}
        
            return JsonResponse(datos)

    #POST:Registro
    def post(self, request):
        #print(request.body)
        #jason data
        jd= json.loads(request.body) #Convierte los datos que se registran en un diccionario python
        #print(jd)
        Usuario.objects.create(correoUsr=jd['correoUsr'],admin=jd['admin'], contrasena=jd['contrasena'])
        datos= {'Mensaje':'Registro exitoso'}
        return JsonResponse(datos)

    #PUT: Actualización
    def put(self, request, idUsuario):
        
        #datos cargados
        jd= json.loads(request.body) #Diccionario de los datos de json enviados
        #usuarios = list(Usuario.objects.filter(idUsuario=idUsuario).values())
        usuarios=list(Usuario.objects.filter(idUsuario=idUsuario).values())

        if len(usuarios)>0:
            #Usamos get en vez de filter porque ya estan cargados los datos
            usuarioAct= Usuario.objects.get(idUsuario=idUsuario)

            #Actualización de datos:
            usuarioAct.correoUsr =jd['correoUsr']
            usuarioAct.contrasena = jd['contrasena']
            usuarioAct.save() #guarda los cambios

            datos={'Mensaje':'Actualizacion exitosa'}

        else:
            datos={'Mensaje':'Usuario no encontrado'}
        
        return JsonResponse(datos)

    #DELETE: Eliminar
    def delete(self, request, idUsuario):
        usuarios= list(Usuario.objects.filter(idUsuario=idUsuario).values())

        if len(usuarios)>0:
            Usuario.objects.filter(idUsuario=idUsuario).delete()
            datos={'Mensaje': 'Usuario Eliminado'}
        else:
            datos={'Mensaje': 'Usuario no encontrado'}
        
        return JsonResponse(datos)
        

