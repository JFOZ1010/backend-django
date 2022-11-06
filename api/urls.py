from django.urls import path
from .views import DesarrolloView

#Agrego las rutas a una carpeta usuarios raiz
urlpatterns=[
    path('usuarios/',DesarrolloView.as_view(),name='usuarios_list'),
    #Para poder hacer consultas con el id del usr
    path('usuarios/<int:idUsuario>',DesarrolloView.as_view(),name='usuario_id'),

]