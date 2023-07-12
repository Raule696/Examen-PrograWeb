from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, blank=False, null=False, verbose_name='Nombre categoría')
    
    class Meta:
        db_table = 'Categoria'
    
    def __str__(self):
        return f'{self.nombre}'

class Producto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING, verbose_name='Categoría')
    nombre = models.CharField(max_length=100, blank=False, null=False, verbose_name='Nombre producto')
    descripcion = models.CharField(max_length=400, blank=False, null=False, verbose_name='Descripción')
    precio = models.IntegerField(blank=False, null=False, verbose_name='Precio')
    descuento_subscriptor = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=False,
        null=False,
        verbose_name='% Descuento subscriptor'
    )
    descuento_oferta = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=False,
        null=False,
        verbose_name='% Descuento oferta'
    )
    imagen = models.ImageField(upload_to='productos/', blank=False, null=False, verbose_name='Imagen')
    
    class Meta:
        db_table = 'Producto'

    def __str__(self):
        return f'{self.id} - {self.categoria.nombre} - {self.nombre} - {self.precio}'

class Perfil(models.Model):
    USUARIO_CHOICES = [
        ('Cliente', 'Cliente'),
        ('Administrador', 'Administrador'),
        ('Superusuario', 'Superusuario'),
    ]
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_usuario = models.CharField(
        choices=USUARIO_CHOICES,
        max_length=50,
        blank=False,
        null=False,
        verbose_name='Tipo de usuario'
    )
    rut = models.CharField(max_length=15, blank=False, null=False, verbose_name='RUT')
    direccion = models.CharField(max_length=400, blank=False, null=False, verbose_name='Dirección')
    subscrito = models.BooleanField(blank=False, null=False, verbose_name='Subscrito')
    imagen = models.ImageField(upload_to='perfiles/', blank=False, null=False, verbose_name='Imagen')
    
    class Meta:
        db_table = 'Perfil'

    def __str__(self):
        return f'{self.usuario.first_name} - {self.usuario.last_name} - {self.tipo_usuario}'

class Carrito(models.Model):
    cliente = models.ForeignKey(Perfil, on_delete=models.DO_NOTHING)
    producto = models.ForeignKey(Producto, on_delete=models.DO_NOTHING)
    precio = models.IntegerField(blank=False, null=False, verbose_name='Precio')
    descuento_subscriptor = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=False,
        null=False,
        verbose_name='Descto subs'
    )
    descuento_oferta = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=False,
        null=False,
        verbose_name='Descto oferta'
    )
    descuento_total = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=False,
        null=False,
        verbose_name='Descto total'
    )
    descuentos = models.IntegerField(blank=False, null=False, verbose_name='Descuentos')
    precio_a_pagar = models.IntegerField(blank=False, null=False, verbose_name='Precio a pagar')
    
    class Meta:
        db_table = 'Carrito'

    def __str__(self):
        return f'{self.producto.categoria.nombre} - {self.producto.nombre} - {self.precio}'

class Boleta(models.Model):
    ESTADO_CHOICES = [
        ('Anulado', 'Anulado'),
        ('Vendido', 'Vendido'),
        ('Despachado', 'Despachado'),
        ('Entregado', 'Entregado'),
    ]
    nro_boleta = models.IntegerField(primary_key=True, blank=False, null=False, verbose_name='Nro boleta')
    cliente = models.ForeignKey(Perfil, on_delete=models.DO_NOTHING)
    monto_sin_iva = models.IntegerField(blank=False, null=False, verbose_name='Monto sin IVA')
    iva = models.IntegerField(blank=False, null=False, verbose_name='IVA')
    total_a_pagar = models.IntegerField(blank=False, null=False, verbose_name='Total a pagar')
    fecha_venta = models.DateField(blank=False, null=False, verbose_name='Fecha de venta')
    fecha_despacho = models.DateField(blank=True, null=True, verbose_name='Fecha de despacho')
    fecha_entrega = models.DateField(blank=True, null=True, verbose_name='Fecha de entrega')
    estado = models.CharField(choices=ESTADO_CHOICES, max_length=50, blank=False, null=False, verbose_name='Estado')
    
    class Meta:
        db_table = 'Boleta'

    def __str__(self):
        return f'{self.nro_boleta} {self.cliente.usuario.first_name} - {self.cliente.usuario.last_name} - {self.total_a_pagar}'

class DetalleBoleta(models.Model):
    boleta = models.ForeignKey(Boleta, on_delete=models.DO_NOTHING)
    producto = models.ForeignKey(Producto, on_delete=models.DO_NOTHING)
    precio = models.IntegerField(blank=False, null=False, verbose_name='Precio')
    descuento_subscriptor = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=False,
        null=False,
        verbose_name='Descto subs'
    )
    descuento_oferta = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=False,
        null=False,
        verbose_name='Descto oferta'
    )
    descuento_total = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=False,
        null=False,
        verbose_name='Descto total'
    )
    descuentos = models.IntegerField(blank=False, null=False, verbose_name='Descuentos')
    precio_a_pagar = models.IntegerField(blank=False, null=False, verbose_name='Precio a pagar')
    
    class Meta:
        db_table = 'DetalleBoleta'

    def __str__(self):
        return f'{self.boleta.nro_boleta} {self.producto.nombre} - {self.precio_a_pagar}'

class Bodega(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.DO_NOTHING, verbose_name='Producto')
    boleta = models.ForeignKey(Boleta, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Boleta')

    class Meta:
        db_table = 'Bodega'

    def __str__(self):
        if self.boleta is None:
            return f'{self.producto.nombre} - En bodega'
        else:
            return f'{self.producto.nombre} - Vendido (Boleta: {self.boleta.nro_boleta})'
