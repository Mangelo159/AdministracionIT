# LIMPIEZA.md — Auditoría de CSS y JS muertos

Generado: 2026-06-10  
Método: grep sobre todos los `.html`, `.js` y `.py` del proyecto  
Base de templates activos: `basebs.html`, `base.html`, `login.html`, `home.html`, `error/404.html`, `error/500.html`

> **INSTRUCCIONES**: Revisa las tres listas. Para aprobar la limpieza dime qué sección ejecutar.
> Nada se borra permanentemente: los archivos van a `static/_deprecated/`.

---

## ✅ SEGURO ELIMINAR

Cero referencias en ningún `.html`, `.js` ni `.py` de `/templates` ni `/adm`.

### CSS (ahorro estimado: ~660 KB)

| Archivo | Tamaño | Evidencia |
|---------|--------|-----------|
| `static/css/bootstrap.css` | 121 KB | `basebs.html` carga `bootstrap.min.css`, nunca la versión no-minificada |
| `static/css/bootstrap-responsive.min.css` | 16 KB | `basebs.html` carga `bootstrap-responsive.css` (sin `.min`); la `.min` no es usada |
| `static/css/bootstrap-theme.min.css` | 13 KB | Sin referencias en ningún template |
| `static/css/colors.min.css` | 427 KB | Sin referencias. Archivo excepcionalmente grande y sin uso |
| `static/css/styles.css` | 5.6 KB | `base.html` usa `consola-tic.css`; nadie carga `styles.css` |
| `static/css/identidad.css` | 0.8 KB | Sin referencias |
| `static/css/theme.css` | 0.8 KB | Sin referencias |
| `static/css/modules.css` | 1.6 KB | Sin referencias |
| `static/css/font-awesome.min.css` | 26 KB | La `.css` local (no-min) es la que se carga en `basebs.html`; la `.min` no se usa (y la local también será eliminada — ver acción puntual más abajo) |
| `static/css/font-awesome-ie7.css` | 23 KB | Polyfill IE7; sin referencias |
| `static/css/sweet-alert.css` | 22 KB | `base.html` carga `sweet-alert.min.js` pero no este CSS; ningún template lo referencia |
| `static/css/login.css` | 1.9 KB | `login.html` usa estilos inline; nadie carga este archivo |
| `static/css/date_input.css` | 2.4 KB | Sin referencias en templates |
| `static/css/epiclock.retro.css` | 3.6 KB | Sin referencias en templates |
| `static/css/flipclock.css` | 9.5 KB | Sin referencias en templates |
| `static/css/jquery.flexbox.css` | 1.8 KB | Sin referencias en templates |
| `static/css/jquery.timeentry.css` | 0.2 KB | Sin referencias en templates |
| `static/css/modern-ticker.css` | 1.9 KB | Sin referencias en templates |
| `static/css/validationEngine.jquery.css` | 2.4 KB | Sin referencias en templates |

### JS (ahorro estimado: ~820 KB)

| Archivo | Tamaño | Evidencia |
|---------|--------|-----------|
| `static/js/bs/bootstrap.js` | 57 KB | `basebs.html` carga `bs/bootstrap.min.js`; la versión no-minificada no se usa |
| `static/js/json2.js` | 17 KB | Polyfill IE8; sin referencias en templates |
| `static/js/shadowbox.js` | 64 KB | Sin referencias en templates |
| `static/js/jquery.gallery.js` | 27 KB | Sin referencias en templates |
| `static/js/jquery.floats.js` | 1.7 KB | Sin referencias en templates |
| `static/js/nicEdit-latest.js` | 37 KB | Sin referencias en templates (solo aparece en el archivo mismo) |
| `static/js/handlebars.runtime.min.js` | 6.7 KB | Sin referencias en templates |
| `static/js/jquery.epiclock.min.js` | 12.8 KB | Sin referencias en templates |
| `static/js/epiclock.retro.min.js` | 1.1 KB | Sin referencias en templates |
| `static/js/flipclock.js` | 53 KB | Sin referencias en templates |
| `static/js/flipclock.min.js` | 20.6 KB | Sin referencias en templates |
| `static/js/jquery.flexbox.js` | 36.7 KB | Sin referencias en templates |
| `static/js/jquery.flexbox.min.js` | 13.2 KB | Sin referencias en templates |
| `static/js/jquery.timeentry.js` | 37 KB | Sin referencias en templates |
| `static/js/jquery.timeentry.min.js` | 16.7 KB | Sin referencias en templates |
| `static/js/jquery.editinplace.js` | 24.1 KB | Sin referencias en templates |
| `static/js/jquery.modern-ticker.min.js` | 8.1 KB | Sin referencias en templates |
| `static/js/jquery.validationEngine.js` | 65 KB | Sin referencias en templates |
| `static/js/jquery.validationEngine-es.js` | 7.5 KB | Sin referencias en templates |
| `static/js/jquery.dateformat.min.js` | 4.1 KB | Solo usada internamente por `jquery.epiclock.min.js`, que también está muerto |
| `static/js/bootstrap3-wysihtml5.min.js` | 25.1 KB | Referenciado solo en `static/vendors/scripts/script.js` (aplicación sganuevo separada), no en ningún template de `adm` |
| `static/js/wysihtml5x-toolbar.min.js` | 168 KB | Igual que el anterior; solo en sganuevo |
| `static/js/jquery.date_input.js` | 14.9 KB | Sin referencias en templates |

