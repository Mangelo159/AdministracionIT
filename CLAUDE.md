# CLAUDE.md — Consola TIC · ITB-UBE

## Regla obligatoria: Design System

**Cada vez que se cree o modifique un componente CSS en `AdminIT/static/css/diseñobs.css`, se debe actualizar también el showcase en `AdminIT/templates/desingsistem.html`.**

### Qué cuenta como "nuevo componente"
- Una clase CSS nueva (`.nueva-clase { … }`) agregada a `diseñobs.css`
- Una variante nueva de un componente existente (ej. `.chip.chip-nuevo`)
- Un bloque de clases relacionadas que conformen un patrón visual (ej. un nuevo tipo de tarjeta, un nuevo layout)

### Cómo actualizar el showcase
1. Ubica la sección temática correcta en `desingsistem.html` (01 tokens, 02 tipo, 03 botones, etc.) o crea una sección nueva numerada si el componente no encaja en ninguna existente.
2. Agrega un demo en vivo con HTML real usando las clases nuevas — no solo el nombre de la clase.
3. Incluye debajo un `.ds-label` con el nombre de las clases involucradas en la sintaxis `padre → hijo · variante`.
4. Si el componente requiere JavaScript (como `.c-select`), agrégalo también en `{% block js_pagina %}` del showcase.

### Estructura de secciones actuales
| # | ID | Contenido |
|---|---|---|
| 01 | `#s-color` | Paleta de tokens de color |
| 02 | `#s-tipo` | Escala tipográfica |
| 03 | `#s-btn` | Botones y acciones |
| 04 | `#s-alertas` | Alertas y mensajes |
| 05 | `#s-chips` | Chips y badges de estado |
| 06 | `#s-tarjetas` | Tarjetas y métricas KPI |
| 07 | `#s-forms` | Formularios, inputs, selects, checkboxes |
| 08 | `#s-tabla` | Tabla `.tabla` con `.panel-tabla` |
| 09 | `#s-pag` | Paginación |
| 10 | `#s-util` | Separadores y estado vacío |
| 11 | `#s-tokens` | Tokens visuales: radios y sombras |
| 12 | `#s-hub` | Hub cabecera `.hub-cabecera` |
| 13 | `#s-modulos` | Módulo cards (home) |
| 14 | `#s-layout-panel` | Layout lista + panel lateral |
| 15 | `#s-buscador` | Buscador card básico |
| 16 | `#s-roles-panel` | Panel de datos `.roles-panel` + `.roles-tabla` |
| 17 | `#s-modal` | Modal `.roles-modal` |
| 18 | `#s-mant-cards` | Cards hub mantenimiento `.mant-card` |
| 19 | `#s-cab-dark` | Cabecera oscura `.cabecera-pagina-dark` |

---

## Stack del proyecto

- **Framework**: Django 3/4, app `adm/`, PostgreSQL en puerto 5433
- **CSS**: Bootstrap 2 (legacy) + `diseñobs.css` (sistema de diseño propio, carga después de Bootstrap)
- **JS**: Alpine.js (global, para navbar), `consola-tic.js` (global, contiene `initCSelect` e `initPaginador`)
- **Tipografía**: IBM Plex Sans + IBM Plex Mono vía Google Fonts CDN
- **Tokens**: definidos en `:root` de `diseñobs.css` — usar siempre `var(--token)`, nunca valores hardcoded

## Patrón de vistas

```python
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from adm.backends import addUserData

@login_required(redirect_field_name='ret', login_url='/login')
def view(request):
    data = {'title': 'Título de la página'}
    addUserData(request, data)
    return render(request, 'nombre-template.html', data)
```

## Regla obligatoria: Control de acciones por rol

**Las acciones de ver, crear, editar y eliminar deben estar validadas por los permisos del rol del usuario, tanto en el servidor (vista) como en el cliente (template).**

