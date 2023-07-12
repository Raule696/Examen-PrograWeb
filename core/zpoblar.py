import sqlite3
from django.contrib.auth.models import User, Permission
from django.db import connection
from datetime import date, timedelta
from random import randint
from core.models import Categoria, Producto, Carrito, Perfil, Boleta, DetalleBoleta, Bodega

def eliminar_tabla(nombre_tabla):
    #try:
    conexion = sqlite3.connect('db.sqlite3')
    cursor = conexion.cursor()
    cursor.execute(f"DELETE FROM {nombre_tabla}")
    conexion.commit()
    conexion.close()
    # except:
    #     pass

def exec_sql(query):
    with connection.cursor() as cursor:
        cursor.execute(query)

def crear_usuario(username, tipo, nombre, apellido, correo, es_superusuario, 
    es_staff, rut, direccion, subscrito, imagen):

    try:
        print(f'Verificar si existe usuario {username}.')

        if User.objects.filter(username=username).exists():
            print(f'   Eliminar {username}')
            User.objects.get(username=username).delete()
            print(f'   Eliminado {username}')
        
        print(f'Iniciando creación de usuario {username}.')

        usuario = None
        if tipo == 'Superusuario':
            print('    Crear Superuser')
            usuario = User.objects.create_superuser(username=username, password='123')
        else:
            print('    Crear User')
            usuario = User.objects.create_user(username=username, password='123')

        if tipo == 'Administrador':
            print('    Es administrador')
            usuario.is_staff = es_staff
            
        usuario.first_name = nombre
        usuario.last_name = apellido
        usuario.email = correo
        usuario.save()

        if tipo == 'Administrador':
            print(f'    Dar permisos a core y apirest')
            permisos = Permission.objects.filter(content_type__app_label__in=['core', 'apirest'])
            usuario.user_permissions.set(permisos)
            usuario.save()
 
        print(f'    Crear perfil: RUT {rut}, Subscrito {subscrito}, Imagen {imagen}')
        Perfil.objects.create(
            usuario=usuario, 
            tipo_usuario=tipo,
            rut=rut,
            direccion=direccion,
            subscrito=subscrito,
            imagen=imagen)
        print("    Creado correctamente")
    except Exception as err:
        print(f"    Error: {err}")

def eliminar_tablas():
    eliminar_tabla('auth_user_groups')
    eliminar_tabla('auth_user_user_permissions')
    eliminar_tabla('auth_group_permissions')
    eliminar_tabla('auth_group')
    eliminar_tabla('auth_permission')
    eliminar_tabla('django_admin_log')
    eliminar_tabla('django_content_type')
    eliminar_tabla('django_migrations')
    eliminar_tabla('django_session')
    eliminar_tabla('Bodega')
    eliminar_tabla('DetalleBoleta')
    eliminar_tabla('Boleta')
    eliminar_tabla('Perfil')
    eliminar_tabla('Carrito')
    eliminar_tabla('Producto')
    eliminar_tabla('Categoria')
    #eliminar_tabla('authtoken_token')
    eliminar_tabla('auth_user')

