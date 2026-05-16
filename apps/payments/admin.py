from django.contrib import admin

from .models import CurrencyRate, PaymentMethod, PaymentMethodField, Payment

@admin.register(CurrencyRate)
class CurrencyRateAdmin(admin.ModelAdmin):
  list_display = ('code', 'label', 'rate', 'date_updated')
  list_filter = ('code',)
  search_fields = ('code', 'label')
  readonly_fields = ('date_created', 'date_updated')
  fieldsets = (
    ('Información de la Moneda', {'fields': ('code', 'label', 'rate')}),
    ('Fechas', {'fields': ('date_created', 'date_updated'), 'classes': ('collapse',)}),
  )

class PaymentMethodFieldInline(admin.TabularInline):
  model = PaymentMethodField
  extra = 1
  fields = ('label', 'value', 'description')

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
  list_display = ('name', 'currency', 'active', 'field_count', 'date_created')
  list_filter = ('active', 'currency')
  search_fields = ('name',)
  readonly_fields = ('date_created', 'date_updated')
  inlines = (PaymentMethodFieldInline,)
  fieldsets = (
    ('Información del Método', {'fields': ('name', 'currency', 'active')}),
    ('Fechas', {'fields': ('date_created', 'date_updated'), 'classes': ('collapse',)}),
  )

  @admin.display(description='Nº campos')
  def field_count(self, obj):
    if obj.pk:
      return obj.defined_fields.count()
    return '—'

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
  list_display = ('id', 'reference', 'amount', 'currency', 'amount_converted', 'status', 'date_created')
  list_display_links = ('id', 'reference')
  list_filter = ('status', 'currency', 'payment_method', 'date_created')
  search_fields = ('reference', 'order_id')
  readonly_fields = ('payment_method', 'reference', 'amount', 'currency', 'exchange_rate', 'amount_converted', 'payment_receipt', 'date_created', 'date_updated')
  fieldsets = (
    ('Información del Pago', {
      'fields': (
        'payment_method', 'reference', 'payment_receipt',
        'amount', 'currency', 'exchange_rate', 'amount_converted',
      ),
    }),
    ('Estado', {'fields': ('status',)}),
    ('Fechas', {'fields': ('date_payment', 'date_created', 'date_updated'), 'classes': ('collapse',)}),
  )

  def has_add_permission(self, request):
    return False
