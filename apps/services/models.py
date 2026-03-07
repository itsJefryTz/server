from django.db import models

# Create your models here.
class Category(models.Model):
  name = models.CharField(max_length=255, verbose_name='Nombre')
  #
  date_created = models.DateTimeField(auto_now_add=True, verbose_name='Creada')
  date_updated = models.DateTimeField(auto_now=True, verbose_name='Actualizada')
  
  class Meta:
    verbose_name = 'Categoría'
    verbose_name_plural = 'Categorías'
  
  def __str__(self):
    return self.name

class Service(models.Model):
  active = models.BooleanField(default=True, verbose_name='¿Activo?')
  category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='services', verbose_name='Categoría')
  image = models.ImageField(upload_to='services/', verbose_name='Imagen')
  name = models.CharField(max_length=255, verbose_name='Nombre')
  description = models.TextField(verbose_name='Descripción')
  #
  date_created = models.DateTimeField(auto_now_add=True, verbose_name='Creada')
  date_updated = models.DateTimeField(auto_now=True, verbose_name='Actualizada')
  
  class Meta:
    verbose_name = 'Servicio'
    verbose_name_plural = 'Servicios'
  
  def __str__(self):
    return self.name
  
class Variant(models.Model):
  available = models.BooleanField(verbose_name='¿Disponible?')
  service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='variants', verbose_name='Servicio')
  name = models.CharField(max_length=255, verbose_name='Nombre')
  price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio')
  delivery_type_choices = [('manual', 'Manual'),]
  delivery_type = models.CharField(max_length=255, choices=delivery_type_choices, verbose_name='Tipo de entrega')
  #
  date_created = models.DateTimeField(auto_now_add=True, verbose_name='Creada')
  date_updated = models.DateTimeField(auto_now=True, verbose_name='Actualizada')
  
  class Meta:
    verbose_name = 'Variante'
    verbose_name_plural = 'Variantes'
  
  def __str__(self):
    return self.name