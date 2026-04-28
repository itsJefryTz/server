from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Service
from .serializers import ServiceSerializer

# Create your views here.
class ServiceAPIView(APIView):
  
  def get(self, request):
    service_id = request.query_params.get('id')
    #
    queryset = Service.objects.select_related('category').prefetch_related('variants')
    
    if service_id:
      service = queryset.filter(id=service_id).first()
      if not service:
        return Response({"error": "service not found."}, status=status.HTTP_404_NOT_FOUND)
      return Response(ServiceSerializer(service).data)
    else:
      services = queryset.all()
      return Response(ServiceSerializer(services, many=True).data, status=status.HTTP_200_OK)