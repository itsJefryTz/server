from django.contrib import admin

from .models import CurrencyRate

@admin.register(CurrencyRate)
class CurrencyRateAdmin(admin.ModelAdmin):
  list_display = ('code', 'rate', 'date_updated')
  list_editable = ('rate',)
  readonly_fields = ('code', 'date_created', 'date_updated')
  
  def has_add_permission(self, request):
    return False
  
  def has_delete_permission(self, request, obj=None):
    return False

  def get_actions(self, request):
    actions = super().get_actions(request)
    if 'delete_selected' in actions:
      del actions['delete_selected']
    return actions