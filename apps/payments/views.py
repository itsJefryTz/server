from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import CurrencyRate, PaymentMethod
from .serializers import CurrencyRateSerializer, PaymentMethodSerializer

class CurrencyRateAPIView(APIView):
  def get(self, request):
    query = CurrencyRate.objects.all()
    return Response(CurrencyRateSerializer(query, many=True).data, status=status.HTTP_200_OK)

class PaymentMethodAPIView(APIView):
  def get(self, request):
    query = PaymentMethod.objects.filter(active=True).prefetch_related('defined_fields')
    return Response(PaymentMethodSerializer(query, many=True).data, status=status.HTTP_200_OK)
