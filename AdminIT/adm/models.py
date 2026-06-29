from django.db import models
from django.contrib.auth.models import User, Group

class Modulo(models.Model):
    url = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    icono = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200)
    activo = models.BooleanField(blank=True, null=True)
    orden = models.IntegerField(default=0)
    app = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre+" (/"+self.url+")"

    class Meta:
        verbose_name = "Modulo"
        verbose_name_plural = "Modulos"

class Rol(models.Model):
    nombre      = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200, blank=True)
    orden       = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['orden', 'nombre']
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'


class RolUsuario(models.Model):
    usuario_id = models.IntegerField()
    rol        = models.ForeignKey(Rol, on_delete=models.CASCADE, related_name='rolusuario_set')

    def __str__(self):
        return f'Usuario {self.usuario_id} → {self.rol}'

    class Meta:
        unique_together = ['usuario_id', 'rol']
        verbose_name = 'Asignación de Rol'
        verbose_name_plural = 'Asignaciones de Rol'


class RolModuloPermiso(models.Model):
    rol            = models.ForeignKey(Rol, on_delete=models.CASCADE, related_name='permisos')
    modulo         = models.ForeignKey(Modulo, on_delete=models.CASCADE)
    puede_ver      = models.BooleanField(default=True)
    puede_crear    = models.BooleanField(default=False)
    puede_editar   = models.BooleanField(default=False)
    puede_eliminar = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.rol} · {self.modulo}'

    class Meta:
        unique_together = ['rol', 'modulo']
        verbose_name = 'Permiso de Módulo'
        verbose_name_plural = 'Permisos de Módulos'


class UsuarioTIC(models.Model):
    usuario_id     = models.IntegerField(primary_key=True)
    username       = models.CharField(max_length=150)
    password       = models.CharField(max_length=128)
    email          = models.EmailField(max_length=254)
    is_active      = models.BooleanField()
    is_staff       = models.BooleanField()
    date_joined    = models.DateTimeField()
    persona_id     = models.IntegerField(null=True, blank=True)
    nombres        = models.CharField(max_length=200, null=True, blank=True)
    apellido1      = models.CharField(max_length=100, null=True, blank=True)
    apellido2      = models.CharField(max_length=100, null=True, blank=True)
    nombre_completo = models.CharField(max_length=500, null=True, blank=True)
    cedula         = models.CharField(max_length=20, null=True, blank=True)
    telefono       = models.CharField(max_length=50, null=True, blank=True)
    emailinst      = models.EmailField(max_length=254, null=True, blank=True)
    grupo          = models.CharField(max_length=150)

    class Meta:
        managed  = False
        db_table = 'view_usuarios_tic'
        verbose_name = 'Usuario TIC'
        verbose_name_plural = 'Usuarios TIC'

    def __str__(self):
        return f'{self.nombre_completo or self.username} ({self.grupo})'

class Institucion(models.Model):
    nombre = models.CharField(max_length=150, unique=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Institución'
        verbose_name_plural = 'Instituciones'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class Sede(models.Model):
    nombre = models.CharField(max_length=100)
    institucion = models.ForeignKey(Institucion, on_delete=models.PROTECT, related_name='sedes')
    direccion = models.CharField(max_length=255, blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Sede'
        verbose_name_plural = 'Sedes'
        ordering = ['institucion', 'nombre']
        constraints = [
            models.UniqueConstraint(
                fields=['institucion', 'nombre'],
                name='unique_sede_por_institucion',
            ),
        ]

    def __str__(self):
        return f'{self.institucion.nombre} - {self.nombre}'


class UsuarioSede(models.Model):
    usuario_id = models.IntegerField()
    sede       = models.ForeignKey(Sede, on_delete=models.CASCADE, related_name='usuariosede_set')

    def __str__(self):
        return f'Usuario {self.usuario_id} → {self.sede}'

    class Meta:
        unique_together = ['usuario_id', 'sede']
        verbose_name = 'Asignación de Sede'
        verbose_name_plural = 'Asignaciones de Sede'
