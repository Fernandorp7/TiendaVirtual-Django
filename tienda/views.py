from django.db.models import Count, Sum
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto, Cliente, Compra, Marca
from django.contrib.admin.views.decorators import staff_member_required
from .form import editarAñadirProductoForm, iniciarSesionForm, filtroForm, compraForm, registrarseForm
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.utils import timezone



# Página de inicio
def welcome(request):
    productos = Producto.objects.all()
    filtro_busqueda = filtroForm()

    if request.method == "POST":
        filtro_busqueda = filtroForm(request.POST)
        if filtro_busqueda.is_valid():
            nombre = filtro_busqueda.cleaned_data['nombre']
            marca = filtro_busqueda.cleaned_data['marca']

            productos = productos.filter(nombre__contains=nombre)
            if marca:
                productos = productos.filter(marca__id__in=marca)

    return render(request, 'tienda/index.html', {'Productos': productos, 'filtro_busqueda': filtro_busqueda})


# Iniciar sesión
def iniciarSesion(request):
    if request.method == "POST":
        form = iniciarSesionForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            next_ruta = request.GET.get('next', '/tienda')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect(next_ruta)
            else:
                messages.error(request, 'Las credenciales no son válidas')

    else:
        form = iniciarSesionForm()

    template = 'tienda/iniciarSesion.html'
    return_render = render(request, template, {'form': form})
    return return_render


def registrarse(request):
    if request.method == 'POST':
        form = registrarseForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            cliente = Cliente(user=user, saldo=0, vip=False)
            cliente.save()
            login(request, user)
            return redirect('welcome')
    else:
        form = registrarseForm()

    return render(request, 'tienda/iniciarSesion.html', {'form': form})


# Cerrar sesión
def cerrarSesion(request):
    logout(request)
    return redirect('welcome')


# Lista de productos (requiere autenticación y ser staff)
@staff_member_required
@login_required(login_url='/tienda/iniciar/')
def productosAdmin(request):
    Productos = Producto.objects.all()
    return render(request, 'tienda/producto.html', {'Productos': Productos})


# Editar producto (requiere autenticación y ser staff)
@staff_member_required
@login_required(login_url='/tienda/iniciar/')
def editarProducto(request, pk):
    producto = get_object_or_404(Producto,pk=pk)
    if request.method == "POST":
        form = editarAñadirProductoForm(request.POST,instance=producto)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.save()
            return redirect('productos')
    else:
        form = editarAñadirProductoForm(instance=producto)
    return render(request, 'tienda/editar.html', {'form': form})


# Añadir producto (requiere autenticación y ser staff)
@staff_member_required
@login_required(login_url='/tienda/iniciar/')
def añadirProducto(request):
    if request.method == "POST":
        form = editarAñadirProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('productos')
    else:
        form = editarAñadirProductoForm()
    return render(request, 'tienda/nuevo.html', {'form': form})


# Redirige a la página de confirmación de eliminar producto
@staff_member_required
@login_required(login_url='/tienda/iniciar/')
def confirmarEliminarProducto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'tienda/confirmarEliminacionProducto.html', {'producto': producto})


# Eliminar producto (requiere autenticación y ser staff)
@staff_member_required
@login_required(login_url='/tienda/iniciar/')
def eliminarProducto(request, pk):
    if request.method == 'POST':
        producto = Producto.objects.filter(pk=pk).delete()
        return redirect('productos')
    else:
        return HttpResponseForbidden("Acceso no permitido")


# Comprar producto
@transaction.atomic
@login_required(login_url='/tienda/iniciar/')
def comprarProducto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == "POST":
        form = compraForm(request.POST)
        if form.is_valid():
            unidades = form.cleaned_data['unidades']

            if unidades <= producto.unidades:
                cliente = Cliente.objects.get(user=request.user)

                if cliente.saldo >= unidades * producto.precio:
                    producto.unidades -= unidades
                    producto.save()

                    compra = Compra()
                    compra.producto = producto
                    compra.user = cliente
                    compra.unidades = unidades
                    compra.importe = unidades * producto.precio
                    compra.fecha = timezone.now()
                    compra.save()

                    cliente.saldo -= compra.importe
                    cliente.save()

                    return redirect('checkout', pk=compra.pk)
                else:
                    messages.error(request, "No tiene suficiente saldo para realizar la compra.")
            else:
                messages.error(request, "No hay suficientes unidades disponibles para la compra.")
    else:
        form = compraForm()

    return render(request, 'tienda/compraProducto.html', {'form': form, 'producto': producto})


# Página de checkout
#@staff_member_required
@login_required(login_url='/tienda/iniciar/')
def checkout(request, pk):
    compra = Compra.objects.get(pk=pk)
    producto = compra.producto
    importe = compra.unidades * producto.precio
    return render(request, 'tienda/checkout.html', {'producto': producto, 'compra': compra, 'importe': importe})


# Informe de productos por marca
@staff_member_required
@login_required(login_url='/tienda/iniciar/')
def informeMarca(request):
    marcas = Marca.objects.all()
    producto = Producto.objects.all()
    return render(request, 'tienda/productoMarca.html', {'marcas': marcas, 'productos': producto})


# Informe de productos más vendidos
@staff_member_required
@login_required(login_url='/tienda/iniciar/')
def informeVentas(request):
    productos = Producto.objects.annotate(recuento=Count('compra')).order_by('-recuento')[:10]
    return render(request, 'tienda/topVendidos.html', {'productos': productos})


# Informe historial de compras por usuario
@login_required(login_url='/tienda/iniciar/')
def informeCompras(request):
    cliente = get_object_or_404(Cliente, user=request.user)
    compras = Compra.objects.all().filter(producto__compra__user_id=cliente)
    return render(request, 'tienda/detalleCompra.html', {'compras': compras})


# Informe mejores clientes
@staff_member_required
@login_required(login_url='/tienda/iniciar/')
def informeClientes(request):
    clientes = Cliente.objects.annotate(dinero=Sum('compra__importe')).order_by('-dinero')[:10]
    return render(request, 'tienda/topClientes.html', {'clientes': clientes})
