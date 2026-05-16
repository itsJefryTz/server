from django.db import models

PAYMENT_CURRENCY_CHOICES = (
  ('VE', 'VES'),
  ('CO', 'COP'),
  ('US', 'USD'),
)

CURRENCY_LABEL_BY_CODE = dict(PAYMENT_CURRENCY_CHOICES)

class CurrencyRate(models.Model):
  code = models.CharField(unique=True, max_length=5, choices=[('VE', 'VE'), ('CO', 'CO'), ('US', 'US')], verbose_name='Código')
  label = models.CharField(unique=True, max_length=5, choices=[('VES', 'VES'), ('COP', 'COP'), ('USD', 'USD')], verbose_name='Etiqueta')
  rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Tasa')
  #
  date_created = models.DateTimeField(auto_now_add=True, verbose_name='Creada')
  date_updated = models.DateTimeField(auto_now=True, verbose_name='Actualizada')

  class Meta:
    verbose_name = 'Tasa de Moneda'
    verbose_name_plural = '1. Tasas de Monedas'

  def __str__(self):
    return f"{self.code} - {self.rate}"

class PaymentMethod(models.Model):
  name = models.CharField(max_length=100, unique=True, verbose_name='Nombre del método')
  currency = models.CharField(max_length=2, choices=PAYMENT_CURRENCY_CHOICES, default='US', verbose_name='Moneda')
  active = models.BooleanField(default=True, verbose_name='Activo')
  #
  date_created = models.DateTimeField(auto_now_add=True, verbose_name='Creado')
  date_updated = models.DateTimeField(auto_now=True, verbose_name='Actualizado')

  class Meta:
    verbose_name = 'Método de Pago'
    verbose_name_plural = '2. Métodos de Pago'

  def __str__(self):
    return f"{self.name} ({self.get_currency_display()})"

class PaymentMethodField(models.Model):
  payment_method = models.ForeignKey(
    PaymentMethod,
    on_delete=models.CASCADE,
    related_name='defined_fields',
    verbose_name='Método de pago',
  )
  label = models.CharField(max_length=200, verbose_name='Etiqueta')
  value = models.TextField(blank=True, verbose_name='Valor')
  description = models.TextField(verbose_name='Descripción breve')

  class Meta:
    verbose_name = 'Campo del método de pago'
    verbose_name_plural = 'Campos del método de pago'
    ordering = ['id']

  def __str__(self):
    return self.label

  def as_field_dict(self):
    return {'label': self.label, 'value': self.value, 'description': self.description}

class Payment(models.Model):
  STATUS_CHOICES = [
    ('pending', 'Pendiente'),
    ('completed', 'Completado'),
    ('cancelled', 'Cancelado'),
    ('refunded', 'Reembolsado'),
  ]
  payment_method = models.ForeignKey(
    PaymentMethod,
    on_delete=models.PROTECT,
    related_name='payments',
    verbose_name='Método de Pago',
  )
  reference = models.CharField(max_length=255, verbose_name='Referencia del pago')
  payment_receipt = models.ImageField(
    upload_to='payments/receipts/',
    blank=True,
    null=True,
    verbose_name='Comprobante de pago',
  )
  amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Monto')
  currency = models.CharField(max_length=2, choices=PAYMENT_CURRENCY_CHOICES, verbose_name='Moneda')
  exchange_rate = models.DecimalField(max_digits=10, decimal_places=2, default=1.00, verbose_name='Tasa de cambio')
  amount_converted = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Monto convertido a USD')
  status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Estado')
  date_payment = models.DateTimeField(blank=True, null=True, verbose_name='Fecha del pago')
  #
  date_created = models.DateTimeField(auto_now_add=True, verbose_name='Creado')
  date_updated = models.DateTimeField(auto_now=True, verbose_name='Actualizado')
  
  class Meta:
    verbose_name = 'Pago'
    verbose_name_plural = '3. Pagos Realizados'
    ordering = ['-date_created']

  def __str__(self):
    return f"{self.reference} - {self.amount} {self.currency} - {self.status}"

  def save(self, *args, **kwargs):
    if self.currency == 'US':
      self.amount_converted = self.amount
    elif self.currency == 'VE':
      self.amount_converted = self.amount / self.exchange_rate if self.exchange_rate else self.amount
    elif self.currency == 'CO':
      self.amount_converted = self.amount / self.exchange_rate if self.exchange_rate else self.amount
    super().save(*args, **kwargs)
