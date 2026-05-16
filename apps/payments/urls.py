from django.urls import path
from .views import CurrencyRateAPIView, PaymentMethodAPIView

payments_urlpatterns = ([
  path('api/v1/CurrencyRateAPIView', CurrencyRateAPIView.as_view(), name='CurrencyRateAPIView'),
  path('api/v1/PaymentMethodAPIView', PaymentMethodAPIView.as_view(), name='PaymentMethodAPIView'),
], 'payments')
