from rest_framework import serializers

from .models import Service, Variant
    
class VariantSerializer(serializers.ModelSerializer):
  date_updated = serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S")
  date_created = serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S")
  
  class Meta:
    model = Variant
    fields = ['id', 'available', 'name', 'price', 'date_updated', 'date_created']
    
class ServiceSerializer(serializers.ModelSerializer):
  variants = VariantSerializer(many=True, read_only=True)
  date_updated = serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S")
  date_created = serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S")
  
  class Meta:
    model = Service
    fields = ['id', 'active', 'image', 'name', 'description', 'variants', 'date_updated', 'date_created']