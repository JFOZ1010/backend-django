from django.urls import path
import re
from . import views

# Agrego las rutas a una carpeta usuarios raiz
urlpatterns = [

    ##################################### URL's USUARIOS. ######################################
    path("login/", views.LoginView.as_view(), name="login"),
    path("users/", views.UserListAll.as_view(), name="users_list_all"),
    path("users/create/", views.CreateUserView.as_view(), name="user_create"),
    path("users/view/<int:documento>",
         views.UserView.as_view(), name="user_view"),
    path("users/modify/<int:pk>", views.UserUpdate.as_view(), name="user_modify"),
    path("users/delete/<int:documento>",
         views.UserView.as_view(), name="user_delete"),

    ##################################### URL's AHORROS. ######################################
    # path('ahorros', Ahorros.as_view(), name='ahorros_list'),
    path('ahorros/create', views.AhorrosCreate.as_view(), name='ahorros_create'),
    path('ahorros/all', views.AhorrosList.as_view(), name='ahorros_list'),
    path('ahorros/all/<int:documento>',
         views.AhorroListUser.as_view(), name='ahorros_user'),
    path('ahorros/delete/<int:pk>',
         views.AhorrosDelete.as_view(), name='ahorros_delete'),
    path('ahorros/update/<int:pk>',
         views.AhorrosUpdate.as_view(), name='ahorros_update'),

    ##################################### URL's PRESTAMOS. ######################################
    path('prestamos/create', views.PrestamoCreate.as_view(),
         name='prestamos_create'),
    path('prestamos/', views.PrestamoList.as_view(), name='prestamos_list'),
    path('prestamos/<str:solicitudPrestamo>',
         views.PrestamoId.as_view(), name='prestamos_id'),
     #Url codeudor
    path('prestamos/<str:codeudor>',
         views.IdCodeudor.as_view(), name='codeudor_id'),
    #Url deudor
    path('prestamos/<str:deudor>',
         views.IdDeudor.as_view(), name='deudor_id'),
     #delete
    path('prestamos/delete/<str:solicitudPrestamo>',
         views.deletePrestamo.as_view(), name='prestamos_delete'),
    path('prestamos/update/<str:solicitudPrestamo>',
         views.updatePrestamo.as_view(), name='prestamos_update'),
    ##################################### URL's ABONOS. ######################################
    path('abono/create', views.AbonoView.as_view(), name='abono_create'),
    path("abono/all", views.AbonoListAll.as_view(), name="abono_list_all"),
    path('abono/all/<int:documento>',
         views.AbonoView.as_view(), name='abono_list_user'),
    path('abono/modify/<int:pk>', views.AbonoView.as_view(), name='abono_modify'),
    path('abono/delete/<int:pk>', views.AbonoView.as_view(), name='abono_modify'),

     ##################################### URL's SANCIONES. ######################################
     path('sanciones/create', views.SancionCreate.as_view(), name='sanciones_create'),
     path('sanciones/', views.SancionList.as_view(), name='sanciones_list'),
     path('sancion/update', views.SancionUpdate.as_view(), name='sanciones_update'),
     path('sancion/delete', views.SancionDelete.as_view(), name='sanciones_delete'),
     
]
