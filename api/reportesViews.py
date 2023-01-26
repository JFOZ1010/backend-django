# Modulos DJANGO
from django.db.models import Sum, Count, F
import datetime
import json

# Modulos locales
from api.models import Abono, User, Ahorro, Prestamo, Multa, Reunion, ReunionVirtual, ReunionPresencial, Cliente
from api.serializer import PrestamoSerializer, AhorroSerializer, ReunionSerializer

# modulos nuevos que importo del framework DRF.
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework import permissions


# Definicion de funciones y clases para reportes


# calDate se devuelve un date de fecha para utilizar en la clase Range_date
def calDate(_date):
    return datetime.date(
        _date['year'],
        _date['month'],
        _date['day']
    )

# Range_date se encarga de recibir la resquest.data de una petición
# para sacar la fecha de inicio y fecha de fin para calcular el rango
# de manera dinamica.


class Range_date():

    def __init__(self, date_start, date_end):
        self.date_start = date_start
        self.date_end = date_end

    def calDate_start(self):
        if self.date_start['fechaInicio']:
            self.date_start = calDate(self.date_start['fechaInicio'])
            return self.date_start
        else:
            raise ValueError(
                'No es una fecha válida'
            )

    def calDate_end(self):
        if self.date_end['fechaFin']:
            self.date_end = calDate(self.date_end['fechaFin'])
            return self.date_end
        else:
            raise ValueError(
                'No es una fecha válida'
            )


# Definiciones de clases para reportes

