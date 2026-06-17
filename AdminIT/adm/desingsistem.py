from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from adm.backends import addUserData


@login_required(redirect_field_name='ret', login_url='/login')
def view(request):
    data = {'title': 'Sistema de Diseño'}
    addUserData(request, data)
    return render(request, 'plantilla/desingsistem.html', data)
