from django.urls import path
import re
from . import views

# Agrego las rutas a una carpeta usuarios raiz
urlpatterns = [
    path('usuarios/', views.DesarrolloView.as_view(), name='usuarios_list'),
    # Cosultas con id de usuario
    path(r"^usuarios/(?P<value>\d+)/$",
         views.DesarrolloView.as_view(), name='usuario_id'),
]
