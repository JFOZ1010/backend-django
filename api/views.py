from optparse import Values
from django import views
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from .models import Usuario
# Create your views here.

#creacion de una vista que implementara los requests
class DesarrolloView(View):

    def get(self, request):
        usuarios=list(Usuario.objects.values())
        
        if len(usuarios)>0:
            datos= {'mensaje ': 'Exitoso', 'Usuarios': usuarios}
        else:
            datos = {'mensaje': 'Usuarios no encontrados'}
        
        return JsonResponse(datos)

    def post(self, request):
        pass

    def put(self, request):
        pass

    def delete(self, request):
        pass
