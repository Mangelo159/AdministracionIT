# MIGRACION.md — Bootstrap 2 → Tailwind CSS v4

Última actualización: 2026-06-10

---

## Estado actual

### ✅ Completado

| Componente | Descripción |
|------------|-------------|
| **Tailwind CSS v4** | Instalado vía npm (`tailwindcss@4.3.0`). Tokens del sistema de diseño en `static/css/input.css` con `@theme`. Output en `static/css/tailwind.css`. |
| **Alpine.js** | Cargado vía CDN al final de `basebs.html`. |
| **login.html** | 100% Tailwind. El bloque `<style>` de 455 líneas fue reemplazado por utilidades. Solo quedan ~70 líneas de CSS para animaciones SVG (`@keyframes`), pseudo-elementos (`::before`), la grilla de pantalla (`grid-template-columns`) y selectores que Tailwind no puede expresar. |
| **Dropdown de períodos** | Migrado de jQuery dropdown a Alpine.js (`x-data`, `x-show`, `@click.outside`). Conserva la clase `.periodoselector` y el atributo `pid` — el handler jQuery existente sigue disparándose. |
| **CSS del chat de soporte** | Eliminado (confirmado muerto por usuario). Quitados `.chat_window`, `.chat_windowsoporte`, `.chat_windowasinado`, `.messages`, `.bottom_wrapper`, `.chat-box`, `.chat-footer`, `.chat-detail` y su JS (`minimaxventasoporte`, `#inciarconver`, etc.). |
| **Limpieza de estáticos** | 44 archivos CSS/JS sin referencias movidos a `static/_deprecated/`. Ahorro: ~1.48 MB. |
| **font-awesome duplicada** | Eliminada la carga local (`font-awesome.css`). Solo queda el CDN 6.4.0. |
| **Componentes reutilizables** | Partials en `templates/components/`: `btn_primary.html`, `card.html`, `alert_error.html`, `badge.html`. |

---

## ⏳ Pendiente de migrar

| Componente | Dependencia actual | Reemplazo sugerido | Complejidad |
|-----------|-------------------|--------------------|-------------|
| Modal `#nuevopanelbs` (registro de requerimiento) | `bootstrap-modal.js` + `bootstrap-modalmanager.js` | Alpine.js `x-show` + `x-transition` + `@click.outside` | Media |
| Modal `#waitpanel` (`showWaiting` / `hideWaiting`) | `jquery.blockUI.js` | Alpine.js store global: `$store.loading.show(titulo, msg)` | Baja |
| Datepicker | `bootstrap-datepicker.js` | [Flatpickr](https://flatpickr.js.org/) — 2 KB gzip, sin dependencias, soporte i18n | Baja |
| Masked input | `jquery.maskedinput.min.js` | HTML5 `pattern` + input listener nativo (ya hay ejemplos en `validacion6.js`) | Baja |
| Grid `.row-fluid` / `.span*` en home.html | Bootstrap 2 grid | Tailwind `grid` / `flex` al migrar home.html | Alta |
| Modales en home.html (profesionalización, encuesta vacunas, etc.) | Bootstrap 3 `.modal()` | Alpine.js `x-show` + `x-transition` | Alta |
| `smoke.confirm()` (2 llamadas activas en home.html líneas 363 y 379) | `smoke.min.js` | `Swal.fire()` — ya está cargado el CDN sweetalert2@11 | Muy baja |
| Editor WYSIHTML5 (sganuevo) | `bootstrap3-wysihtml5.min.js` (170 KB, solo en sganuevo) | [Trix](https://trix-editor.org/) o [Quill](https://quilljs.com/) | Media |
| Validación de formularios (sganuevo) | `jquery.validationEngine.js` | HTML5 `required`/`pattern` + Tailwind error states | Media |
| `big.min.js` | Cargado en `basebs.html` pero sin llamadas detectadas | Investigar si se usa; si no, eliminar | Pendiente |

---

## Cómo compilar Tailwind

```bash
# Desde AdminIT/

# Desarrollo — recarga automática al guardar templates
npm run tw:watch

# Producción — minificado (correr antes de deploy)
npm run tw:build
```

El archivo compilado `static/css/tailwind.css` se versiona para que Django pueda servirlo sin npm en producción. El `node_modules/` va en `.gitignore`.

---

## Sistema de diseño (tokens @theme)

Definidos en `static/css/input.css`:

| Token | Valor | Uso |
|-------|-------|-----|
| `--color-ink` | `#0A1628` | Texto principal, fondos navbar/footer |
| `--color-ink-2` | `#0F1F38` | Gradiente navbar/footer (más claro) |
| `--color-azul` | `#2D7FF9` | Primario: botones, focus, links |
| `--color-azul-hover` | `#1C6BE3` | Hover de botones azules |
| `--color-cian` | `#22D3EE` | Acentos, reloj, elementos activos |
| `--color-hueso` | `#F6F8FB` | Fondo general, fondo breadcrumbs |
| `--color-niebla` | `#8A97AB` | Texto secundario, bordes, iconos |
| `--color-error` | `#E5484D` | Errores, alertas rojas |
| `--color-ok` | `#30C48D` | Éxito, estados activos verdes |
| `--font-sans` | IBM Plex Sans | Texto, títulos, labels |
| `--font-mono` | IBM Plex Mono | Reloj, breadcrumbs, chips, footer |
| `--radius-card` | `14px` | Cards y botones principales |

---

## Componentes disponibles (`templates/components/`)

```django
{# Botón primario #}
{% include 'components/btn_primary.html' with label="Guardar" icon="fa-save" type="submit" %}

{# Alerta de error #}
{% include 'components/alert_error.html' with mensaje=form.errors %}

{# Badge de estado #}
{% include 'components/badge.html' with texto="Activo" variante="ok" %}
{# variantes: ok | error | azul | niebla #}
```

---

## Archivos clave

| Archivo | Función |
|---------|---------|
| `static/css/input.css` | Fuente Tailwind — editar aquí para agregar tokens o `@utility` |
| `static/css/tailwind.css` | Output compilado — no editar a mano |
| `package.json` | Scripts `tw:watch` y `tw:build` |
| `templates/basebs.html` | Base legacy + Tailwind en coexistencia con Bootstrap |
| `templates/login.html` | 100% Tailwind |
| `templates/components/` | Partials reutilizables |
| `static/_deprecated/` | Archivos eliminados (recuperables si es necesario) |
| `LIMPIEZA.md` | Inventario completo de la auditoría de estáticos muertos |
