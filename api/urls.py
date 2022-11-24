from django.urls import path
import re
from . import views

# Agrego las rutas a una carpeta usuarios raiz
urlpatterns = [
    path('usuarios', views.DesarrolloView.as_view(), name='users_list'),

    path('auth', views.Auth.as_view(), name="auth"),

    path('example', views.ExampleAuth.as_view(), name='example_auth'),
    # Cosultas con id de usuario
    path(r"^usuarios/(?P<value>\d+)/$",
         views.DesarrolloView.as_view(), name='usuario_id'),
]
