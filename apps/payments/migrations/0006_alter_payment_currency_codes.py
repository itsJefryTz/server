from django.db import migrations, models


def forwards_currency_codes(apps, schema_editor):
  label_to_code = {'VES': 'VE', 'COP': 'CO', 'USD': 'US'}
  for model_name in ('PaymentMethod', 'Payment'):
    Model = apps.get_model('payments', model_name)
    for obj in Model.objects.all():
      cur = obj.currency
      if cur in label_to_code:
        obj.currency = label_to_code[cur]
        obj.save(update_fields=['currency'])


def backwards_currency_labels(apps, schema_editor):
  code_to_label = {'VE': 'VES', 'CO': 'COP', 'US': 'USD'}
  for model_name in ('PaymentMethod', 'Payment'):
    Model = apps.get_model('payments', model_name)
    for obj in Model.objects.all():
      cur = obj.currency
      if cur in code_to_label:
        obj.currency = code_to_label[cur]
        obj.save(update_fields=['currency'])


class Migration(migrations.Migration):

  dependencies = [
    ('payments', '0005_simplify_paymentmethodfield_label_value'),
  ]

  operations = [
    migrations.RunPython(forwards_currency_codes, backwards_currency_labels),
    migrations.AlterField(
      model_name='paymentmethod',
      name='currency',
      field=models.CharField(
        choices=[('VE', 'VES'), ('CO', 'COP'), ('US', 'USD')],
        default='US',
        max_length=2,
        verbose_name='Moneda',
      ),
    ),
    migrations.AlterField(
      model_name='payment',
      name='currency',
      field=models.CharField(
        choices=[('VE', 'VES'), ('CO', 'COP'), ('US', 'USD')],
        max_length=2,
        verbose_name='Moneda',
      ),
    ),
  ]
