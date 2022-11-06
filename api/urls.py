from django.urls import path
from .views import DesarrolloView

#Agrego las rutas a una carpeta usuarios raiz
urlpatterns=[
    path('usuarios/',DesarrolloView.as_view(),name='usuarios_list')

]