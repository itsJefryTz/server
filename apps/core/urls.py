from django.urls import path

from .views import CurrencyRateAPIView

core_urlpatterns = ([
  path('api/v1/CurrencyRateAPIView', CurrencyRateAPIView.as_view(), name='CurrencyRateAPIView'),
  ], 'core')