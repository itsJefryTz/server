from decimal import Decimal
from rest_framework import serializers

from .models import CurrencyRate, PaymentMethod, Payment, CURRENCY_LABEL_BY_CODE

class CurrencyRateSerializer(serializers.ModelSerializer):
  class Meta:
    model = CurrencyRate
    fields = ['code', 'label', 'rate']

class PaymentMethodSerializer(serializers.ModelSerializer):
  currency_label = serializers.SerializerMethodField()

  class Meta:
    model = PaymentMethod
    fields = ['name', 'currency', 'currency_label']

  def get_currency_label(self, obj):
    return CURRENCY_LABEL_BY_CODE.get(obj.currency, obj.currency)

  def to_representation(self, instance):
    data = super().to_representation(instance)
    data['fields'] = [f.as_field_dict() for f in instance.defined_fields.all()]
    return data
