from django.urls import path
import re
from . import views, reportesViews

# Agrego las rutas a una carpeta usuarios raiz
urlpatterns = [

    ##################################### URL's USUARIOS. ######################################
    path("login/", views.LoginView.as_view(), name="login"),
    path("users/", views.ListUserAllView.as_view(), name="users_list_all"),
    path("users/create/", views.CreateUserView.as_view(), name="user_create"),
    path("users/view/<int:documento>",
         views.UserView.as_view(), name="user_view"),
    path("users/modify/<int:pk>",
         views.UpdateClienteView.as_view(), name="user_modify"),
    path("users/delete/<int:documento>",
         views.UserView.as_view(), name="user_delete"),

    ##################################### URL's CLIENTES. ######################################
    path("clientes/", views.ListClientetAllView.as_view(),
         name="clientes_list_all"),
    path("clientes/create/", views.CreateClienteView.as_view(),
         name="cliente_create"),
    path("clientes/view/<int:documento>",
         views.ClienteView.as_view(), name="cliente_view"),
    path("clientes/modify/<int:pk>",
         views.UpdateClienteView.as_view(), name="cliente_modify"),
    path("clientes/delete/<int:documento>",
         views.ClienteView.as_view(), name="cliente_delete"),

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
    # Urls##################

    ##################################### URL's PRESTAMOS. ######################################
    path('prestamos/create', views.PrestamoCreate.as_view(),
         name='prestamos_create'),
    path('prestamos/', views.PrestamoList.as_view(), name='prestamos_list'),
    path('prestamos/<str:idPrestamo>',
         views.PrestamoId.as_view(), name='prestamos_id'),
    # Url codeudor
    path('prestamos/codeudor/<str:codeudor>',
         views.IdCodeudor.as_view(), name='codeudor_id'),
    # Url deudor
    path('prestamos/deudor/<str:deudor>',
         views.IdDeudor.as_view(), name='deudor_id'),
    # delete
    path('prestamos/delete/<str:idPrestamo>',
         views.deletePrestamo.as_view(), name='prestamos_delete'),
    path('prestamos/update/<str:idPrestamo>',
         views.updatePrestamo.as_view(), name='prestamos_update'),
    ##################################### URL's ABONOS. ######################################
    path('abono/create', views.AbonoView.as_view(), name='abono_create'),
    path("abono/all", views.AbonoListAll.as_view(), name="abono_list_all"),
    path('abono/all/<int:documento>',
         views.AbonoView.as_view(), name='abono_list_user'),
    path('abono/modify/<int:pk>', views.AbonoView.as_view(), name='abono_modify'),
    path('abono/delete/<int:pk>', views.AbonoView.as_view(), name='abono_modify'),

    ##################################### URL's SANCIONES. ######################################
    path('sanciones/create', views.SancionCreate.as_view(),
         name='sanciones_create'),
    path('sanciones/all', views.SancionList.as_view(), name='sanciones_list'),
    path('sanciones/<str:documento>',
         views.SancionListUser.as_view(), name='sanciones_user'),
    path('sancion/update/<int:pk>',
         views.SancionUpdate.as_view(), name='sanciones_update'),
    path('sancion/delete/<int:pk>',
         views.SancionDelete.as_view(), name='sanciones_delete'),

    ##################################### URL's Reuniones. ######################################
    path('reuniones-presencial/create', views.ReunionPresencialCreateView.as_view(),
         name='reunionesPresencial_create'),
    path('reuniones-virtual/create', views.ReunionVirtualCreateView.as_view(),
         name='reunionesVirtual_create'),
    path("reuniones-presencial/all",
         views.ReunionPresencialListAll.as_view(), name="reunionesPresencial_listAll"),
    path("reuniones-virtual/all", views.ReunionVirtualListAll.as_view(),
         name="reunionesVirtual_listAll"),
    path("reuniones-presencial/update/<int:id>",
         views.ReunionPresencialUpdateView.as_view(), name="reunionesPresencial_update"),
    path("reuniones-virtual/update/<int:id>",
         views.ReunionVirtualUpdateView.as_view(), name="reunionesVirtual_update"),
    path("reuniones-presencial/delete/<int:id>",
         views.ReunionPresencialDeleteView.as_view(), name="reunionesPresencial_delete"),
    path("reuniones-virtual/delete/<int:id>",
         views.ReunionVirtualDeleteView.as_view(), name="reunionesVirtual_delete"),

######################################## REPORTES. ################################################
    path("reportes/prestamotop",
         reportesViews.Reporte_MesMasPrestamos.as_view(), name='top_prestamo'),
    path("reportes/ahorrotop",
         reportesViews.Reporte_MasAhorros.as_view(), name='max_ahorros'),
    path("reporte/fechasreunion",
         reportesViews.Reporte_ReunionesFechas.as_view(), name='fecha_reuniones'),
    path("reportes/prestamosmes",
         reportesViews.Reporte_MontoMesPrestamo.as_view(), name='monto_prestamos_mes'),
    path("reportes/prestamostopclientes",
         reportesViews.Reporte_ClientesMasPrestamoMes.as_view(), name='clientes_mas_prestamos_mes'), 
    path("reportes/prestamoAsociado", reportesViews.Reporte_AsociadoPorPrestamo.as_view(), name='asociado_por_prestamo'),
    path("reportes/multasAsociado", reportesViews.Reporte_MultasPorAsociado.as_view(), name='multas_por_asociado')

]
