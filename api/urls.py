from django.urls import path
import re
from . import views

# Agrego las rutas a una carpeta usuarios raiz
urlpatterns = [

    ##################################### URL's USUARIOS. ######################################
    path("users/", views.UserView.as_view(), name="users_list_all"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("users/<int:documento>", views.UserView.as_view(), name="user"),
    path("users/create", views.CreateUserView.as_view(), name="create_user"),
    path("users/modify/<int:pk>", views.UserUpdate.as_view(), name="user_modify"),

    ##################################### URL's AHORROS. ######################################
    #path('ahorros', Ahorros.as_view(), name='ahorros_list'),
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
]
