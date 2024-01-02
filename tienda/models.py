from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


# Create your models here.



class Marca(models.Model):
    #marca_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Marcas"


class Cliente(models.Model):
    #cliente_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vip = models.BooleanField(default=False)
    saldo = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f'{self.user.username}'

    class Meta:
        verbose_name_plural = "Clientes"


class Producto(models.Model):
    #producto_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    unidades = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(limit_value=0)])
    vip = models.BooleanField(default=False)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    #imagen = models.ImageField(upload_to='img/')

    def __str__(self):
        return f'{self.marca} {self.modelo}'

    class Meta:
        verbose_name_plural = "Productos"
        unique_together = ['marca', 'modelo']


class Compra(models.Model):
    #referencia = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(default=timezone.now)
    unidades = models.IntegerField()
    importe = models.DecimalField(max_digits=12, decimal_places=2)
    iva = models.DecimalField(max_digits=12, decimal_places=2, default=0.21)
    user = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.user.username}{self.fecha}'

    class Meta:
        verbose_name_plural = "Compras"
        unique_together=['fecha', 'producto', 'user']
