from django.contrib import admin

from .models import Item, Order

# Register your models here.
class ItemAdmin(admin.ModelAdmin):
  list_display = ('id', 'service', 'variant', 'quantity', 'date_created')
  list_filter = ('service', 'date_created')
  search_fields = ('service__name', 'variant__name')
  readonly_fields = [f.name for f in Item._meta.get_fields()]
  
  def has_add_permission(self, request):
    return False

  def has_change_permission(self, request, obj=None):
    return False

  def has_delete_permission(self, request, obj=None):
    return False

class OrderItemInline(admin.TabularInline):
  model = Order.items.through
  extra = 0
  verbose_name = "Item de la Orden"
  verbose_name_plural = "Items de la Orden"
  
  def has_add_permission(self, request, obj=None):
    return False

  def has_change_permission(self, request, obj=None):
    return False

  def has_delete_permission(self, request, obj=None):
    return False

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
  change_form_template = 'admin/orders/order/change_form.html'
  
  ordering = ('-id',)
  list_display = ('id', 'type', 'status', 'phone', 'payment_method', 'reference', 'date_created')
  list_display_links = ('id', 'phone', 'payment_method', 'reference')
  list_filter = ('status', 'type', 'payment_method', 'date_created')
  search_fields = ('email', 'reference', 'phone', 'id')
  readonly_fields = ('type', 'payment_method', 'reference', 'phone', 'email', 'date_created', 'date_updated')
  
  fieldsets = (
    ('Orden', { 'fields': ('type', 'status') }),
    ('Detalles del Pago', { 'fields': ('payment_method', 'reference') }),
    ('Información de Contacto', { 'fields': ('phone', 'email') }),
    ('Fechas de Registro', {
      'fields': ('date_created', 'date_updated'),
      'classes': ('collapse',),
    }),
  )
  
  inlines = [OrderItemInline]
  exclude = ('items',)

  def get_form(self, request, obj=None, **kwargs):
    form = super().get_form(request, obj, **kwargs)
    return form
  
  def has_add_permission(self, request):
    return False