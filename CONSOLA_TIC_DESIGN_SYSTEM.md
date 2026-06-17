# Prompt de Diseño — Sistema "Consola TIC" (Administración TIC · ITB)

Copia y pega este prompt (completo o por secciones) cada vez que pidas una nueva pantalla, componente o módulo. Garantiza que todo el sistema mantenga la misma identidad visual.

---

## PROMPT

Diseña la interfaz siguiendo el sistema de diseño **"Consola TIC"**, una estética de consola de operaciones tecnológicas: precisa, técnica, institucional y moderna. No uses estilos genéricos de Bootstrap ni plantillas; cada decisión visual debe derivarse de los tokens y principios siguientes.

### 1. Concepto

La interfaz es el **centro de control de la infraestructura tecnológica de un instituto**. Debe transmitir: orden, seguridad, monitoreo en tiempo real y dominio técnico. El usuario es personal TIC autorizado; el tono es profesional y directo, nunca decorativo ni infantil.

### 2. Paleta de colores (tokens CSS)

```css
:root {
    --ink:        #0A1628;  /* fondo oscuro principal / texto sobre claro */
    --ink-2:      #0F1F38;  /* fondo oscuro secundario (gradientes) */
    --azul:       #2D7FF9;  /* color de marca: acciones, focus, acentos */
    --azul-hover: #1C6BE3;  /* hover de acciones primarias */
    --cian:       #22D3EE;  /* acento técnico: pulsos, highlights, datos vivos */
    --hueso:      #F6F8FB;  /* fondo claro principal */
    --niebla:     #8A97AB;  /* texto secundario, iconos en reposo */
    --linea:      rgba(138, 151, 171, 0.22); /* bordes y divisores */
    --error:      #E5484D;  /* errores */
    --ok:         #30C48D;  /* estados operativos / éxito */
    --radio:      14px;     /* border-radius estándar */
    --sombra:     0 24px 60px -24px rgba(10, 22, 40, 0.45);
}
```

Reglas de uso:
- Fondos de trabajo siempre en `--hueso`; paneles de identidad/estado en oscuro (`--ink` → `--ink-2` con gradiente).
- `--azul` se reserva para acciones e interacción. `--cian` solo para detalles "vivos" (telemetría, pulsos, datos en tiempo real). Nunca usar ambos como fondo grande.
- `--ok` y `--error` solo comunican estado, jamás decoración.

### 3. Tipografía

- **IBM Plex Sans** (400/500/600/700): todo el contenido, títulos y formularios.
- **IBM Plex Mono** (400/500): exclusivamente para lenguaje "de sistema" — eyebrows, etiquetas técnicas, relojes, IDs, códigos, chips de estado, metadatos. Siempre con `letter-spacing` amplio (0.06em–0.22em) y frecuentemente en MAYÚSCULAS a tamaño pequeño (10.5–12px).
- Títulos: peso 700, `letter-spacing: -0.02em`, interlineado 1.1–1.2.
- Jerarquía: eyebrow mono → título grande → subtítulo en `--niebla`.

### 4. Firma visual del sistema

Estos elementos son la identidad reconocible; úsalos con moderación (1–2 por pantalla):

1. **Eyebrow con guion**: etiqueta mono uppercase precedida por una línea de 26px en `--azul` (`.eyebrow::before`).
2. **Trazas de circuito**: paths SVG ortogonales con esquinas redondeadas (`q 16 0 16 16`) en azul translúcido, con un "pulso" de luz cian animado (`stroke-dasharray` + `stroke-dashoffset`) recorriéndolas. Solo en paneles oscuros.
3. **Malla de puntos**: `radial-gradient` de 1px cada 26px con máscara elíptica, sobre fondos oscuros.
4. **Chips de estado**: píldora con borde y fondo translúcidos del color de estado, punto con animación de latido (`box-shadow` expansivo), texto mono uppercase.
5. **Tarjetas de telemetría**: bordes `rgba(blanco, 0.14)`, fondo `rgba(blanco, 0.05)`, `backdrop-filter: blur(6px)`, etiqueta mono pequeña arriba y valor en sans abajo.

### 5. Componentes

