from django.urls import path
import re
from . import views

# Agrego las rutas a una carpeta usuarios raiz
urlpatterns = [

    ##################################### URL's USUARIOS. ######################################
    path('usuarios', views.Users.as_view(), name='users_list'),
    path('auth', views.Auth.as_view(), name="auth"),
    # Cosultas con id de usuario
    path("usuarios/<int:id>/",
         views.Users.as_view(), name='usuario_id'),

    ##################################### URL's AHORROS. ######################################    
    #path('ahorros', Ahorros.as_view(), name='ahorros_list'),
    path('ahorros/create', views.AhorrosCreate.as_view(), name='ahorros_create'),
    path('ahorros/all', views.AhorrosList.as_view(), name='ahorros_list'),
    path('ahorros/delete/<int:pk>', views.AhorrosDelete.as_view(), name='ahorros_delete'),
    path('ahorros/update/<int:pk>', views.AhorrosUpdate.as_view(), name='ahorros_update'),

    
    ##################################### URL's ASOCIADOS. ######################################
    path('asociados/create', views.AsociadoCreate.as_view(), name='asociados_create'),
    path('asociados/all', views.AsociadoList.as_view(), name='asociados_list'),

    ##################################### URL's PRESTAMOS. ######################################
    path('prestamos/create', views.PrestamoCreate.as_view(), name= 'prestamos_create'),
    path('prestamos/all', views.PrestamoList.as_view(), name= 'prestamos_list'),
]
