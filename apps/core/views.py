from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import CurrencyRate
from .serializers import CurrencyRateSerializer

# Create your views here.
class CurrencyRateAPIView(APIView):
  
  def get(self, request):
    query = CurrencyRate.objects.all()
    
    return Response({
      'message': 'success',
      'data': CurrencyRateSerializer(query, many=True).data
    }, status=status.HTTP_200_OK)