import datetime

from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import check_password
from .models import UsuarioTIC, Rol, RolModuloPermiso


class SistemaPrincipalBackend:

    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username or not password:
            return None

        # Buscar en la vista (lee del sistema principal via dblink)
        usuario_tic = UsuarioTIC.objects.filter(username=username).first()

        if not usuario_tic or not usuario_tic.is_active:
            return None

        if not check_password(password, usuario_tic.password):
            return None

        # Credenciales válidas — get or create usuario local
        user, creado = User.objects.get_or_create(
            username=username,
            defaults={'is_active': True}
        )
        if creado:
            user.set_unusable_password()
            user.save()

        # Sincronizar grupos desde la vista
        nombres_grupos = list(
            UsuarioTIC.objects.filter(username=username).values_list('grupo', flat=True)
        )
        if nombres_grupos:
            grupos = []
            for nombre in nombres_grupos:
                grupo, _ = Group.objects.get_or_create(name=nombre)
                grupos.append(grupo)
            user.groups.set(grupos)

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

def addUserData(request, data):
    if request.user.is_authenticated:
        try:
            persona = UsuarioTIC.objects.get(username=request.user.username)
            data['persona'] = persona
        except UsuarioTIC.DoesNotExist:
            pass
    data['currenttime'] = datetime.datetime.now()


def get_permisos(usuario_tic_id, url_modulo):
    roles = Rol.objects.filter(rolusuario_set__usuario_id=usuario_tic_id)
    qs = RolModuloPermiso.objects.filter(rol__in=roles, modulo__url=url_modulo)
    return {
        'puede_ver':      qs.filter(puede_ver=True).exists(),
        'puede_crear':    qs.filter(puede_crear=True).exists(),
        'puede_editar':   qs.filter(puede_editar=True).exists(),
        'puede_eliminar': qs.filter(puede_eliminar=True).exists(),
    }


_PREFIJO_PERMISO = {'crear': 'puede_crear', 'editar': 'puede_editar', 'eliminar': 'puede_eliminar'}

def permiso_para_accion(accion):
    """Devuelve el flag requerido para una acción con prefijo crear_/editar_/eliminar_."""
    return _PREFIJO_PERMISO.get(accion.split('_')[0])


