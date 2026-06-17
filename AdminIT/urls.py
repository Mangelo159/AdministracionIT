from django.urls import re_path as url, path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
import django.views.static
from django.contrib import admin

import settings
from adm import views, mantenimiento, desingsistem, auditoria

admin.autodiscover()
handler404 = views.error_404
handler500 = views.error_500

urlpatterns = []
if not settings.DEBUG:
    urlpatterns = [
        url(r'^static/(?P<path>.*)$', django.views.static.serve,
            {'document_root': settings.STATIC_ROOT}),
        url(r'^media/(?P<path>.*)$', django.views.static.serve,
            {'document_root': settings.MEDIA_ROOT}),
    ]

urlpatterns += [
    url(r'^admin/', admin.site.urls),
    url(r'^login$', views.login_view, name='login'),
    url(r'^logout$', views.logout_view, name='logout'),
    url(r'^$', views.home, name='home'),
    url(r'^mantenimiento$', mantenimiento.view, name='mantenimiento'),
    url(r'^desingsistem', desingsistem.view, name='Plantillas de Diseño'),
    url(r'^auditoria', auditoria.view, name='Auditoria, Registro del Sistema'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
