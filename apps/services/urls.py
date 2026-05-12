from django.urls import path

from .views import PlayerLookupView, ServiceAPIView

services_urlpatterns = ([
  path('api/v1/lookup-player', PlayerLookupView.as_view(), name='lookup-player'),
  path('api/v1/ServiceAPIView', ServiceAPIView.as_view(), name='ServiceAPIView'),
], 'services')