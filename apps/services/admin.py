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
  list_display = ('id', 'active', 'name', 'date_updated', 'date_created')
  list_display_links = ('active', 'name')
  readonly_fields = ('date_updated', 'date_created')
  ordering = ['id']
  
@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
  list_display = ('id', 'available', 'get_service_name', 'name', 'price', 'date_updated', 'date_created')
  list_display_links = ('available', 'get_service_name', 'name', 'price')
  readonly_fields = ('date_updated', 'date_created')
  ordering = ['id']
  
  @admin.display(description='SERVICIO')
  def get_service_name(self, obj):
    return obj.service.name