from django.contrib import admin

from .models import Category, Service, Variant

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
  list_display = ('id', 'name', 'date_updated', 'date_created')
  list_display_links = ('name',)
  search_fields = ('name',)
  readonly_fields = ('date_updated', 'date_created')
  ordering = ['id']

class VariantInline(admin.TabularInline):
  model = Variant
  extra = 1
  fields = ('available', 'name', 'price', 'delivery_type', 'delivery_method')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
  list_display = ('id', 'active', 'get_category_name', 'name', 'date_updated')
  list_display_links = ('name',)
  list_filter = ('active', 'category')
  search_fields = ('name', 'category__name')
  readonly_fields = ('date_updated', 'date_created')
  ordering = ['id']
  
  list_select_related = ('category',)
  
  inlines = [VariantInline]

  @admin.display(description='CATEGORÍA', ordering='category__name')
  def get_category_name(self, obj):
    return obj.category.name

@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
  list_display = ('id', 'available', 'get_service_name', 'name', 'price', 'delivery_type')
  list_display_links = ('name',)
  list_filter = ('available', 'delivery_type', 'service__category')
  search_fields = ('name', 'service__name')
  readonly_fields = ('date_updated', 'date_created')
  ordering = ['id']
  
  list_select_related = ('service',)

  @admin.display(description='SERVICIO', ordering='service__name')
  def get_service_name(self, obj):
    return obj.service.name