### Acción puntual (no mover a _deprecated, editar en basebs.html):

```html
<!-- ELIMINAR esta línea en basebs.html línea 16: -->
<link href='/static/css/font-awesome.css' rel='stylesheet'/>
<!-- Ya existe el CDN de FA 6.4.0 en línea 21 — es redundante cargar la versión local -->
```

### Código inline muerto en basebs.html (confirmado por el usuario):

El bloque completo del chat de soporte (~80 líneas) puede eliminarse:
- Handler `#inciarconver`, `#idregistrochat`, `#btnregistrochat`
- Función `minimaxventasoporte()`
- Listener `.chat_windowsoporte`
- Reglas CSS `.chat_window`, `.chat_windowsoporte`, `.chat_windowasinado` en el `<style>` inline

---

## ⚠️ PROBABLEMENTE MUERTO — Requiero tu confirmación

| Archivo / Código | Tamaño | Duda |
|-----------------|--------|------|
| `static/js/big.min.js` | 5.4 KB | Cargado en `basebs.html` línea 38, pero ningún template llama `new Big()` ni usa su API. Es `big.js v1.0.1` (aritmética decimal arbitraria). ¿Se usa desde algún view o JS externo al proyecto? Si no, es SEGURO ELIMINAR. |
| `static/css/sweet-alert.css` + versión local `static/js/sweet-alert.min.js` | — | `base.html` carga `sweet-alert.min.js` local Y también el CDN `sweetalert2@11`. ¿Ambas son necesarias? La versión local (SweetAlert 1.x) es diferente a SweetAlert2. Posible duplicado de API. |

---

## 🔒 EN USO — No tocar

| Archivo | Usado por |
|---------|-----------|
| `static/css/bootstrap.min.css` | `basebs.html` línea 14 |
| `static/css/bootstrap-responsive.css` | `basebs.html` línea 15 (versión NO-min) |
| `static/css/bootstrap-modal.css` | `basebs.html` línea 20 |
| `static/css/smoke.css` + `static/js/smoke.min.js` | `basebs.html` + `home.html` — `smoke.confirm()` activo en líneas 363 y 379 |
| `static/css/datepicker.css` | `basebs.html` línea 19 |
| `static/css/stylesbs.css` | `basebs.html` línea 18 (overrides Bootstrap 2) |
| `static/css/consola-tic.css` | `base.html` |
| `static/js/jquery.min.js` | `basebs.html` + `base.html` |
| `static/js/bs/bootstrap.min.js` | `basebs.html` + `base.html` |
| `static/js/jquery.blockUI.js` | `basebs.html` + `base.html` — usado por `showWaiting()` / `hideWaiting()` |
| `static/js/jquery.maskedinput.min.js` | `basebs.html` + `base.html` — usado en `static/sganuevo/src/scripts/validacion6.js` y `jquery.steps*.js` |
| `static/js/bootstrap-datepicker.js` | `basebs.html` + `base.html` |
| `static/js/bootstrap-modal.js` + `bootstrap-modalmanager.js` | `basebs.html` — modales activos en `home.html` |
| `static/js/sweet-alert.min.js` | `base.html` (SweetAlert 1.x) |
| `static/js/consola-tic.js` | `base.html` |
| `static/js/notificacionpanel.js` | (verificar en `base.html`) |
| `static/js/highcharts.js` + `exporting.js` | `home.html` (verificar) |
| `static/js/firebase*.js` + `conexion_firebase*.js` | Chat tiempo real |
| `static/js/imprmir.js` | (verificar) |
| `static/css/font-awesome.css` local | Cargada en `basebs.html` — ELIMINAR y dejar solo CDN 6.4.0 |
| CDN Font Awesome 6.4.0 | `basebs.html` línea 21 — mantener |
| CDN sweetalert2@11 | `basebs.html` línea 45 — mantener |
| CDN Google Fonts IBM Plex | `basebs.html` líneas 26-28 — mantener |

---

## Resumen de ahorro estimado

| Categoría | Ahorro |
|-----------|--------|
| CSS (SEGURO ELIMINAR) | ~660 KB |
| JS (SEGURO ELIMINAR) | ~820 KB |
| **Total potencial** | **~1.48 MB** |

Sin contar los 427 KB de `colors.min.css` que de por sí casi duplican el tamaño de Bootstrap.

---

## Cómo aprobar la ejecución

Dime cuál(es) de estas acciones ejecuto:
1. **Mover [SEGURO ELIMINAR] a `static/_deprecated/`** — archivos CSS y JS sin referencias
2. **Eliminar font-awesome.css local en basebs.html** — quitar línea 16
3. **Eliminar bloque JS del chat en basebs.html** — ~80 líneas confirmadas muertas
4. **Todo lo anterior de una vez** — commit único de limpieza
