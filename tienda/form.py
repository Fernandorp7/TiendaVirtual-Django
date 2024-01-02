from django import forms
from django.contrib.auth.models import User

from .models import Producto, Compra, Marca
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm



# Formulario para editar los productos en el modelo Producto
class editarAñadirProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['marca', 'nombre', 'modelo', 'unidades', 'precio', 'vip']


# Formulario para iniciar sesión
class iniciarSesionForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Usuario", }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Contraseña", }), label="Contraseña")
    next = forms.CharField(widget=forms.HiddenInput, initial="/")


# Formulario para registrarse
class registrarseForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# Formulario para filtrrar búsqueda
class filtroForm(forms.Form):
    nombre = forms.CharField(required=False, widget=forms.TextInput({"placeholder": "Buscar. . ."}))
    marca = forms.ModelMultipleChoiceField(queryset=Marca.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)


# Formulario para hacer la compra
class compraForm(forms.ModelForm):

    class Meta:
        model = Compra
        fields = ['unidades']
