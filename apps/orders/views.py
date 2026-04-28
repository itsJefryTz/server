from django.db import transaction

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Order, Item
from apps.services.models import Service, Variant

# Create your views here.
class OrderAPIView(APIView):
  
  def post(self, request):
    """Example request body:
      {
        "order_type": "cart",
        "items": [
          {
            "service_id": 1,
            "variant_id": 1,
            "quantity": 1
          },
          {
            "service_id": 1,
            "variant_id": 2,
            "quantity": 1
          }
        ],
        "payment_method": "Pago Móvil",
        "reference": "0331",
        "phone": "+58 424-6835617",
        "email": "thejefryurdaneta21@gmail.com",
      }
    """
    
    # create order.
    items_data = request.data.get('items', [])
    if not items_data:
      return Response({'message': 'The items list is empty'}, status=status.HTTP_400_BAD_REQUEST)

    try:
      with transaction.atomic():
        created_items = []
            
        for item_data in items_data:
          try:
            service = Service.objects.get(id=item_data.get('service_id'))
            variant = Variant.objects.get(id=item_data.get('variant_id'))
          except (Service.DoesNotExist, Variant.DoesNotExist):
            return Response({
              'message': f"Product or variant not found: ID {item_data.get('service_id')}"
            }, status=status.HTTP_404_NOT_FOUND)
              
          new_item = Item.objects.create(
            service=service,
            variant=variant,
            quantity=item_data.get('quantity', 1)
          )
          created_items.append(new_item)
          
        order = Order.objects.create(
          type=request.data.get('order_type'),
          payment_method=request.data.get('payment_method'),
          reference=request.data.get('reference'),
          phone=request.data.get('phone'),
          email=request.data.get('email')
        )
        
        order.items.set(created_items)

        # send email to user.

        return Response({
          'message': 'Orden creada exitosamente'
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
      return Response({
        'message': 'Ocurrió un error inesperado al procesar la orden'
      }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)