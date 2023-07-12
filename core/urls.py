from django.urls import path
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views
from .views import index, registrarme, nosotros, admin_productos
from .views import admin_usuarios, admin_bodega, ventas, ingresar
from .views import misdatos, miscompras, salir, carrito, ficha
from .views import cambiar_estado_boleta, poblar

urlpatterns = [
    path('', index, name='index'),
    path('registrarme', registrarme, name='registrarme'),
    path('nosotros', nosotros, name='nosotros'),
    path('admin_productos/<accion>/<id>', admin_productos, name='admin_productos'),
    path('admin_usuarios', admin_usuarios, name='admin_usuarios'),
    path('admin_bodega', admin_bodega, name='admin_bodega'),
    path('ventas', ventas, name='ventas'),
    path('cambiar_estado_boleta/<nro_boleta>/<estado>', cambiar_estado_boleta, name='cambiar_estado_boleta'),
    path('ingresar', ingresar, name='ingresar'),
    path('misdatos', misdatos, name='misdatos'),
    path('miscompras', miscompras, name='miscompras'),
    path('salir', salir, name='salir'),
    path('carrito', carrito, name='carrito'),
    path('ficha/<id>', ficha, name='ficha'),
    path('poblar', poblar, name='poblar'),

    # path('cerrarsesion', cerrarsesion, name='cerrarsesion'),
    # path('pswcambiada', TemplateView.as_view(template_name='core/pswcambiada.html'), name='pswcambiada'),
    # path('cambiarpsw', auth_views.PasswordChangeView.as_view(template_name='core/cambiarpsw.html', success_url='/cambiarpsw'), name='cambiarpsw'),
    # path('pagar/<id>', pagar, name="pagar"),
    # path('pagoexitoso/', pagoexitoso, name="pagoexitoso"),
]