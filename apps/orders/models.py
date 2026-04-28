from django.db import models

from apps.services.models import Service, Variant

# Create your models here.
class Item(models.Model):
  service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name='Servicio')
  variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name='items', verbose_name='Variante')
  quantity = models.PositiveIntegerField(verbose_name='Cantidad')
  #
  date_created = models.DateTimeField(auto_now_add=True, verbose_name='Creada')
  date_updated = models.DateTimeField(auto_now=True, verbose_name='Actualizada')
  
  class Meta:
    verbose_name = 'Item'
    verbose_name_plural = 'Items'
  
  def __str__(self):
    return self.service.name + ' - ' + self.variant.name + ' x' + str(self.quantity) + ' - $US ' + str(self.variant.price)
  
class Order(models.Model):
  type = models.CharField(max_length=255, choices=[('cart', 'Carrito'), ('single', ' Único')], verbose_name='Tipo de orden')
  items = models.ManyToManyField(Item, related_name='orders', verbose_name='Items')
  status = models.CharField(max_length=255, choices=[('pending', 'Pendiente'), ('completed', 'Completada'), ('cancelled', 'Cancelada')], default='pending', verbose_name='Estado')
  payment_method = models.CharField(max_length=255, verbose_name='Método de pago')
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