import json

from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseForbidden, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.encoding import force_str

from adm.backends import addUserData, get_permisos, permiso_para_accion
from adm.models import Rol, RolUsuario, RolModuloPermiso, Modulo, UsuarioTIC, Institucion, Sede, UsuarioSede


@login_required(redirect_field_name='ret', login_url='/login')
def view(request):
    usuario_tic_id = request.session.get('usuario_tic_id', request.user.id)
    if request.user.is_staff:
        perms = {'puede_ver': True, 'puede_crear': True, 'puede_editar': True, 'puede_eliminar': True}
    else:
        perms = get_permisos(usuario_tic_id, 'mantenimiento')

    try:
        if request.method == 'POST':
            accion = request.POST.get('accion', '')
            permiso_requerido = permiso_para_accion(accion)
            if permiso_requerido and not perms.get(permiso_requerido):
                return JsonResponse({'result': 'forbidden'}, status=403)

            client_address = request.META.get('REMOTE_ADDR', '')

            if accion == 'crear_rol':
                try:
                    nombre = request.POST.get('nombre', '').strip()
                    if nombre:
                        rol = Rol.objects.create(
                            nombre=nombre,
                            descripcion=request.POST.get('descripcion', '').strip(),
                            orden=int(request.POST.get('orden') or 0),
                        )
                        LogEntry.objects.log_action(
                            user_id=request.user.pk,
                            content_type_id=ContentType.objects.get_for_model(rol).pk,
                            object_id=rol.pk,
                            object_repr=force_str(rol),
                            action_flag=ADDITION,
                            change_message=f'Creó rol "{rol.nombre}" ({client_address})')
                    return JsonResponse({'result': 'ok'})
                except Exception as ex:
                    return JsonResponse({'result': 'bad', 'error': str(ex)})

            elif accion == 'editar_rol':
                try:
                    rol = get_object_or_404(Rol, id=request.POST.get('rol_id'))
                    rol.nombre      = request.POST.get('nombre', rol.nombre).strip()
                    rol.descripcion = request.POST.get('descripcion', '').strip()
                    rol.orden       = int(request.POST.get('orden') or rol.orden)
                    rol.save()
                    LogEntry.objects.log_action(
                        user_id=request.user.pk,
                        content_type_id=ContentType.objects.get_for_model(rol).pk,
                        object_id=rol.pk,
                        object_repr=force_str(rol),
                        action_flag=CHANGE,
                        change_message=f'Editó rol "{rol.nombre}" ({client_address})')
                    return JsonResponse({'result': 'ok'})
                except Exception as ex:
                    return JsonResponse({'result': 'bad', 'error': str(ex)})

            elif accion == 'eliminar_rol':
                try:
                    rol = get_object_or_404(Rol, id=request.POST.get('rol_id'))
                    LogEntry.objects.log_action(
                        user_id=request.user.pk,
                        content_type_id=ContentType.objects.get_for_model(rol).pk,
                        object_id=rol.pk,
                        object_repr=force_str(rol),
                        action_flag=DELETION,
                        change_message=f'Eliminó rol "{rol.nombre}" ({client_address})')
                    rol.delete()
                    return JsonResponse({'result': 'ok'})
                except Exception as ex:
                    return JsonResponse({'result': 'bad', 'error': str(ex)})

            elif accion == 'crear_asignacion':
                try:
                    usuario_id = request.POST.get('usuario_id')
                    rol_id     = request.POST.get('rol_id')
                    if usuario_id and rol_id:
                        asig, created = RolUsuario.objects.get_or_create(
                            usuario_id=int(usuario_id),
                            rol_id=int(rol_id),
                        )
                        if created:
                            LogEntry.objects.log_action(
                                user_id=request.user.pk,
                                content_type_id=ContentType.objects.get_for_model(asig).pk,
                                object_id=asig.pk,
                                object_repr=force_str(asig),
                                action_flag=ADDITION,
                                change_message=f'Asignó usuario ID {usuario_id} al rol ID {rol_id} ({client_address})')
                    return JsonResponse({'result': 'ok'})
                except Exception as ex:
                    return JsonResponse({'result': 'bad', 'error': str(ex)})

            elif accion == 'eliminar_asignacion':
                try:
                    asig = get_object_or_404(RolUsuario, id=request.POST.get('asignacion_id'))
                    LogEntry.objects.log_action(
                        user_id=request.user.pk,
                        content_type_id=ContentType.objects.get_for_model(asig).pk,
                        object_id=asig.pk,
                        object_repr=force_str(asig),
                        action_flag=DELETION,
                        change_message=f'Eliminó asignación ID {asig.pk} ({client_address})')
                    asig.delete()
                    return JsonResponse({'result': 'ok'})
                except Exception as ex:
                    return JsonResponse({'result': 'bad', 'error': str(ex)})

            elif accion == 'crear_asignacion_sede':
                try:
                    usuario_id = request.POST.get('usuario_id')
                    sede_id    = request.POST.get('sede_id')
                    if usuario_id and sede_id:
                        asig, created = UsuarioSede.objects.get_or_create(
                            usuario_id=int(usuario_id),
                            sede_id=int(sede_id),
                        )
                        if created:
                            LogEntry.objects.log_action(
                                user_id=request.user.pk,
                                content_type_id=ContentType.objects.get_for_model(asig).pk,
                                object_id=asig.pk,
                                object_repr=force_str(asig),
                                action_flag=ADDITION,
                                change_message=f'Asignó usuario ID {usuario_id} a sede ID {sede_id} ({client_address})')
                    return JsonResponse({'result': 'ok'})
                except Exception as ex:
                    return JsonResponse({'result': 'bad', 'error': str(ex)})

            elif accion == 'eliminar_asignacion_sede':
                try:
                    asig = get_object_or_404(UsuarioSede, id=request.POST.get('asignacion_sede_id'))
                    LogEntry.objects.log_action(
                        user_id=request.user.pk,
                        content_type_id=ContentType.objects.get_for_model(asig).pk,
                        object_id=asig.pk,
                        object_repr=force_str(asig),
                        action_flag=DELETION,
                        change_message=f'Eliminó asignación de sede ID {asig.pk} ({client_address})')
                    asig.delete()
                    return JsonResponse({'result': 'ok'})
                except Exception as ex:
                    return JsonResponse({'result': 'bad', 'error': str(ex)})

            elif accion == 'crear_permiso':
                try:
                    rol_id    = request.POST.get('rol_id')
                    modulo_id = request.POST.get('modulo_id')
                    if rol_id and modulo_id:
                        permiso, _ = RolModuloPermiso.objects.get_or_create(
                            rol_id=int(rol_id),
                            modulo_id=int(modulo_id),
                        )
                        for campo in ('puede_ver', 'puede_crear', 'puede_editar', 'puede_eliminar'):
                            setattr(permiso, campo, campo in request.POST)
                        permiso.save()
                        LogEntry.objects.log_action(
                            user_id=request.user.pk,
                            content_type_id=ContentType.objects.get_for_model(permiso).pk,
                            object_id=permiso.pk,
                            object_repr=force_str(permiso),
                            action_flag=ADDITION,
                            change_message=f'Creó permiso rol ID {rol_id} / módulo ID {modulo_id} ({client_address})')
                    return JsonResponse({'result': 'ok'})
                except Exception as ex:
                    return JsonResponse({'result': 'bad', 'error': str(ex)})

            elif accion == 'editar_permiso':
                try:
                    permiso = get_object_or_404(RolModuloPermiso, id=request.POST.get('permiso_id'))
                    for campo in ('puede_ver', 'puede_crear', 'puede_editar', 'puede_eliminar'):
                        setattr(permiso, campo, campo in request.POST)
                    permiso.save()
                    LogEntry.objects.log_action(
                        user_id=request.user.pk,
                        content_type_id=ContentType.objects.get_for_model(permiso).pk,
                        object_id=permiso.pk,
                        object_repr=force_str(permiso),
                        action_flag=CHANGE,
                        change_message=f'Editó permiso ID {permiso.pk} ({client_address})')
                    return JsonResponse({'result': 'ok'})
                except Exception as ex:
                    return JsonResponse({'result': 'bad', 'error': str(ex)})

            elif accion == 'eliminar_permiso':
                try:
                    permiso = get_object_or_404(RolModuloPermiso, id=request.POST.get('permiso_id'))
                    LogEntry.objects.log_action(
                        user_id=request.user.pk,
                        content_type_id=ContentType.objects.get_for_model(permiso).pk,
                        object_id=permiso.pk,
                        object_repr=force_str(permiso),
                        action_flag=DELETION,
                        change_message=f'Eliminó permiso ID {permiso.pk} ({client_address})')
                    permiso.delete()
                    return JsonResponse({'result': 'ok'})
                except Exception as ex:
                    return JsonResponse({'result': 'bad', 'error': str(ex)})

            elif accion == 'crear_modulo':
                try:
                    nombre = request.POST.get('mod_nombre', '').strip()
                    if nombre:
                        mod = Modulo.objects.create(
                            nombre=nombre,
                            url=request.POST.get('mod_url', '').strip(),
                            icono=request.POST.get('mod_icono', '').strip(),
                            descripcion=request.POST.get('mod_descripcion', '').strip(),
                            orden=int(request.POST.get('mod_orden') or 0),
                            activo=True,
                        )
                        LogEntry.objects.log_action(
                            user_id=request.user.pk,
                            content_type_id=ContentType.objects.get_for_model(mod).pk,
                            object_id=mod.pk,
                            object_repr=force_str(mod),
                            action_flag=ADDITION,
                            change_message=f'Creó módulo "{mod.nombre}" ({client_address})')
                    return JsonResponse({'result': 'ok'})
                except Exception as ex:
                    return JsonResponse({'result': 'bad', 'error': str(ex)})

            elif accion == 'editar_modulo':
                try:
                    mod = get_object_or_404(Modulo, id=request.POST.get('modulo_id'))
                    mod.nombre      = request.POST.get('mod_nombre', mod.nombre).strip()
                    mod.url         = request.POST.get('mod_url', mod.url).strip()
                    mod.icono       = request.POST.get('mod_icono', mod.icono).strip()
                    mod.descripcion = request.POST.get('mod_descripcion', mod.descripcion).strip()
                    mod.orden       = int(request.POST.get('mod_orden') or mod.orden)
                    mod.activo      = 'mod_activo' in request.POST
                    mod.save()
                    LogEntry.objects.log_action(
                        user_id=request.user.pk,
                        content_type_id=ContentType.objects.get_for_model(mod).pk,
                        object_id=mod.pk,
                        object_repr=force_str(mod),
                        action_flag=CHANGE,
                        change_message=f'Editó módulo "{mod.nombre}" ({client_address})')
                    return JsonResponse({'result': 'ok'})
                except Exception as ex:
                    return JsonResponse({'result': 'bad', 'error': str(ex)})

            elif accion == 'eliminar_modulo':
                try:
                    mod = get_object_or_404(Modulo, id=request.POST.get('modulo_id'))
                    LogEntry.objects.log_action(
                        user_id=request.user.pk,
                        content_type_id=ContentType.objects.get_for_model(mod).pk,
                        object_id=mod.pk,
                        object_repr=force_str(mod),
                        action_flag=DELETION,
                        change_message=f'Eliminó módulo "{mod.nombre}" ({client_address})')
                    mod.delete()
                    return JsonResponse({'result': 'ok'})
                except Exception as ex:
                    return JsonResponse({'result': 'bad', 'error': str(ex)})

            elif accion == 'crear_institucion':
                try:
                    nombre = request.POST.get('nombre', '').strip()
                    if nombre:
                        inst = Institucion.objects.create(
                            nombre=nombre,
                            activo='activo' in request.POST,
                        )
                        LogEntry.objects.log_action(
                            user_id=request.user.pk,
                            content_type_id=ContentType.objects.get_for_model(inst).pk,
                            object_id=inst.pk,
                            object_repr=force_str(inst),
                            action_flag=ADDITION,
                            change_message=f'Creó institución "{inst.nombre}" ({client_address})')
                    return JsonResponse({'result': 'ok'})
                except Exception as ex:
                    return JsonResponse({'result': 'bad', 'error': str(ex)})

            elif accion == 'editar_institucion':
                try:
                    inst = get_object_or_404(Institucion, id=request.POST.get('inst_id'))
                    inst.nombre = request.POST.get('nombre', inst.nombre).strip()
                    inst.activo = 'activo' in request.POST
                    inst.save()
                    LogEntry.objects.log_action(
                        user_id=request.user.pk,
                        content_type_id=ContentType.objects.get_for_model(inst).pk,
                        object_id=inst.pk,
                        object_repr=force_str(inst),
                        action_flag=CHANGE,
                        change_message=f'Editó institución "{inst.nombre}" ({client_address})')
                    return JsonResponse({'result': 'ok'})
                except Exception as ex:
                    return JsonResponse({'result': 'bad', 'error': str(ex)})

            elif accion == 'eliminar_institucion':
                try:
                    inst = get_object_or_404(Institucion, id=request.POST.get('inst_id'))
                    LogEntry.objects.log_action(
                        user_id=request.user.pk,
                        content_type_id=ContentType.objects.get_for_model(inst).pk,
                        object_id=inst.pk,
                        object_repr=force_str(inst),
                        action_flag=DELETION,
                        change_message=f'Eliminó institución "{inst.nombre}" ({client_address})')
                    inst.delete()
                    return JsonResponse({'result': 'ok'})
                except Exception as ex:
                    return JsonResponse({'result': 'bad', 'error': str(ex)})

            elif accion == 'crear_sede':
                try:
                    nombre    = request.POST.get('nombre', '').strip()
                    inst_id   = request.POST.get('inst_id', '').strip()
                    if nombre and inst_id:
                        sede = Sede.objects.create(
                            nombre=nombre,
                            institucion_id=int(inst_id),
                            direccion=request.POST.get('direccion', '').strip(),
                            activo='activo' in request.POST,
                        )
                        LogEntry.objects.log_action(
                            user_id=request.user.pk,
                            content_type_id=ContentType.objects.get_for_model(sede).pk,
                            object_id=sede.pk,
                            object_repr=force_str(sede),
                            action_flag=ADDITION,
                            change_message=f'Creó sede "{sede}" ({client_address})')
                    return JsonResponse({'result': 'ok'})
                except Exception as ex:
                    return JsonResponse({'result': 'bad', 'error': str(ex)})

            elif accion == 'editar_sede':
                try:
                    sede = get_object_or_404(Sede, id=request.POST.get('sede_id'))
                    sede.nombre       = request.POST.get('nombre', sede.nombre).strip()
                    sede.institucion_id = int(request.POST.get('inst_id') or sede.institucion_id)
                    sede.direccion    = request.POST.get('direccion', '').strip()
                    sede.activo       = 'activo' in request.POST
                    sede.save()
                    LogEntry.objects.log_action(
                        user_id=request.user.pk,
                        content_type_id=ContentType.objects.get_for_model(sede).pk,
                        object_id=sede.pk,
                        object_repr=force_str(sede),
                        action_flag=CHANGE,
                        change_message=f'Editó sede "{sede}" ({client_address})')
                    return JsonResponse({'result': 'ok'})
                except Exception as ex:
                    return JsonResponse({'result': 'bad', 'error': str(ex)})

            elif accion == 'eliminar_sede':
                try:
                    sede = get_object_or_404(Sede, id=request.POST.get('sede_id'))
                    LogEntry.objects.log_action(
                        user_id=request.user.pk,
                        content_type_id=ContentType.objects.get_for_model(sede).pk,
                        object_id=sede.pk,
                        object_repr=force_str(sede),
                        action_flag=DELETION,
                        change_message=f'Eliminó sede "{sede}" ({client_address})')
                    sede.delete()
                    return JsonResponse({'result': 'ok'})
                except Exception as ex:
                    return JsonResponse({'result': 'bad', 'error': str(ex)})

        else:
            if not perms['puede_ver']:
                return HttpResponseForbidden()

            data = {'title': 'Mantenimiento', 'perms': perms}
            addUserData(request, data)

            if 'action' in request.GET:
                action = request.GET['action']

                if action == 'roles':
                    usuarios_qs = UsuarioTIC.objects.values('usuario_id', 'nombre_completo', 'cedula', 'grupo').order_by('nombre_completo').distinct()
                    usuarios_dict = {u['usuario_id']: u for u in usuarios_qs}
                    asignaciones_raw = RolUsuario.objects.select_related('rol').order_by('rol__orden', 'rol__nombre')
                    asignaciones = []
                    for asig in asignaciones_raw:
                        u = usuarios_dict.get(asig.usuario_id)
                        asignaciones.append({
                            'id':     asig.id,
                            'nombre': u['nombre_completo'] if u else f'ID {asig.usuario_id}',
                            'cedula': u['cedula'] if u else '',
                            'rol':    asig.rol.nombre,
                        })
                    data['roles']        = Rol.objects.all()
                    data['asignaciones'] = asignaciones
                    data['permisos']     = RolModuloPermiso.objects.select_related('rol', 'modulo').order_by('rol__orden', 'modulo__orden')
                    data['usuarios']     = usuarios_qs
                    return render(request, "mantenimiento/mroles.html", data)

                elif action == 'modulo':
                    data['modulos'] = Modulo.objects.order_by('orden', 'nombre')
                    return render(request, "mantenimiento/mmodulo.html", data)

                elif action == 'asignaciones':
                    usuarios_qs = UsuarioTIC.objects.values('usuario_id', 'nombre_completo', 'cedula', 'grupo').order_by('nombre_completo').distinct()
                    usuarios_dict = {u['usuario_id']: u for u in usuarios_qs}
                    asignaciones_raw = RolUsuario.objects.select_related('rol').order_by('rol__orden', 'rol__nombre')
                    asignaciones = []
                    usuarios_con_rol_ids = set()
                    for asig in asignaciones_raw:
                        u = usuarios_dict.get(asig.usuario_id)
                        usuarios_con_rol_ids.add(asig.usuario_id)
                        asignaciones.append({
                            'id':     asig.id,
                            'nombre': u['nombre_completo'] if u else f'ID {asig.usuario_id}',
                            'cedula': u['cedula'] if u else '',
                            'rol':    asig.rol.nombre,
                        })
                    asignaciones_sede_raw = UsuarioSede.objects.select_related('sede__institucion').order_by('sede__institucion__nombre', 'sede__nombre')
                    asignaciones_sede = []
                    for asig in asignaciones_sede_raw:
                        u = usuarios_dict.get(asig.usuario_id)
                        asignaciones_sede.append({
                            'id':          asig.id,
                            'nombre':      u['nombre_completo'] if u else f'ID {asig.usuario_id}',
                            'cedula':      u['cedula'] if u else '',
                            'sede':        asig.sede.nombre,
                            'institucion': asig.sede.institucion.nombre,
                        })
                    data['roles']             = Rol.objects.all()
                    data['asignaciones']      = asignaciones
                    data['asignaciones_sede'] = asignaciones_sede
                    data['usuarios']          = usuarios_qs
                    data['usuarios_con_rol']  = [u for u in usuarios_qs if u['usuario_id'] in usuarios_con_rol_ids]
                    data['sedes']             = Sede.objects.select_related('institucion').filter(activo=True).order_by('institucion__nombre', 'nombre')
                    data['instituciones']     = Institucion.objects.filter(activo=True).order_by('nombre')
                    return render(request, "mantenimiento/masignaciones.html", data)

                elif action == 'permisos':
                    data['roles']   = Rol.objects.all()
                    data['modulos'] = Modulo.objects.order_by('orden', 'nombre')
                    data['permisos'] = RolModuloPermiso.objects.select_related('rol', 'modulo').order_by('rol__orden', 'modulo__orden')
                    return render(request, "mantenimiento/mpermisos.html", data)

                elif action == 'instituciones':
                    data['instituciones'] = Institucion.objects.all()
                    return render(request, "mantenimiento/minstituciones.html", data)

                elif action == 'sedes':
                    data['sedes']        = Sede.objects.select_related('institucion').all()
                    data['instituciones'] = Institucion.objects.filter(activo=True).order_by('nombre')
                    return render(request, "mantenimiento/msedes.html", data)

            else:
                data['roles']         = Rol.objects.all()
                data['modulos']       = Modulo.objects.order_by('orden', 'nombre')
                data['asignaciones']  = RolUsuario.objects.all()
                data['permisos']      = RolModuloPermiso.objects.all()
                data['instituciones'] = Institucion.objects.all()
                data['sedes']         = Sede.objects.all()
                return render(request, "mantenimiento/mantenimientobs.html", data)

    except Exception as e:
        return HttpResponseRedirect('/?info=' + str(e))
