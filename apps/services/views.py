import requests

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Service
from .serializers import ServiceSerializer

# Create your views here.
class PlayerLookupView(APIView):
  def get(self, request):
    player_id = request.query_params.get('id')
    game = request.query_params.get('game')
    
    if not player_id or not game:
      return Response({ 'error': 'missing parameters: [player_id] and [game] are required.' }, status=status.HTTP_400_BAD_REQUEST)
    
    if game not in ["Free Fire", "Blood Strike"]:
      return Response({ 'error': 'game not found.' }, status=status.HTTP_404_NOT_FOUND)
    
    if game == "Free Fire":
      url = "https://adzeerstore.com/api/freefire.php?action=verify"
      payload = { "accountId": str(player_id) }
    elif game == "Blood Strike":
      url = "https://adzeerstore.com/api/bloodstrike.php?action=verify"
      payload = { "playerId": str(player_id) }
      
    headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    }
    
    try:
      response = requests.post(url, json=payload, headers=headers, timeout=25)
      response.raise_for_status()
      data = response.json()
      
      return Response({
        'game': game,
        'player_id': player_id,
        'player_name': data.get('playerName')
      }, status=status.HTTP_200_OK)
    except requests.exceptions.ConnectionError:
      return Response({ 
        'error': 'the provider closed the connection. please try again in a few seconds.'
      }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    except requests.exceptions.Timeout:
      return Response({ 
        'error': 'the game server took too long to respond.'
      }, status=status.HTTP_408_REQUEST_TIMEOUT)
    except requests.exceptions.HTTPError:
      return Response({ 
        'error': f"external server error: {response.status_code}"
      }, status=status.HTTP_400_BAD_REQUEST)

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