from django.contrib import admin
from .models import Modulo, Rol, RolUsuario, RolModuloPermiso, UsuarioTIC


@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    list_display  = ['nombre', 'url', 'activo', 'orden']
    list_filter   = ['activo']
    list_editable = ['activo', 'orden']
    ordering      = ['orden', 'nombre']


@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display  = ['nombre', 'orden', 'descripcion']
    list_editable = ['orden']


@admin.register(RolUsuario)
class RolUsuarioAdmin(admin.ModelAdmin):
    list_display = ['nombre_usuario', 'rol']
    list_filter  = ['rol']

    def nombre_usuario(self, obj):
        u = UsuarioTIC.objects.filter(usuario_id=obj.usuario_id).first()
        return u.nombre_completo if u else obj.usuario_id
    nombre_usuario.short_description = 'Usuario'


@admin.register(RolModuloPermiso)
class RolModuloPermisoAdmin(admin.ModelAdmin):
    list_display  = ['rol', 'modulo', 'puede_ver', 'puede_crear', 'puede_editar', 'puede_eliminar']
    list_filter   = ['rol']
    list_editable = ['puede_ver', 'puede_crear', 'puede_editar', 'puede_eliminar']