# Meses en los que se presentaron más préstamos (Top 10)
class Reporte_MesMasPrestamos(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    model = Prestamo

    def get(self, request):
        loans_january = len(self.model.objects.filter(fecha__month=1))
        loans_february = len(self.model.objects.filter(fecha__month=2))
        loans_march = len(self.model.objects.filter(fecha__month=3))
        loans_april = len(self.model.objects.filter(fecha__month=4))
        loans_may = len(self.model.objects.filter(fecha__month=5))
        loans_june = len(self.model.objects.filter(fecha__month=6))
        loans_july = len(self.model.objects.filter(fecha__month=7))
        loans_august = len(self.model.objects.filter(fecha__month=8))
        loans_september = len(self.model.objects.filter(fecha__month=9))
        loans_octuber = len(self.model.objects.filter(fecha__month=10))
        loans_november = len(self.model.objects.filter(fecha__month=11))
        loans_december = len(self.model.objects.filter(fecha__month=12))

        loans_len = {
            "Enero": loans_january,
            "Febrero": loans_february,
            "Marzo": loans_march,
            "Abril": loans_april,
            "Mayo": loans_may,
            "Junio": loans_june,
            "Julio": loans_july,
            "Agosto": loans_august,
            "Septiembre": loans_september,
            "Octubre": loans_octuber,
            "Noviembre": loans_november,
            "Diciembre": loans_december
        }
        sorted_loans_len = sorted(
            loans_len.items(), key=lambda x: x[1], reverse=True)
        sorted_loans_len = dict(sorted_loans_len[0:10])

        return Response(sorted_loans_len, status=status.HTTP_200_OK)

# Top de Asociados que más ahorrado


class Reporte_MasAhorros(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    model = Ahorro

    def get(self, request):
        ahorro_max = self.model.objects.values(
            'DocAsociado_id'
        ).filter(
            DocAsociado_id__rol__exact='asociado'
        ).order_by(
            'DocAsociado_id'
        ).annotate(
            ahorrado=Sum('monto')
        )
        return Response(data=ahorro_max)

# Reuniones por fecha (fecha inicial - fecha final)


class Reporte_ReunionesFechas(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    model = Reunion
    serializer_class = ReunionSerializer

    def get(self, request: Request):
        print(repr(request.data))
        _date = Range_date(request.data, request.data)
        start_date = _date.calDate_start()
        end_date = _date.calDate_end()
        reuniones_range = self.model.objects.filter(
            fecha__range=(start_date, end_date)
        )
        serialezer = self.serializer_class(reuniones_range, many=True)
        return Response(
            data={
                "data": serialezer.data,
                "cantidad": len(serialezer.data)
            }, status=status.HTTP_200_OK)

# Monto de préstamos por meses


class Reporte_MontoMesPrestamo(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    model = Prestamo

    def get(self, request):
        loans_january = self.model.objects.filter(
            fecha__month=1
        ).aggregate(january=Sum('monto'))['january']
        loans_february = self.model.objects.filter(
            fecha__month=2
        ).aggregate(february=Sum('monto'))['february']
        loans_march = self.model.objects.filter(
            fecha__month=3
        ).aggregate(march=Sum('monto'))['march']
        loans_april = self.model.objects.filter(
            fecha__month=4
        ).aggregate(april=Sum('monto'))['april']
        loans_may = self.model.objects.filter(
            fecha__month=5
        ).aggregate(may=Sum('monto'))['may']
        loans_june = self.model.objects.filter(
            fecha__month=6
        ).aggregate(june=Sum('monto'))['june']
        loans_july = self.model.objects.filter(
            fecha__month=7
        ).aggregate(july=Sum('monto'))['july']
        loans_august = self.model.objects.filter(
            fecha__month=8
        ).aggregate(august=Sum('monto'))['august']
        loans_september = self.model.objects.filter(
            fecha__month=9
        ).aggregate(september=Sum('monto'))['september']
        loans_octuber = self.model.objects.filter(
            fecha__month=10
        ).aggregate(octuber=Sum('monto'))['octuber']
        loans_november = self.model.objects.filter(
            fecha__month=11
        ).aggregate(november=Sum('monto'))['november']
        loans_december = self.model.objects.filter(
            fecha__month=12
        ).aggregate(december=Sum('monto'))['december']

        loans_january = 0 if loans_january == None else loans_january
        loans_february = 0 if loans_february == None else loans_february
        loans_march = 0 if loans_march == None else loans_march
        loans_april = 0 if loans_april == None else loans_april
        loans_may = 0 if loans_may == None else loans_may
        loans_june = 0 if loans_june == None else loans_june
        loans_july = 0 if loans_july == None else loans_july
        loans_august = 0 if loans_august == None else loans_august
        loans_september = 0 if loans_september == None else loans_september
        loans_octuber = 0 if loans_octuber == None else loans_octuber
        loans_november = 0 if loans_november == None else loans_november
        loans_december = 0 if loans_december == None else loans_december

        return Response(data={
            "Enero": loans_january,
            "Febrero": loans_february,
            "Marzo": loans_march,
            "Abril": loans_april,
            "Mayo": loans_may,
            "Junio": loans_june,
            "Julio": loans_july,
            "Agosto": loans_august,
            "Septiembre": loans_september,
            "Octubre": loans_octuber,
            "Noviembre": loans_november,
            "Diciembre": loans_december
        }, status=status.HTTP_200_OK)

# Clientes que más préstamos realizan (fecha inicial - fecha final)


class Reporte_ClientesMasPrestamoMes(generics.GenericAPIView):
    model = Prestamo
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        _date = Range_date(request.data, request.data)
        start_date = _date.calDate_start()
        end_date = _date.calDate_end()
        clientes = self.model.objects.values(
            'deudor'
        ).filter(
            fecha__range=(start_date, end_date),
            deudor__rol__exact='cliente'
        ).annotate(
            prestamos=Count('deudor', distinct=False)
        )
        return Response(data=clientes, status=status.HTTP_200_OK)

# Author: JFx0Z0r - Juan Felipe Osorio.


class Reporte_AsociadoPorPrestamo(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    model = Prestamo

    def get(self, request):
        _date = Range_date(request.data, request.data)
        start_date = _date.calDate_start()
        #start_date = datetime.date(2023,1,1)
        #end_date = datetime.date(2023,1,31)
        end_date = _date.calDate_end()
        asociados = self.model.objects.values(
            'deudor'
        ).filter(
            fecha__range=(start_date, end_date),
            deudor__rol__exact='asociado'
        ).annotate(
            prestamos=Count('deudor', distinct=False)
        )
        return Response(data=asociados, status=status.HTTP_200_OK)

# reporte de cantidad de multas por Asociados.
# Author: JFx0Z0r - Juan Felipe Osorio.


class Reporte_MultasPorAsociado(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    model = Multa

    def get(self, request):
        _date = Range_date(request.data, request.data)
        start_date = _date.calDate_start()
        end_date = _date.calDate_end()
        #start_date = datetime.date(2023,1,1)
        #end_date = datetime.date(2023,1,31)
        multas = self.model.objects.values(
            'asociadoReferente'
        ).filter(
            fecha__range=(start_date, end_date),
            #asociado__rol__exact = 'asociadoReferente'
        ).annotate(
            cantidad=Count('asociadoReferente', distinct=False)
        )
        return Response(data=multas, status=status.HTTP_200_OK)
