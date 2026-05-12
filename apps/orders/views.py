from decimal import Decimal
from django.db import transaction
from django.template.loader import render_to_string
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Order, Item
from apps.services.models import Service, Variant
from apps.core.models import CurrencyRate
from apps.core.utils import send_email_async

class OrderAPIView(APIView):
  def post(self, request):
    raw_items = request.data.get('items', [])
    items_data = [item for item in raw_items if isinstance(item, dict)]

    if not items_data:
      return Response({'message': 'The items list is empty or invalid'}, status=status.HTTP_400_BAD_REQUEST)

    try:
      variant_ids = [item.get('variant_id') for item in items_data if item.get('variant_id')]
      variants_query = Variant.objects.filter(id__in=variant_ids)
      
      prices_dict = {v.id: v.price for v in variants_query}
      variants_dict = {v.id: v for v in variants_query}
      
      service_ids = [item.get('service_id') for item in items_data if item.get('service_id')]
      services_dict = {s.id: s for s in Service.objects.filter(id__in=service_ids)}

      total_amount = Decimal('0.00')
      for item in items_data:
        v_id = item.get('variant_id')
        qty = int(item.get('quantity', 0))
        total_amount += Decimal(qty) * Decimal(prices_dict.get(v_id, 0))

      with transaction.atomic():
        currency_code = request.data.get('currency', 'US')
        try:
          currencyRate_obj = CurrencyRate.objects.get(code=currency_code)
          rate = currencyRate_obj.rate
        except CurrencyRate.DoesNotExist:
          rate = Decimal('1.00')

        order = Order.objects.create(
          type=request.data.get('order_type'),
          payment_method=f"{request.data.get('payment_method')} ({request.data.get('currency')} - {rate})",
          total_amount=total_amount,
          total_amount_converted=total_amount * rate,
          reference=request.data.get('reference'),
          phone=request.data.get('phone'),
          email=request.data.get('email')
        )

        for item_data in items_data:
          service = services_dict.get(item_data.get('service_id'))
          variant = variants_dict.get(item_data.get('variant_id'))
          
          if not service or not variant:
            raise ValueError(f"Not found: {item_data.get('variant_id')}")

          delivery_list = item_data.get('delivery_details', [])
          for credentials in delivery_list:
            if not isinstance(credentials, dict): continue

            is_id = variant.delivery_method == 'id'
            summary = (
              f"RESUMEN:\n- {service.name} - {variant.name}\n"
              f"- PRECIO: $US {variant.price}\n"
              f"---------------------------\n"
              f"- ENTREGA: {'ID' if is_id else 'Correo'}: "
              f"{credentials.get('id') if is_id else credentials.get('email')}\n"
            )
            
            if variant.delivery_method == 'internal':
              summary += f"- Pass: {credentials.get('password')}"

            Item.objects.create(order=order, item_summary=summary)
            
      # Email.
      try:
        list_items = []
        
        emailContext = {
          "date": timezone.now().strftime("%d %b %Y"),
          "id": order.id,
          "total_items": len(items_data),
          "items": list_items,
          "payment_method": f"{request.data.get('payment_method')} ({request.data.get('currency')} - {rate})",
          "currency_label": currencyRate_obj.label,
          "total_amount": f"{total_amount * rate}"
        }
        html_content = render_to_string('email/orderInProcess.html', emailContext)

        send_email_async(
          request.data.get('email'),
          'Confirmación de orden',
          html_content
        )
      except Exception as e:
        print(e)
      
      return Response({'message': 'Orden creada exitosamente'}, status=status.HTTP_201_CREATED)

    except ValueError as e:
      return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
      return Response({'message': 'Error', 'error': str(e)}, status=500)