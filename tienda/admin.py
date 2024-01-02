from django.contrib import admin
from .models import Marca, Cliente, Producto, Compra

admin.site.register(Marca)
admin.site.register(Cliente)
admin.site.register(Producto)
admin.site.register(Compra)