El modelo `RolModuloPermiso` define cuatro flags por combinación `(rol, módulo)`:
- `puede_ver` — acceso a la página/listado
- `puede_crear` — botón/formulario de alta
- `puede_editar` — botón/formulario de edición
- `puede_eliminar` — botón/acción de baja

### Patrón en la vista

Usar el helper a continuación para resolver los permisos efectivos del usuario (unión de todos sus roles):

```python
from adm.models import RolModuloPermiso, Rol

def get_permisos(usuario_tic_id, url_modulo):
    roles = Rol.objects.filter(rolusuario_set__usuario_id=usuario_tic_id)
    qs = RolModuloPermiso.objects.filter(rol__in=roles, modulo__url=url_modulo)
    return {
        'puede_ver':      qs.filter(puede_ver=True).exists(),
        'puede_crear':    qs.filter(puede_crear=True).exists(),
        'puede_editar':   qs.filter(puede_editar=True).exists(),
        'puede_eliminar': qs.filter(puede_eliminar=True).exists(),
    }
```

En la vista, pasar `perms` al contexto y bloquear en el servidor:

```python
@login_required(redirect_field_name='ret', login_url='/login')
def mi_vista(request):
    usuario_tic_id = request.session.get('usuario_tic_id', request.user.id)
    perms = get_permisos(usuario_tic_id, 'nombre-del-modulo')  # coincide con Modulo.url

    if not perms['puede_ver']:
        return HttpResponseForbidden()

    if request.method == 'POST':
        accion = request.POST.get('accion')
        if accion == 'crear'   and not perms['puede_crear']:    return HttpResponseForbidden()
        if accion == 'editar'  and not perms['puede_editar']:   return HttpResponseForbidden()
        if accion == 'eliminar' and not perms['puede_eliminar']: return HttpResponseForbidden()

    data = {'title': '...', 'perms': perms}
    addUserData(request, data)
    return render(request, 'template.html', data)
```

### Patrón en el template

Envolver cada acción con la variable `perms` recibida del contexto:

```html
{% if perms.puede_crear %}
  <a href="..." class="btn-tic btn-tic-primary">Nuevo</a>
{% endif %}

{% if perms.puede_editar %}
  <a href="..." class="btn-tic btn-tic-secondary">Editar</a>
{% endif %}

{% if perms.puede_eliminar %}
  <button type="button" class="btn-tic btn-tic-danger">Eliminar</button>
{% endif %}
```

### Reglas de aplicación

- La comprobación en el servidor es obligatoria; la del template es adicional (UX).
- Si el usuario no tiene `puede_ver`, retornar `HttpResponseForbidden()` antes de cualquier query.
- Nunca ocultar botones solo con CSS — el bloqueo real va en la vista.
- El parámetro `url_modulo` en `get_permisos` debe coincidir exactamente con el campo `Modulo.url` en base de datos.

---

## Regla obligatoria: Auditoría con LogEntry

**Toda acción de crear, editar o eliminar sobre cualquier modelo debe registrarse con `LogEntry` de Django admin. Sin log, la acción no está completa.**

La tabla `django_admin_log` es el registro de auditoría del sistema. Es obligatorio loguear en el servidor inmediatamente después de confirmar que la operación fue exitosa.

### Imports requeridos

```python
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_str
```

### Patrón por acción

```python
client_address = request.META.get('REMOTE_ADDR', '')
ct = ContentType.objects.get_for_model(objeto)

# CREAR
LogEntry.objects.log_action(
    user_id=request.user.pk, content_type_id=ct.pk,
    object_id=objeto.pk, object_repr=force_str(objeto),
    action_flag=ADDITION,
    change_message=f'Creó {objeto} ({client_address})')

# EDITAR
LogEntry.objects.log_action(
    user_id=request.user.pk, content_type_id=ct.pk,
    object_id=objeto.pk, object_repr=force_str(objeto),
    action_flag=CHANGE,
    change_message=f'Editó {objeto} ({client_address})')

# ELIMINAR
LogEntry.objects.log_action(
    user_id=request.user.pk, content_type_id=ct.pk,
    object_id=objeto.pk, object_repr=force_str(objeto),
    action_flag=DELETION,
    change_message=f'Eliminó {objeto} ({client_address})')
```

