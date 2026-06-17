from django.http import HttpResponseForbidden
from .models import Modulo, RolModuloPermiso, UsuarioTIC

RUTAS_EXENTAS = {'/', '/login', '/logout'}


class RolAccesoMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.permiso = None

        if (request.user.is_authenticated
                and request.path not in RUTAS_EXENTAS
                and not request.path.startswith('/admin/')
                and not request.path.startswith('/static/')
                and not request.path.startswith('/media/')):

            # Obtener usuario_tic_id — de sesión si ya está, si no buscarlo por username
            usuario_tic_id = request.session.get('usuario_tic_id')
            if not usuario_tic_id:
                tic = UsuarioTIC.objects.filter(
                    username=request.user.username
                ).values('usuario_id').first()
                if tic:
                    usuario_tic_id = tic['usuario_id']
                    request.session['usuario_tic_id'] = usuario_tic_id

            path = request.path.strip('/')
            modulo = Modulo.objects.filter(url__icontains=path, activo=True).first()

            if modulo and usuario_tic_id:
                permiso = RolModuloPermiso.objects.filter(
                    rol__rolusuario_set__usuario_id=usuario_tic_id,
                    modulo=modulo,
                    puede_ver=True
                ).first()
                if not permiso:
                    return HttpResponseForbidden('No tienes acceso a este módulo.')
                request.permiso = permiso

        return self.get_response(request)
