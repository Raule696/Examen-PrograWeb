from datetime import date
from django.shortcuts import render, redirect
from .models import Producto, Boleta
from .forms import ProductoForm
from .zpoblar import poblar_bd

def index(request):
    productos = Producto.objects.all().order_by('nombre')
    if request.method == 'POST':
        buscar = request.POST.get('buscar')
        if buscar.strip() != '':
            productos = Producto.objects.filter(nombre__icontains=buscar).order_by('nombre')
    datos = { 
        'productos': productos
    }
    return render(request, 'core/index.html', datos)

def poblar(request):
    poblar_bd()
    return redirect(index)

def registrarme(request):
    return render(request, 'core/registrarme.html')

def nosotros(request):
    return render(request, 'core/nosotros.html')

def admin_productos(request):

    return render(request, 'core/productos.html')

def admin_usuarios(request):
    return render(request, 'core/admin_usuarios.html')

def admin_bodega(request):
    return render(request, 'core/admin_bodega.html')

def ventas(request):
    boletas = Boleta.objects.all()
    historial =[]
    for boleta in boletas:
        boleta_historial = {}
        boleta_historial['nro_boleta'] = boleta.nro_boleta
        boleta_historial['nom_cliente'] = f'{boleta.cliente.usuario.first_name} {boleta.cliente.usuario.last_name}'
        boleta_historial['fecha_venta'] = boleta.fecha_venta
        boleta_historial['fecha_despacho'] = boleta.fecha_despacho
        boleta_historial['fecha_entrega'] = boleta.fecha_entrega
        if boleta.cliente.subscrito:
            boleta_historial['subscrito'] = 'Sí'
        else:
            boleta_historial['subscrito'] = 'No'
        boleta_historial['total_a_pagar'] = boleta.total_a_pagar
        boleta_historial['estado'] = boleta.estado
        historial.append(boleta_historial)
    datos = { 'historial': historial }
    return render(request, 'core/ventas.html', datos)

def cambiar_estado_boleta(request, nro_boleta, estado):
    boleta = Boleta.objects.get(nro_boleta=nro_boleta)
    boleta.estado = estado
    if estado == 'Anulado':
        boleta.fecha_venta = date.today()
        boleta.fecha_despacho = None
        boleta.fecha_entrega = None
    else:
        if estado == 'Vendido':
            boleta.fecha_venta = date.today()
            boleta.fecha_despacho = None
            boleta.fecha_entrega = None
        elif estado == 'Despachado':
            boleta.fecha_despacho = date.today()
            boleta.fecha_entrega = None
        elif estado == 'Entregado':
            if boleta.estado == 'Vendido':
                boleta.fecha_despacho = date.today()
                boleta.fecha_entrega = date.today()
            elif boleta.estado == 'Desapachado':
                boleta.fecha_entrega = date.today()
            elif boleta.estado == 'Entregado':
                boleta.fecha_entrega = date.today()
    boleta.save()
    return redirect(ventas)

def ingresar(request):
    return render(request, 'core/ingresar.html')

def misdatos(request):
    return render(request, 'core/misdatos.html')

def miscompras(request):
    return render(request, 'core/miscompras.html')

def salir(request):
    return redirect(index)

def carrito(request):
    return render(request, 'core/carrito.html')

def ficha(request, id):
    data = {'producto':  Producto.objects.get(id=id) }
    return render(request, 'core/ficha.html', data)

def admin_productos(request, accion, id):
    data = {
        'mensaje': '', 
        'formulario': ProductoForm, 
        'accion': accion, 
        'id': id, 
    }

    if accion == 'ins':
        if request.method == 'POST':
            formulario = ProductoForm(request.POST, request.FILES)
            if formulario.is_valid():
                try:
                    formulario.save()
                    data['mensaje'] = '¡El producto fue creado correctamente!'
                except:
                    data['mensaje'] = '¡No se puede crear dos productos con el mismo ID!'

    elif accion == 'upd':
        producto = Producto.objects.get(id=id)
        if request.method == 'POST':
            formulario = ProductoForm(data=request.POST, files=request.FILES, instance=producto)
            if formulario.is_valid():
                formulario.save()
                data['mensaje'] = '¡El producto fue actualizado correctamente!'
        data['formulario'] = ProductoForm(instance=producto)

    elif accion == 'del':
        try:
            Producto.objects.get(id=id).delete()
            data['mensaje'] = '¡El producto fue eliminado correctamente!'
            return redirect(admin_productos, accion='ins', id = '-1')
        except:
            data['mensaje'] = '¡El producto ya estaba eliminado!'

    data['productos'] = Producto.objects.all().order_by('id')
    return render(request, 'core/admin_productos.html', data)

# def guardar_formulario(request, Formulario, instancia, entidad):
#     if request.method == 'POST':
#         formulario = Formulario(request.POST, request.FILES)
#         if formulario.is_valid:
#             try:
#                 formulario.save()
#                 return f'¡El {entidad} fue creado correctamente!'
#             except:

