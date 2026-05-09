from django.db import models

# Create your models here.  
class Order(models.Model):
  type = models.CharField(max_length=255, choices=[('cart', 'Carrito'), ('single', ' Único')], verbose_name='Tipo de orden')
  status = models.CharField(max_length=255, choices=[('pending', 'Pendiente'), ('completed', 'Completada'), ('cancelled', 'Cancelada')], default='pending', verbose_name='Estado')
  payment_method = models.CharField(max_length=255, verbose_name='Método de pago')
  total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Monto total')
  total_amount_converted = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Monto total convertido')
  reference = models.CharField(max_length=255, verbose_name='Referencia')
  phone = models.CharField(max_length=255, verbose_name='Teléfono')
  email = models.EmailField(verbose_name='Correo electrónico')
  #
  date_created = models.DateTimeField(auto_now_add=True, verbose_name='Creada')
  date_updated = models.DateTimeField(auto_now=True, verbose_name='Actualizada')
  
  class Meta:
    verbose_name = 'Orden'
    verbose_name_plural = 'Órdenes'
  
  def __str__(self):
    return str(self.id) + ' - ' + self.status + ' - ' + self.phone + ' - ' + self.reference
  
class Item(models.Model):
  order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Orden')
  item_summary = models.TextField(verbose_name='Resumen')
  status = models.CharField(max_length=255, choices=[('pending', 'Pendiente'), ('delivered', 'Entregado')], default='pending', verbose_name='Estado')
  #
  date_created = models.DateTimeField(auto_now_add=True, verbose_name='Creada')
  date_updated = models.DateTimeField(auto_now=True, verbose_name='Actualizada')
  
  class Meta:
    verbose_name = 'Item'
    verbose_name_plural = 'Items'
  
  def __str__(self):
    return self.item_summary