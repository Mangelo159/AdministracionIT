from django.contrib.admin.models import LogEntry
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render

from adm.backends import addUserData, get_permisos


@login_required(redirect_field_name='ret', login_url='/login')
def view(request):
    usuario_tic_id = request.session.get('usuario_tic_id', request.user.id)
    if request.user.is_staff:
        perms = {'puede_ver': True, 'puede_crear': True, 'puede_editar': True, 'puede_eliminar': True}
    else:
        perms = get_permisos(usuario_tic_id, 'auditoria')

    try:
        if not perms['puede_ver']:
            return HttpResponseForbidden()

        logs = (LogEntry.objects
                .select_related('user', 'content_type')
                .order_by('-action_time')[:500])

        content_types = (LogEntry.objects
                         .select_related('content_type')
                         .values('content_type__id', 'content_type__model')
                         .distinct()
                         .order_by('content_type__model'))

        data = {
            'title': 'Auditoría',
            'perms': perms,
            'logs': logs,
            'content_types': content_types,
        }
        addUserData(request, data)
        return render(request, 'auditoria/auditoriabs.html', data)

    except Exception as e:
        return HttpResponseRedirect('/?info=' + str(e))
