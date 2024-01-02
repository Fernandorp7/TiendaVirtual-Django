from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('tienda/', views.welcome, name='welcome'),
    path('tienda/admin/productos', views.productosAdmin, name='productos'),
    path('tienda/admin/editar/<int:pk>', views.editarProducto, name='editarProducto'),
    path('tienda/admin/eliminar-confirmar/<int:pk>', views.confirmarEliminarProducto, name='confirmarEliminarProducto'),
    path('tienda/admin/eliminar/<int:pk>', views.eliminarProducto, name='eliminarProducto'),
    path('tienda/admin/nuevo/', views.añadirProducto, name='añadirProducto'),
    path('tienda/iniciar/', views.iniciarSesion, name='iniciarSesion'),
    path('tienda/registrarse/', views.registrarse, name='registrarse'),
    path('tienda/cerrar/', views.cerrarSesion, name='cerrarSesion'),
    path('tienda/detalle-compra/<int:pk>', views.comprarProducto, name='comprarProducto'),
    path('tienda/info-checkout/<int:pk>', views.checkout, name='checkout'),
    path('tienda/informe/marca-productos/', views.informeMarca, name='informeMarca'),
    path('tienda/informe/top-ventasproductos', views.informeVentas, name='informeVentas'),
    path('tienda/informe/historial-compras', views.informeCompras, name='informeCompras'),
    path('tienda/informe/top-clientes', views.informeClientes, name='informeClientes'),
]