**Inputs**: altura 50px, borde 1.5px `--linea`, radio `--radio`, icono lineal (stroke 2) a la izquierda en `--niebla` que cambia a `--azul` con focus. Focus: borde azul + `box-shadow: 0 0 0 4px rgba(45,127,249,0.14)`. Placeholder en #B9C2CF.

**Botón primario**: alto 52px, fondo `--azul`, texto blanco 600, radio `--radio`, sombra azul difusa (`0 10px 24px -10px rgba(45,127,249,0.55)`), icono de flecha que se desplaza 3px al hover, `translateY(1px)` al hacer clic.

**Botones secundarios**: fondo transparente, borde `--linea`, texto `--ink`; hover con fondo `rgba(138,151,171,0.12)`.

**Alertas**: fondo del color de estado al 8% de opacidad, borde al 35%, icono lineal a la izquierda, radio 10px, texto 13.5px.

**Tablas/listas (módulos internos)**: cabeceras en mono uppercase pequeño color `--niebla`, filas con divisor `--linea`, hover de fila con fondo `rgba(45,127,249,0.05)`, estados como chips.

**Tarjetas**: fondo blanco sobre `--hueso`, borde `--linea`, radio `--radio`, sombra `--sombra` solo si la tarjeta es protagonista.

### 6. Layout

- Pantallas de acceso/identidad: grid dividido `minmax(420px, 5fr) 7fr` — formulario claro a la izquierda, panel oscuro narrativo a la derecha.
- Módulos internos: sidebar oscura (`--ink`) con navegación en mono/sans pequeño + área de contenido en `--hueso` con cabecera que repite el patrón eyebrow → título.
- Espaciado generoso: `clamp()` para paddings (ej. `clamp(32px, 6vw, 96px)`), máximos de ancho de texto en 46–60ch.
- En móvil: el panel oscuro colapsa a cabecera; sidebar se vuelve menú; ocultar telemetría decorativa.

### 7. Movimiento

- Transiciones de 0.15–0.3s con `ease`; nada de rebotes ni efectos llamativos.
- Una sola animación ambiental por pantalla (pulsos de circuito o latido de estado), el resto son micro-interacciones de hover/focus.
- Respetar siempre `prefers-reduced-motion: reduce` (desactivar pulsos y latidos).

### 8. Accesibilidad y calidad (no negociable)

- `:focus-visible` visible en todo elemento interactivo (anillo azul).
- `aria-label` / `aria-pressed` en toggles; `role="alert"` y `aria-live` en mensajes.
- Contraste AA mínimo; texto secundario nunca por debajo de `--niebla` sobre `--hueso`.
- Detalles pro esperados: aviso de Bloq Mayús en contraseñas, autocomplete correcto, estados vacíos con instrucción de acción, errores que dicen qué pasó y cómo corregirlo.

### 9. Voz y redacción (español)

- Verbos directos y en sentencia: "Ingresar al sistema", "Guardar cambios", "Crear usuario".
- Lenguaje del usuario, no del sistema: "credenciales institucionales", no "auth payload".
- Metadatos y estados en registro técnico breve: "Conexión · Cifrada TLS", "Sesión · Auditada".
- Sin signos de exclamación, sin disculpas en errores, sin relleno.

### 10. Prohibido

- Bootstrap visual por defecto, gradientes arcoíris, sombras duras, emojis en la UI, bordes a 0px de radio mezclados con redondeados, más de un acento de color por componente, animaciones que no comuniquen estado.

---

## 11. Integración en Django

Este proyecto es Django. Toda pantalla nueva o modificada DEBE seguir estas reglas de implementación, no solo las visuales:

### Estructura de archivos

```
proyecto/
├── static/
│   ├── css/
│   │   ├── consola-tic.css      ← sistema de diseño (tokens + componentes). NO se toca por página.
│   │   └── paginas/
│   │       ├── login.css        ← solo estilos exclusivos de esa página
│   │       └── usuarios.css
│   ├── js/
│   │   └── consola-tic.js       ← utilidades compartidas (toggle contraseña, bloq mayús, reloj)
│   └── images/
└── templates/
    ├── base.html                ← carga consola-tic.css y define bloques
    └── ...
```

### Reglas obligatorias

