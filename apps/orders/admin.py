from django.contrib import admin

from .models import Item, Order

class ItemInline(admin.StackedInline):
  model = Item
  extra = 0
  verbose_name = "Item de la Orden"
  verbose_name_plural = "Items de la Orden"
  readonly_fields = ('item_summary',)
  fields = ('item_summary', 'status')

  def has_add_permission(self, request, obj=None):
    return False

  def has_change_permission(self, request, obj=None):
    return True

  def has_delete_permission(self, request, obj=None):
    return False
  
  def get_actions(self, request):
    actions = super().get_actions(request)
    if 'delete_selected' in actions:
      del actions['delete_selected']
    return actions

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
  change_form_template = 'admin/orders/order/change_form.html'
  
  ordering = ('-id',)
  list_display = ('id', 'type', 'status', 'payment', 'date_created')
  list_display_links = ('id', 'payment')
  list_filter = ('status', 'type', 'date_created')
  search_fields = ('email', 'phone', 'id')
  readonly_fields = ('type', 'payment', 'phone', 'email', 'date_created', 'date_updated')
  
  fieldsets = (
    ('Orden', { 'fields': ('type', 'status') }),
    ('Detalles del Pago', { 'fields': ('payment',) }),
    ('Información de Contacto', { 'fields': ('phone', 'email') }),
    ('Fechas de Registro', {
      'fields': ('date_created', 'date_updated'),
      'classes': ('collapse',),
    }),
  )
  
  inlines = [ItemInline]

  def get_form(self, request, obj=None, **kwargs):
    form = super().get_form(request, obj, **kwargs)
    return form
  
  def has_add_permission(self, request):
    return False