def poblar_bd():
    eliminar_tablas()

    crear_usuario(
        username='cevans',
        tipo='Cliente', 
        nombre='Chris', 
        apellido='Evans (Cliente Subscrito)', 
        correo='cevans@marvel.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='15499707-3', 
        direccion='123 Main Street, Los Angeles, \nCalifornia 90001 \nEstados Unidos', 
        subscrito=True, 
        imagen='perfiles/cevans.png')

    crear_usuario(
        username='eolsen',
        tipo='Cliente', 
        nombre='Elizabeth', 
        apellido='Olsen (Cliente Subscrito)', 
        correo='eolsen@marvel.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='19090011-2', 
        direccion='Albert Street, New York, \nNew York 10001 \nEstados Unidos', 
        subscrito=True, 
        imagen='perfiles/eolsen.png')

    crear_usuario(
        username='tholland',
        tipo='Cliente', 
        nombre='Tom', 
        apellido='Holland (Cliente no Subscrito)', 
        correo='tholland@marvel.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='23548549-0', 
        direccion='105 Apple Park Way, \nCupertino, CA 95014 \nEstados Unidos', 
        subscrito=False, 
        imagen='perfiles/tholland.png')

    crear_usuario(
        username='sjohansson',
        tipo='Cliente', 
        nombre='Scarlett', 
        apellido='Johansson (Cliente no Subscrito)', 
        correo='sjohansson@marvel.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='12788999-4', 
        direccion='350 5th Ave, \nNew York, NY 10118 \nEstados Unidos', 
        subscrito=False, 
        imagen='perfiles/sjohansson.png')

    crear_usuario(
        username='cpratt',
        tipo='Administrador', 
        nombre='Chris', 
        apellido='Pratt (Empleado)', 
        correo='cpratt@marvel.com', 
        es_superusuario=False, 
        es_staff=True, 
        rut='16543210-8', 
        direccion='10 Pine Road, Miami, \nFlorida 33101 \nEstados Unidos', 
        subscrito=False, 
        imagen='perfiles/cpratt.png')
    
    crear_usuario(
        username='mruffalo',
        tipo='Administrador', 
        nombre='Mark', 
        apellido='Ruffalo (Empleado)', 
        correo='mruffalo@marvel.com', 
        es_superusuario=False, 
        es_staff=True, 
        rut='21123344-7', 
        direccion='1600 Pennsylvania Avenue NW, \nWashington, D.C. \nEstados Unidos', 
        subscrito=False, 
        imagen='perfiles/mruffalo.png')

    crear_usuario(
        username='super',
        tipo='Superusuario',
        nombre='Robert',
        apellido='Downey Jr. (Empleado)',
        correo='rdowneyjr@marvel.com',
        es_superusuario=True,
        es_staff=True,
        rut='18472636-6',
        direccion='15 Oak Street, Los Angeles, \nCalifornia 90001 \nEstados Unidos',
        subscrito=False,
        imagen='perfiles/rdowneyjr.png')
    
    categorias_data = [
        { 'id': 1, 'nombre': 'Perros'},
        { 'id': 2, 'nombre': 'Gatos'},
        { 'id': 3, 'nombre': 'Pájaros'},
        { 'id': 4, 'nombre': 'Hamsters'},
    ]

    print('Crear categorías')
    for categoria in categorias_data:
        Categoria.objects.create(**categoria)
    print('Categorías creadas correctamente')

    productos_data = [
        # Categoría "Perros"
        {
            'id': 1,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Saco de alimento Royal Canin 3Kg sabor pavo',
            'descripcion': 'Saco de alimento Royal Canin 3Kg sabor pavo, con vitaminas, 25% de proteínas, para perros adultos',
            'precio': 12000,
            'descuento_subscriptor': 5,
            'descuento_oferta': 5,
            'imagen': 'productos/000001.jpg'
        },
        {
            'id': 2,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Collar para perros ajustable',
            'descripcion': 'Collar de nylon resistente para perros de diferentes tamaños, ajustable y cómodo.',
            'precio': 1500,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/000002.jpg'
        },
        {
            'id': 3,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Juguete mordedor para perros',
            'descripcion': 'Juguete resistente de caucho para perros, ideal para aliviar el estrés y promover la salud dental.',
            'precio': 800,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/000003.jpg'
        },
        {
            'id': 4,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Cama acolchada para perros',
            'descripcion': 'Cama suave y cómoda para perros de todas las razas y tamaños, lavable y duradera.',
            'precio': 3500,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/000004.jpg'
        },
        {
            'id': 5,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Correa retráctil para perros',
            'descripcion': 'Correa extensible y resistente para pasear a tu perro de forma segura y cómoda.',
            'precio': 2500,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/000005.jpg'
        },
        # Categoría "Gatos"
        {
            'id': 6,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'Rascador para gatos',
            'descripcion': 'Rascador de sisal con plataformas y juguetes para mantener entretenidos a tus gatos.',
            'precio': 3500,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/000006.jpg'
        },
        {
            'id': 7,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'Comedero automático para gatos',
            'descripcion': 'Comedero con temporizador para alimentar a tus gatos de forma automática y controlada.',
            'precio': 5000,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/000007.jpg'
        },
        {
            'id': 8,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'Juguete interactivo para gatos',
            'descripcion': 'Juguete con luces y movimientos aleatorios para estimular el juego y ejercicio de tus gatos.',
            'precio': 2000,
            'descuento_subscriptor': 5,
            'descuento_oferta': 5,
            'imagen': 'productos/000008.jpg'
        },
        {
            'id': 9,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'Arena para gatos',
            'descripcion': 'Arena absorbente y sin olor para mantener limpio el arenero de tus gatos.',
            'precio': 1500,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/000009.jpg'
        },
        {
            'id': 10,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'Transportadora para gatos',
            'descripcion': 'Transportadora segura y cómoda para llevar a tus gatos de manera segura.',
            'precio': 4000,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/000010.jpg'
        },
        # Categoría "Pájaros"
        {
            'id': 11,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Jaula para pájaros',
            'descripcion': 'Jaula amplia y segura para alojar a tus pájaros con comodidad.',
            'precio': 5000,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/000011.jpg'
        },
        {
            'id': 12,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Comedero automático para pájaros',
            'descripcion': 'Comedero con temporizador para alimentar a tus pájaros de forma automática y controlada.',
            'precio': 3000,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/000012.jpg'
        },
        {
            'id': 13,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Nido para pájaros',
            'descripcion': 'Nido cómodo y seguro para que tus pájaros puedan anidar y reproducirse.',
            'precio': 2000,
            'descuento_subscriptor': 5,
            'descuento_oferta': 5,
            'imagen': 'productos/000013.jpg'
        },
        {
            'id': 14,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Columpio para pájaros',
            'descripcion': 'Columpio de madera para que tus pájaros puedan jugar y ejercitarse.',
            'precio': 1500,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/000014.jpg'
        },
        {
            'id': 15,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Baño para pájaros',
            'descripcion': 'Baño especial para pájaros para que puedan asearse y refrescarse.',
            'precio': 2500,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/000015.jpg'
        },
        # Categoría "Hamsters"
    ]

    print('Crear productos')
    for producto in productos_data:
        Producto.objects.create(**producto)
    print('Productos creados correctamente')

    carrito_data = [
        {
            'id': 1,
            'cliente': Perfil.objects.get(rut='15499707-3'),
            'producto': Producto.objects.get(id=1), 
            'precio': 10000, 
            'descuento_subscriptor': 5,
            'descuento_oferta': 5,
            'descuento_total': 10,
            'descuentos': 1000,
            'precio_a_pagar': 9000,
        },
        {
            'id': 2,
            'cliente': Perfil.objects.get(rut='23548549-0'),
            'producto': Producto.objects.get(id=1), 
            'precio': 8000, 
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'descuento_total': 15,
            'descuentos': 3200,
            'precio_a_pagar': 6800,
        },
    ]

    print('Crear carritos')
    for carrito in carrito_data:
        Carrito.objects.create(**carrito)
    print('Carritos creados correctamente')

    print('Crear boletas')
    nro_boleta = 0
    perfiles_cliente = Perfil.objects.filter(tipo_usuario='Cliente')
    for cliente in perfiles_cliente:
        estado_index = -1
        for cant_boletas in range(1, randint(5, 21)):
            nro_boleta += 1
            estado_index += 1
            if estado_index > 3:
                estado_index = 0
            estado = Boleta.ESTADO_CHOICES[estado_index][1]
            fecha_venta = date(2023, randint(1, 5), randint(1, 28))
            fecha_despacho = fecha_venta + timedelta(days=randint(0, 3))
            fecha_entrega = fecha_despacho + timedelta(days=randint(0, 3))
            if estado == 'Anulado':
                fecha_despacho = None
                fecha_entrega = None
            elif estado == 'Vendido':
                fecha_despacho = None
                fecha_entrega = None
            elif estado == 'Despachado':
                fecha_entrega = None
            boleta = Boleta.objects.create(
                nro_boleta=nro_boleta, 
                cliente=cliente,
                monto_sin_iva=0,
                iva=0,
                total_a_pagar=0,
                fecha_venta=fecha_venta,
                fecha_despacho=fecha_despacho,
                fecha_entrega=fecha_entrega,
                estado=estado)
            detalle_boleta = []
            total_a_pagar = 0
            for cant_productos in range(1, randint(5, 11)):
                producto_id = randint(1, 10)
                producto = Producto.objects.get(id=producto_id)
                precio = producto.precio
                descuento_subscriptor = 0
                if cliente.subscrito:
                    descuento_subscriptor = producto.descuento_subscriptor
                descuento_oferta = producto.descuento_oferta
                descuento_total = descuento_subscriptor + descuento_oferta
                descuentos = int(round(precio * (100 - descuento_total) / 100))
                precio_a_pagar = precio - descuentos
                DetalleBoleta.objects.create(
                    boleta=boleta,
                    producto=producto,
                    precio=precio,
                    descuento_subscriptor=descuento_subscriptor,
                    descuento_oferta=descuento_oferta,
                    descuento_total=descuento_total,
                    descuentos=descuentos,
                    precio_a_pagar=precio_a_pagar)
                total_a_pagar += precio_a_pagar
            monto_sin_iva = int(round(total_a_pagar / 1.19))
            iva = total_a_pagar - monto_sin_iva
            boleta.monto_sin_iva = monto_sin_iva
            boleta.iva = iva
            boleta.total_a_pagar = total_a_pagar
            boleta.fecha_venta = fecha_venta
            boleta.fecha_despacho = fecha_despacho
            boleta.fecha_entrega = fecha_entrega
            boleta.estado = estado
            boleta.save()
            print(f'    Creada boleta Nro={nro_boleta} Cliente={cliente.usuario.first_name} {cliente.usuario.last_name}')
    print('Boletas creadas correctamente')
