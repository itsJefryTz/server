from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Service
from .serializers import ServiceSerializer

# Create your views here.
class ServiceAPIView(APIView):
  
  def get(self, request):
    service_id = request.query_params.get('id')
    
    if service_id:
      try:
        service = Service.objects.get(id=service_id)
        return Response(ServiceSerializer(service).data)
      except Service.DoesNotExist:
        return Response({"error": "service not found."}, status=status.HTTP_404_NOT_FOUND)
    else:
      services = Service.objects.all()
      return Response(ServiceSerializer(services, many=True).data, status=status.HTTP_200_OK)