# Generated manually

from django.db import migrations, models


def merge_old_columns_into_value(apps, schema_editor):
  PaymentMethodField = apps.get_model('payments', 'PaymentMethodField')
  for row in PaymentMethodField.objects.all():
    chunks = []
    ph = (getattr(row, 'placeholder', None) or '').strip()
    if ph:
      chunks.append(ph)
    desc = (getattr(row, 'description', None) or '').strip()
    if desc:
      chunks.append(desc)
    ftype = getattr(row, 'field_type', '') or ''
    raw_opts = getattr(row, 'select_options', None) or ''
    if ftype == 'select' and raw_opts.strip():
      chunks.append(raw_opts.strip())
    row.value = '\n\n'.join(chunks) if chunks else ''
    row.save(update_fields=['value'])


class Migration(migrations.Migration):

  dependencies = [
    ('payments', '0004_paymentmethodfield_remove_config_fields'),
  ]

  operations = [
    migrations.AddField(
      model_name='paymentmethodfield',
      name='value',
      field=models.TextField(blank=True, default='', verbose_name='Valor'),
      preserve_default=False,
    ),
    migrations.RunPython(merge_old_columns_into_value, migrations.RunPython.noop),
    migrations.RemoveConstraint(
      model_name='paymentmethodfield',
      name='payments_paymentmethodfield_unique_key_per_method',
    ),
    migrations.RemoveField(model_name='paymentmethodfield', name='sort_order'),
    migrations.RemoveField(model_name='paymentmethodfield', name='key'),
    migrations.RemoveField(model_name='paymentmethodfield', name='field_type'),
    migrations.RemoveField(model_name='paymentmethodfield', name='placeholder'),
    migrations.RemoveField(model_name='paymentmethodfield', name='required'),
    migrations.RemoveField(model_name='paymentmethodfield', name='validation_regex'),
    migrations.RemoveField(model_name='paymentmethodfield', name='description'),
    migrations.RemoveField(model_name='paymentmethodfield', name='select_options'),
  ]