### Reglas de aplicación

- El log va **después** de que la operación sobre la base de datos fue exitosa, nunca antes.
- Usar `change_message` descriptivo: incluir qué cambió y la IP del cliente (`client_address`).
- El `object_repr` debe ser legible para humanos (el `__str__` del modelo).
- Aplica a **todas las vistas** del proyecto, sin excepción: personal, equipos, roles, módulos, etc.
- La auditoría es visible en `/admin/admin/logentry/`.

---

## Regla obligatoria: Selects con `.c-select`

**Nunca usar `<select>` nativo en templates. Todo selector desplegable debe usar el componente `.c-select` del design system.**

### Estructura HTML

```html
<input type="hidden" name="campo_id" id="campo-val">
<div class="c-select" id="cs-campo">
  <button type="button" class="c-select-trigger" aria-haspopup="listbox">
    <span class="c-select-label">— Seleccionar —</span>
    <svg class="c-select-chevron" width="10" height="6" viewBox="0 0 10 6" fill="none" aria-hidden="true">
      <path d="M1 1l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  </button>
  <div class="c-select-panel" role="listbox">
    <div class="c-select-option selected" data-value="">— Seleccionar —</div>
    {% for item in items %}
    <div class="c-select-option" data-value="{{ item.id }}">{{ item.nombre }}</div>
    {% endfor %}
  </div>
</div>
```

### Inicialización JS

```javascript
var cscampo = initCSelect('cs-campo', function() {
  document.getElementById('campo-val').value = cscampo.getValue();
});
```

### Tamaños de alto disponibles

| Clase | Alto | Uso |
|---|---|---|
| `.c-select--s` | 28 px | Filtros compactos dentro de `.buscador-fila` |
| `.c-select--m` | 36 px | Default — campos en modales |
| `.c-select--l` | 44 px | Formularios de página completa |
| `.c-select--xl` | 52 px | Selects de alta jerarquía visual |

### Anchos disponibles

| Clase | Ancho | Uso |
|---|---|---|
| `.c-select--full` | 100% | Siempre dentro de modales y formularios de página |
| `.c-select--w-xs` | 120 px | Selects de códigos cortos |
| `.c-select--w-sm` | 180 px | Selects de categorías breves |
| `.c-select--w-md` | 260 px | Selects estándar en layouts libres |
| `.c-select--w-lg` | 360 px | Selects con opciones largas |
| `.c-select--w-xl` | 480 px | Selects en cabeceras o destacados |

### Combinaciones por contexto

| Contexto | Clases a usar |
|---|---|
| Filtro en `.buscador-fila` | solo `.c-select` (sin modificador) |
| Campo en modal `.roles-modal` | `.c-select--m .c-select--full` |
| Campo en formulario de página | `.c-select--l .c-select--full` |
| Select pequeño en tabla o chip | `.c-select--s .c-select--w-sm` |

### Reglas de aplicación

- El valor se envía mediante un `<input type="hidden">` vinculado al callback de `initCSelect`.
- Validar manualmente antes del submit que el hidden input tenga valor (el browser no valida `required` en hidden).
- Al resetear un formulario, llamar también `cscampo.reset()` para limpiar la etiqueta visible.
- Aplica en modales, formularios de página y filtros de búsqueda — sin excepciones.

---

## CSS — reglas de estilo

- Todo CSS nuevo va en `diseñobs.css`. No crear archivos `css/paginas/*.css` nuevos.
- Los templates deben tener `{% block extrahead %}{% endblock %}` vacío — sin `<link>` a CSS de página.
- El showcase `desingsistem.html` no carga CSS adicional: todo viene de `diseñobs.css` vía `basebs.html`.
