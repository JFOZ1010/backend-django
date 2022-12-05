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

    ##################################### URL's AHORROS. ######################################    
    #path('ahorros', Ahorros.as_view(), name='ahorros_list'),
    path('ahorros/create', views.AhorrosCreate.as_view(), name='ahorros_create'),
    path('ahorros/all', views.AhorrosList.as_view(), name='ahorros_list'),
    path('ahorros/delete/<int:pk>', views.AhorrosDelete.as_view(), name='ahorros_delete'),
    path('ahorros/update/<int:pk>', views.AhorrosUpdate.as_view(), name='ahorros_update'),

    
    ##################################### URL's ASOCIADOS. ######################################
    path('asociados/create', views.AsociadoCreate.as_view(), name='asociados_create'),
    path('asociados/all', views.AsociadoList.as_view(), name='asociados_list'),
]


"""
    path('New/create/',addNews.as_view()),
    path('New/all/',allNew.as_view()),
    path('New/delete/<str:pk>/',DeleteNew.as_view(), name="delete"),
    path('New/update/<str:pk>/',UpdateNew.as_view(), name = "update"),
    path('New/get/<str:pk>',NewGet.as_view(), name = 'newGet'),
"""