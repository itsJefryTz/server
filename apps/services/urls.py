from django.urls import path

from .views import ServiceAPIView

services_urlpatterns = ([
  path('api/v1/ServiceAPIView', ServiceAPIView.as_view(), name='ServiceAPIView'),
  ], 'services')