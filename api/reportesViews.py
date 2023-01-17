# Modulos DJANGO
from django.db.models import Sum, Count
import datetime

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

def calDate(_date):
    return datetime.date(
        _date['year'],
        _date['month'],
        _date['day']
    )


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
        ).annotate(
            Enero=Count('fecha')
        ).annotate(
            Total=Sum('monto')
        )
        print(loans_january)
        # loans_february = len(self.model.objects.filter(fecha__month=2))
        # loans_march = len(self.model.objects.filter(fecha__month=3))
        # loans_april = len(self.model.objects.filter(fecha__month=4))
        # loans_may = len(self.model.objects.filter(fecha__month=5))
        # loans_june = len(self.model.objects.filter(fecha__month=6))
        # loans_july = len(self.model.objects.filter(fecha__month=7))
        # loans_august = len(self.model.objects.filter(fecha__month=8))
        # loans_september = len(self.model.objects.filter(fecha__month=9))
        # loans_octuber = len(self.model.objects.filter(fecha__month=10))
        # loans_november = len(self.model.objects.filter(fecha__month=11))
        # loans_december = len(self.model.objects.filter(fecha__month=12))
        # return Response({
        #     "Enero": loans_january,
        #     "Febrero": loans_february,
        #     "Marzo": loans_march,
        #     "Abril": loans_april,
        #     "Mayo": loans_may,
        #     "Junio": loans_june,
        #     "Julio": loans_july,
        #     "Agosto": loans_august,
        #     "Septiembre": loans_september,
        #     "Octubre": loans_octuber,
        #     "Noviembre": loans_november,
        #     "Diciembre": loans_december
        # }, status=status.HTTP_200_OK)
        return Response(loans_january)
