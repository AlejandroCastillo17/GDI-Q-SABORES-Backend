from django.db import models


class Gastos(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    constante = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'Gastos'


class Usuario(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)
    contrasena = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'Usuario'
        
    def __str__(self):
        return self.nombre, self.contrasena, self.id


class Ventas(models.Model):
    fecha = models.DateField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Ventas'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Compras(models.Model):
    fecha = models.DateField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'compras'


class Detallescompras(models.Model):
    idcompra = models.ForeignKey(Compras, models.DO_NOTHING, db_column='idCompra')  # Field name made lowercase.
    idproveedor = models.ForeignKey('Proveedores', models.DO_NOTHING, db_column='idProveedor')  # Field name made lowercase.
    idproducto = models.ForeignKey('Productos', models.DO_NOTHING, db_column='idProducto')  # Field name made lowercase.
    cantidad = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'detallesCompras'


class Detallesventas(models.Model):
    idventa = models.ForeignKey(Ventas, models.DO_NOTHING, db_column='idVenta')  # Field name made lowercase.
    idproducto = models.ForeignKey('Productos', models.DO_NOTHING, db_column='idProducto')  # Field name made lowercase.
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'detallesVentas'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Productos(models.Model):
    nombre = models.CharField(max_length=30)
    categoria = models.CharField(max_length=20)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_actual = models.IntegerField()
    cantidad_inicial = models.IntegerField()
    foto = models.TextField(blank=True, null=True)
    proveedorid = models.ForeignKey('Proveedores', models.DO_NOTHING, db_column='proveedorId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'productos'
        
    def __str__(self):
        return '{} {} {} {} {} {} {}'.format(self.nombre, self.categoria, self.precio, self.cantidad_actual, self.cantidad_inicial, self.foto, self.proveedorid)


class Proveedores(models.Model):
    nombre = models.CharField(max_length=20)
    telefono = models.CharField(max_length=11, blank=True, null=True)
    email = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'proveedores'
