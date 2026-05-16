# Generated manually for relational payment method fields

from django.db import migrations, models
import django.db.models.deletion


def copy_config_json_to_rows(apps, schema_editor):
  PaymentMethod = apps.get_model('payments', 'PaymentMethod')
  PaymentMethodField = apps.get_model('payments', 'PaymentMethodField')
  for pm in PaymentMethod.objects.all():
    cfg = pm.config_fields or {}
    rows = cfg.get('fields') or []
    for idx, row in enumerate(rows):
      key = (row.get('key') or '').strip() or f'field_{idx}'
      ftype = (row.get('type') or 'text').strip()
      if ftype not in ('text', 'email', 'select'):
        ftype = 'text'
      opts = row.get('options') or []
      if isinstance(opts, list):
        select_options = '\n'.join(str(o) for o in opts)
      else:
        select_options = ''
      PaymentMethodField.objects.create(
        payment_method=pm,
        sort_order=idx,
        label=row.get('label') or key,
        key=key,
        field_type=ftype,
        placeholder=(row.get('placeholder') or '')[:200],
        required=bool(row.get('required', True)),
        validation_regex=(row.get('validation') or '')[:500],
        description=row.get('description') or '',
        select_options=select_options,
      )


def restore_json_from_rows(apps, schema_editor):
  PaymentMethod = apps.get_model('payments', 'PaymentMethod')
  PaymentMethodField = apps.get_model('payments', 'PaymentMethodField')
  for pm in PaymentMethod.objects.all():
    out = []
    for f in PaymentMethodField.objects.filter(payment_method=pm).order_by('sort_order', 'id'):
      row = {
        'label': f.label,
        'key': f.key,
        'type': f.field_type,
        'placeholder': f.placeholder,
        'required': f.required,
      }
      if f.validation_regex:
        row['validation'] = f.validation_regex
      if f.description:
        row['description'] = f.description
      if f.field_type == 'select' and f.select_options.strip():
        row['options'] = [line.strip() for line in f.select_options.splitlines() if line.strip()]
      out.append(row)
    pm.config_fields = {'fields': out}
    pm.save(update_fields=['config_fields'])


class Migration(migrations.Migration):

  dependencies = [
    ('payments', '0003_remove_paymentmethod_description_and_more'),
  ]

  operations = [
    migrations.CreateModel(
      name='PaymentMethodField',
      fields=[
        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        ('sort_order', models.PositiveSmallIntegerField(default=0, verbose_name='Orden')),
        ('label', models.CharField(max_length=200, verbose_name='Etiqueta (visible al usuario)')),
        ('key', models.CharField(help_text='Identificador único dentro del método (ej. phone, id_card). Sin espacios.', max_length=100, verbose_name='Clave interna')),
        ('field_type', models.CharField(choices=[('text', 'Texto'), ('email', 'Correo electrónico'), ('select', 'Lista desplegable')], default='text', max_length=20, verbose_name='Tipo de campo')),
        ('placeholder', models.CharField(blank=True, max_length=200, verbose_name='Texto de ejemplo')),
        ('required', models.BooleanField(default=True, verbose_name='Obligatorio')),
        ('validation_regex', models.CharField(blank=True, help_text='Opcional. Solo para tipos texto y correo.', max_length=500, verbose_name='Validación (expresión regular)')),
        ('description', models.TextField(blank=True, verbose_name='Descripción / ayuda')),
        ('select_options', models.TextField(blank=True, help_text='Una opción por línea. Solo se usa cuando el tipo es «Lista desplegable».', verbose_name='Opciones del desplegable')),
        ('payment_method', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='defined_fields', to='payments.paymentmethod', verbose_name='Método de pago')),
      ],
      options={
        'verbose_name': 'Campo del método de pago',
        'verbose_name_plural': 'Campos del método de pago',
        'ordering': ['sort_order', 'id'],
      },
    ),
    migrations.AddConstraint(
      model_name='paymentmethodfield',
      constraint=models.UniqueConstraint(fields=('payment_method', 'key'), name='payments_paymentmethodfield_unique_key_per_method'),
    ),
    migrations.RunPython(copy_config_json_to_rows, restore_json_from_rows),
    migrations.RemoveField(
      model_name='paymentmethod',
      name='config_fields',
    ),
  ]
