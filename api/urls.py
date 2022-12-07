from django.urls import path
import re
from . import views

# Agrego las rutas a una carpeta usuarios raiz
urlpatterns = [
    path('usuarios', views.Users.as_view(), name='users_list'),

    path('auth', views.Auth.as_view(), name="auth"),

    # Cosultas con id de usuario
    path("usuarios/<int:id>/",
         views.Users.as_view(), name='usuario_id'),

    #Url de prestamos

    path('prestamos/create', views.PrestamoCreate.as_view(), name= 'prestamos_create'),

    path('prestamos/all', views.PrestamoList.as_view(), name= 'prestamos_list'),

]