1. **Nunca CSS inline ni `<style>` con tokens duplicados.** Los colores, radios, sombras y fuentes SOLO viven en `static/css/consola-tic.css` como variables CSS (`:root`). Las páginas consumen `var(--azul)`, `var(--radio)`, etc.
2. **Siempre `{% load static %}`** y rutas con `{% static 'css/consola-tic.css' %}`, nunca rutas absolutas escritas a mano.
3. **Todo template extiende `base.html`** con `{% extends 'base.html' %}` y usa los bloques `{% block titulo %}`, `{% block css_pagina %}`, `{% block contenido %}`, `{% block js_pagina %}`. Excepción: pantallas de acceso (login) pueden tener su propio base ligero `base_acceso.html`.
4. **Preservar SIEMPRE la lógica Django existente** al rediseñar: `{% csrf_token %}`, `{% if %}`, `{% for %}`, `{{ variables }}`, `{% url %}`, names de inputs y actions de formularios quedan intactos. El rediseño solo cambia clases, estructura HTML y estilos.
5. **Mensajes de Django**: el bloque de `messages` usa las clases del sistema (`alerta alerta-error`, `alerta-exito`, etc.), que ya mapean los tags `error/success/info/warning`:
   ```html
   {% if messages %}
       {% for message in messages %}
           <div class="alerta alerta-{{ message.tags }}" role="alert">{{ message }}</div>
       {% endfor %}
   {% endif %}
   ```
6. **Formularios de Django Forms**: si se usa `{{ form }}`, renderizar campo por campo con la estructura `.campo > label + .control > input` aplicando las clases vía widget attrs en `forms.py`:
   ```python
   widgets = {
       'username': forms.TextInput(attrs={'placeholder': 'usuario.institucional', 'autocomplete': 'username'}),
   }
   ```
   El estilo lo dan las clases del sistema en el template, no estilos en Python.
7. **JS compartido en `consola-tic.js`**: toggle de contraseña, aviso de Bloq Mayús y reloj son utilidades globales; las páginas solo las invocan, no las reescriben.
8. **Al modificar una página existente**: leer primero el template actual, conservar toda su lógica de negocio, reemplazar solo la capa visual (Bootstrap u otra) por las clases del sistema Consola TIC, y mover cualquier `<style>` embebido a `static/css/paginas/<pagina>.css`.

### Plantilla base de referencia (`base.html`)

```html
{% load static %}
<!doctype html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block titulo %}Administración TIC{% endblock %}</title>
    <link rel="shortcut icon" href="{% static 'images/itb/favicon.ico' %}">
    <link rel="stylesheet" href="{% static 'css/consola-tic.css' %}">
    {% block css_pagina %}{% endblock %}
</head>
<body>
    {% block contenido %}{% endblock %}
    <script src="{% static 'js/consola-tic.js' %}"></script>
    {% block js_pagina %}{% endblock %}
</body>
</html>
```

### Instrucción para la IA (incluir al pedir cambios)

> Este es un proyecto Django con el sistema de diseño Consola TIC ya instalado en `static/css/consola-tic.css`. Modifica el template que te paso aplicando las clases del sistema (`.campo`, `.control`, `.btn-primario`, `.alerta`, `.chip`, `.tarjeta`, `.tabla`, `.eyebrow`, etc.) SIN cambiar su lógica Django (csrf, urls, names, condicionales, bucles). Si necesitas estilos nuevos exclusivos de esta página, créalos en `static/css/paginas/` usando las variables CSS del sistema; nunca inventes colores ni fuentes nuevas.

---

## Mini-prompt (versión corta para pegar rápido)

> Proyecto Django con sistema de diseño "Consola TIC" en `static/css/consola-tic.css`: fondo claro #F6F8FB con paneles oscuros #0A1628; acción en #2D7FF9, acento vivo #22D3EE, estados #30C48D/#E5484D; tipografía IBM Plex Sans + IBM Plex Mono (mono solo para etiquetas técnicas uppercase con tracking amplio); radio 14px; usa las clases del sistema (.campo, .control, .btn-primario, .alerta, .chip, .tarjeta, .tabla, .eyebrow); estilos exclusivos de página en `static/css/paginas/` con variables CSS, nunca inline; carga con `{% static %}` y extiende `base.html`; conserva intacta toda la lógica Django (csrf, names, urls, if/for); accesible (focus-visible, aria, reduced-motion); copy en español, directo y técnico.
