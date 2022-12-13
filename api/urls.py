from django.urls import path
import re
from . import views

# Agrego las rutas a una carpeta usuarios raiz
urlpatterns = [

    ##################################### URL's USUARIOS. ######################################
    path("users/", views.SignUpView.as_view(), name="users"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("users/<int:pk>", views.SignUpView.as_view(), name="user"),
    path("users/modify/<int:pk>", views.UserUpdate.as_view(), name="user_modify"),

    ##################################### URL's AHORROS. ######################################
    #path('ahorros', Ahorros.as_view(), name='ahorros_list'),
    path('ahorros/create', views.AhorrosCreate.as_view(), name='ahorros_create'),
    path('ahorros/all', views.AhorrosList.as_view(), name='ahorros_list'),
    path('ahorros/delete/<int:pk>',
         views.AhorrosDelete.as_view(), name='ahorros_delete'),
    path('ahorros/update/<int:pk>',
         views.AhorrosUpdate.as_view(), name='ahorros_update'),

    ##################################### URL's PRESTAMOS. ######################################
    path('prestamos/create', views.PrestamoCreate.as_view(),
         name='prestamos_create'),
    path('prestamos/', views.PrestamoList.as_view(), name='prestamos_list'),
    path('prestamos/<str:solicitudPrestamo>', views.PrestamoId.as_view(), name='prestamos_id'),
    path('prestamos/delete/<str:solicitudPrestamo>', views.deletePrestamo.as_view(), name='prestamos_delete'),
    path('prestamos/update/<str:solicitudPrestamo>', views.updatePrestamo.as_view(), name='prestamos_update'),
]
