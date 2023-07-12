from django import forms
from django.forms import ModelForm, fields, Form
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Producto

form_select = {'class':'form-select'}
form_control = {'class':'form-control'}
form_text_area = {'class':'form-control', 'rows': '3'}
form_file = {'class': 'form-control-file', 'title': 'Debe subir una imagen'}

class ProductoForm(ModelForm):

    class Meta:
        model = Producto
        
        fields = [
            'categoria',
            'nombre',
            'descripcion',
            'precio',
            'descuento_subscriptor',
            'descuento_oferta',
            'imagen'
        ]

        widgets = {
            'categoria': forms.Select(attrs=form_select),
            'nombre': forms.TextInput(attrs=form_control),
            'descripcion': forms.Textarea(attrs=form_text_area),
            'precio': forms.NumberInput(attrs=form_control),
            'descuento_subscriptor': forms.NumberInput(attrs=form_control),
            'descuento_oferta': forms.NumberInput(attrs=form_control),
            'imagen': forms.FileInput(attrs=form_file),
        }


# class IniciarSesionForm(Form):
#     username = forms.CharField(widget=forms.TextInput(), label="Correo")
#     password = forms.CharField(widget=forms.PasswordInput(), label="Contraseña")
#     class Meta:
#         fields = ['username', 'password']

# class RegistrarUsuarioForm(UserCreationForm):
#     rut = forms.CharField(max_length=80, required=True, label="Rut")
#     direccion = forms.CharField(max_length=80, required=True, label="Dirección")
#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name', 'email', 'rut', 'direccion']

# class PerfilUsuarioForm(Form):
#     first_name = forms.CharField(max_length=150, required=True, label="Nombres")
#     last_name = forms.CharField(max_length=150, required=True, label="Apellidos")
#     email = forms.CharField(max_length=254, required=True, label="Correo")
#     rut = forms.CharField(max_length=80, required=False, label="Rut")
#     direccion = forms.CharField(max_length=80, required=False, label="Dirección")

#     class Meta:
#         fields = '__all__'