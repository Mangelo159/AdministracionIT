from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Rol, Modulo, UsuarioTIC


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            tic = UsuarioTIC.objects.filter(username=username).values('usuario_id').first()
            if tic:
                request.session['usuario_tic_id'] = tic['usuario_id']
            return HttpResponseRedirect('/')
        error = 'Usuario o contraseña incorrectos.'
    return render(request, 'login.html', {'error': error})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login')


@login_required(login_url='/login')
def home(request):
    usuario_tic_id = request.session.get('usuario_tic_id', request.user.id)
    persona  = UsuarioTIC.objects.filter(usuario_id=usuario_tic_id).first()
    roles    = Rol.objects.filter(rolusuario_set__usuario_id=usuario_tic_id).order_by('orden')

    grupos = []
    for rol in roles:
        modulos = Modulo.objects.filter(
            rolmodulopermiso__rol=rol,
            rolmodulopermiso__puede_ver=True,
            activo=True
        ).order_by('orden')
        if modulos.exists():
            grupos.append({'nombre': rol.nombre, 'modulos': modulos})

    return render(request, 'home.html', {
        'user':    request.user,
        'persona': persona,
        'roles':   roles,
        'grupos':  grupos,
    })


def error_404(request, exception=None):
    return render(request, 'error/404.html', status=404)


def error_500(request):
    return render(request, 'error/500.html', status=500)
