from django.contrib import admin

from .models import Category, Service, Variant

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
  list_display = ('id', 'name', 'date_updated', 'date_created')
  list_display_links = ('name',)
  readonly_fields = ('date_updated', 'date_created')
  ordering = ['id']
  
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
  list_display = ('id', 'active', 'get_category_name', 'name', 'date_updated', 'date_created')
  list_display_links = ('active', 'get_category_name', 'name')
  readonly_fields = ('date_updated', 'date_created')
  ordering = ['id']
  
  @admin.display(description='CATEGORÍA')
  def get_category_name(self, obj):
    return obj.category.name
  
@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
  list_display = ('id', 'available', 'get_service_name', 'name', 'price', 'delivery_type', 'delivery_method', 'date_updated', 'date_created')
  list_display_links = ('available', 'get_service_name', 'name', 'price', 'delivery_type', 'delivery_method')
  readonly_fields = ('date_updated', 'date_created')
  ordering = ['id']
  
  @admin.display(description='SERVICIO')
  def get_service_name(self, obj):
    return obj.service.name