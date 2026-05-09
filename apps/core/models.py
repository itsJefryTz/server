from django.db import models

# Create your models here.
class CurrencyRate(models.Model):
  code = models.CharField(unique=True, max_length=5, choices=[('VE', 'VE'), ('CO', 'CO'), ('US', 'US')], verbose_name='Código')
  rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Tasa')
  #
  date_created = models.DateTimeField(auto_now_add=True, verbose_name='Creada')
  date_updated = models.DateTimeField(auto_now=True, verbose_name='Actualizada')
  
  class Meta:
    verbose_name = 'Tasa de Moneda'
    verbose_name_plural = 'Tasas de Monedas'
    
  def __str__(self):
    return f"{self.code} - {self.rate}"