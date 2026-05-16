import json
from decimal import Decimal
from django.db import transaction
from django.template.loader import render_to_string
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Order, Item
from apps.services.models import Service, Variant
from apps.payments.models import CurrencyRate, PaymentMethod, Payment
from apps.core.utils import send_email_async

ALLOWED_RECEIPT_CONTENT_TYPES = {
  'image/jpeg',
  'image/png',
  'image/gif',
  'image/webp',
}
MAX_RECEIPT_SIZE_BYTES = 5 * 1024 * 1024

def _parse_order_items(raw_items):
  if isinstance(raw_items, str):
    try:
      raw_items = json.loads(raw_items)
    except json.JSONDecodeError:
      return []
  if not isinstance(raw_items, list):
    return []
  return [item for item in raw_items if isinstance(item, dict)]

class OrderAPIView(APIView):
  def post(self, request):
    raw_items = request.data.get('items', [])
    items_data = _parse_order_items(raw_items)

    if not items_data:
      return Response({'message': 'The items list is empty or invalid'}, status=status.HTTP_400_BAD_REQUEST)

    receipt = request.FILES.get('payment_receipt')
    if not receipt:
      return Response(
        {'message': 'El comprobante de pago es obligatorio.'},
        status=status.HTTP_400_BAD_REQUEST,
      )

    if receipt.content_type not in ALLOWED_RECEIPT_CONTENT_TYPES:
      return Response(
        {'message': 'El comprobante debe ser una imagen (JPG, PNG, WEBP o GIF).'},
        status=status.HTTP_400_BAD_REQUEST,
      )

    if receipt.size > MAX_RECEIPT_SIZE_BYTES:
      return Response(
        {'message': 'El comprobante no debe superar 5 MB.'},
        status=status.HTTP_400_BAD_REQUEST,
      )

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

        payment_method_name = request.data.get('payment_method')
        try:
          payment_method_obj = PaymentMethod.objects.get(
            name=payment_method_name,
            active=True,
          )
        except PaymentMethod.DoesNotExist:
          raise ValueError(f'Método de pago no válido: {payment_method_name}')

        amount_converted = total_amount * rate
        
        payment = Payment.objects.create(
          payment_method=payment_method_obj,
          reference=request.data.get('reference'),
          amount=amount_converted,
          currency=currency_code,
          exchange_rate=rate,
          payment_receipt=receipt,
          status='pending',
        )

        order = Order.objects.create(
          type=request.data.get('order_type'),
          payment=payment,
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
              f"- ENTREGA VÍA {'ID' if is_id else 'Interno'}:\n"
            )
            
            if (variant.delivery_method == 'id'):
              summary += f"- ID: {credentials.get('id')}\n"
              summary += f"- Nombre del Jugador: {credentials.get('player_name') if credentials.get('player_name') else ''}\n"
            elif variant.delivery_method == 'internal':
              summary += f"- Email: {credentials.get('email')}"
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