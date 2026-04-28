from django.urls import path

from .views import OrderAPIView

orders_urlpatterns = ([
  path('api/v1/OrderAPIView', OrderAPIView.as_view(), name='OrderAPIView'),
  ], 'orders')