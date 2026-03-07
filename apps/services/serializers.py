from rest_framework import serializers

from .models import Category, Service, Variant

class CategorySerializer(serializers.ModelSerializer):
  date_updated = serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S")
  date_created = serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S")
  
  class Meta:
    model = Category
    fields = ['id', 'name', 'date_updated', 'date_created']
    
class VariantSerializer(serializers.ModelSerializer):
  date_updated = serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S")
  date_created = serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S")
  
  class Meta:
    model = Variant
    fields = ['id', 'available', 'name', 'price', 'delivery_type', 'date_updated', 'date_created']
    
class ServiceSerializer(serializers.ModelSerializer):
  category = CategorySerializer(read_only=True)
  variants = VariantSerializer(many=True, read_only=True)
  date_updated = serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S")
  date_created = serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S")
  
  class Meta:
    model = Service
    fields = ['id', 'active', 'category', 'image', 'name', 'description', 'variants', 'date_updated', 'date_created']