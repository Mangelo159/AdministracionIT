/* ============================================================
   CONSOLA TIC — Utilidades compartidas
   Ubicación: static/js/consola-tic.js
   Se cargan automáticamente desde base.html.
   ============================================================ */

(function () {
    'use strict';

    /* ---- Toggle mostrar/ocultar contraseña ----
       Uso: <button class="btn-ojo" data-toggle-password="idDelInput"> */
    const OJO_ABIERTO = '<path d="M10 12a2 2 0 1 0 4 0a2 2 0 0 0 -4 0"/><path d="M21 12c-2.4 4 -5.4 6 -9 6c-3.6 0 -6.6 -2 -9 -6c2.4 -4 5.4 -6 9 -6c3.6 0 6.6 2 9 6"/>';
    const OJO_CERRADO = '<path d="M10.585 10.587a2 2 0 0 0 2.829 2.828"/><path d="M16.681 16.673a8.717 8.717 0 0 1 -4.681 1.327c-3.6 0 -6.6 -2 -9 -6c1.272 -2.12 2.712 -3.678 4.32 -4.674m2.86 -1.146a9.055 9.055 0 0 1 1.82 -.18c3.6 0 6.6 2 9 6c-.666 1.11 -1.379 2.067 -2.138 2.87"/><path d="M3 3l18 18"/>';

    document.querySelectorAll('[data-toggle-password]').forEach(function (btn) {
        const input = document.getElementById(btn.dataset.togglePassword);
        const icono = btn.querySelector('svg');
        if (!input) return;

        btn.setAttribute('aria-pressed', 'false');
        btn.setAttribute('aria-label', 'Mostrar contraseña');

        btn.addEventListener('click', function () {
            const visible = input.type === 'text';
            input.type = visible ? 'password' : 'text';
            if (icono) icono.innerHTML = visible ? OJO_ABIERTO : OJO_CERRADO;
            btn.setAttribute('aria-pressed', String(!visible));
            btn.setAttribute('aria-label', visible ? 'Mostrar contraseña' : 'Ocultar contraseña');
            input.focus({ preventScroll: true });
        });
    });

    /* ---- Aviso de Bloq Mayús ----
       Uso: <input data-aviso-mayus="idDelAviso">
            <p class="aviso-mayus" id="idDelAviso" aria-live="polite">...</p> */
    document.querySelectorAll('[data-aviso-mayus]').forEach(function (input) {
        const aviso = document.getElementById(input.dataset.avisoMayus);
        if (!aviso) return;

        input.addEventListener('keyup', function (e) {
            if (typeof e.getModifierState === 'function') {
                aviso.classList.toggle('visible', e.getModifierState('CapsLock'));
            }
        });
        input.addEventListener('blur', function () {
            aviso.classList.remove('visible');
        });
    });

    /* ---- Reloj del sistema ----
       Uso: <span data-reloj></span> */
    const relojes = document.querySelectorAll('[data-reloj]');
    if (relojes.length) {
        const tick = function () {
            const hora = new Date().toLocaleTimeString('es-EC', { hour12: false });
            relojes.forEach(function (r) { r.textContent = hora; });
        };
        tick();
        setInterval(tick, 1000);
    }

})();

/* ── initCSelect(id, onChange) ─────────────────────────────
   Inicializa un dropdown .c-select. onChange(value) se llama
   cada vez que el usuario selecciona una opción.            */
function initCSelect(id, onChange) {
  var wrap         = document.getElementById(id);
  if (!wrap) return { getValue: function() { return ''; }, reset: function() {} };
  var trigger      = wrap.querySelector('.c-select-trigger');
  var labelEl      = wrap.querySelector('.c-select-label');
  var options      = wrap.querySelectorAll('.c-select-option');
  var value        = '';
  var defaultLabel = labelEl ? labelEl.textContent.trim() : '';

  trigger.addEventListener('click', function(e) {
    e.stopPropagation();
    var isOpen = wrap.classList.contains('open');
    document.querySelectorAll('.c-select').forEach(function(el) { el.classList.remove('open'); });
    if (!isOpen) wrap.classList.add('open');
  });

  options.forEach(function(opt) {
    opt.addEventListener('click', function() {
      value = opt.dataset.value;
      if (labelEl) labelEl.textContent = opt.textContent.trim();
      options.forEach(function(o) { o.classList.toggle('selected', o === opt); });
      wrap.classList.remove('open');
      if (typeof onChange === 'function') onChange(value);
    });
  });

  return {
    getValue: function() { return value; },
    reset: function() {
      value = '';
      if (labelEl) labelEl.textContent = defaultLabel;
      options.forEach(function(o) { o.classList.toggle('selected', o.dataset.value === ''); });
      wrap.classList.remove('open');
    }
  };
}

/* Cierra cualquier .c-select abierto al hacer clic fuera */
document.addEventListener('click', function() {
  document.querySelectorAll('.c-select.open').forEach(function(el) { el.classList.remove('open'); });
});

/* ── initCSelectSearch(id, onChange) ───────────────────────
   Igual que initCSelect pero con input de búsqueda dentro
   del panel para filtrar opciones en tiempo real.           */
function initCSelectSearch(id, onChange) {
  var wrap         = document.getElementById(id);
  if (!wrap) return { getValue: function() { return ''; }, reset: function() {} };
  var trigger      = wrap.querySelector('.c-select-trigger');
  var labelEl      = wrap.querySelector('.c-select-label');
  var options      = wrap.querySelectorAll('.c-select-option');
  var buscar       = wrap.querySelector('.c-select-buscar');
  var buscarWrap   = wrap.querySelector('.c-select-buscar-wrap');
  var value        = '';
  var defaultLabel = labelEl ? labelEl.textContent.trim() : '';

  function filtrarOpciones(q) {
    var texto = q.toLowerCase();
    options.forEach(function(opt) {
      if (opt.dataset.value === '') { opt.style.display = ''; return; }
      opt.style.display = opt.textContent.toLowerCase().includes(texto) ? '' : 'none';
    });
  }

  trigger.addEventListener('click', function(e) {
    e.stopPropagation();
    var isOpen = wrap.classList.contains('open');
    document.querySelectorAll('.c-select').forEach(function(el) { el.classList.remove('open'); });
    if (!isOpen) {
      wrap.classList.add('open');
      if (buscar) { buscar.value = ''; filtrarOpciones(''); buscar.focus(); }
    }
  });

  if (buscarWrap) {
    buscarWrap.addEventListener('click', function(e) { e.stopPropagation(); });
  }
  if (buscar) {
    buscar.addEventListener('input', function() { filtrarOpciones(this.value); });
  }

  options.forEach(function(opt) {
    opt.addEventListener('click', function() {
      value = opt.dataset.value;
      if (labelEl) labelEl.textContent = opt.textContent.trim();
      options.forEach(function(o) { o.classList.toggle('selected', o === opt); });
      wrap.classList.remove('open');
      if (buscar) { buscar.value = ''; filtrarOpciones(''); }
      if (typeof onChange === 'function') onChange(value);
    });
  });

  return {
    getValue: function() { return value; },
    reset: function() {
      value = '';
      if (labelEl) labelEl.textContent = defaultLabel;
      options.forEach(function(o) {
        o.classList.toggle('selected', o.dataset.value === '');
        o.style.display = '';
      });
      if (buscar) { buscar.value = ''; }
      wrap.classList.remove('open');
    }
  };
}

/* ── mantReload(msg, tipo) ─────────────────────────────────
   Persiste un toast en sessionStorage y recarga la página.
   El toast aparece en la página ya recargada.             */
function mantReload(msg, tipo) {
  sessionStorage.setItem('_mant_toast', JSON.stringify({ msg: msg, tipo: tipo || 'exito' }));
  location.reload();
}

/* ── mantToast(msg, tipo) ──────────────────────────────────
   Muestra una notificación flotante temporal.
   tipo: 'exito' (verde) | 'error' (rojo) | 'info' (azul)  */
function mantToast(msg, tipo) {
  var wrap = document.getElementById('mant-toast-wrap');
  if (!wrap) {
    wrap = document.createElement('div');
    wrap.id = 'mant-toast-wrap';
    wrap.className = 'mant-toast-wrap';
    document.body.appendChild(wrap);
  }
  var div = document.createElement('div');
  div.className = 'alerta alerta-' + (tipo || 'exito') + ' mant-toast';
  div.textContent = msg;
  wrap.appendChild(div);
  setTimeout(function() { div.classList.add('mant-toast-salir'); }, 1800);
  setTimeout(function() { if (div.parentNode) div.parentNode.removeChild(div); }, 2150);
}

/* ── mantPost(form, onOk) ──────────────────────────────────
   Envía un form via fetch (AJAX). Si result === 'ok' llama
   a onOk(); si hay error o forbidden muestra un toast.      */
function mantPost(form, onOk) {
  fetch(window.location.href, {
    method: 'POST',
    body: new FormData(form),
    headers: { 'X-Requested-With': 'XMLHttpRequest' }
  })
  .then(function(r) { return r.json(); })
  .then(function(json) {
    if (json.result === 'ok') {
      if (typeof onOk === 'function') onOk();
    } else if (json.result === 'forbidden') {
      mantToast('Sin permisos para esta acción', 'error');
    } else {
      mantToast(json.error || 'Ocurrió un error', 'error');
    }
  })
  .catch(function() { mantToast('Error de conexión', 'error'); });
}

/* ── initPaginador(tbodySelector, navId, porPagina) ────────
   Paginador cliente. Lee data-filtrado="1" en las filas para
   saber cuáles están filtradas; páginas las restantes.      */
function initPaginador(tbodySelector, navId, porPagina) {
  var tbody = document.querySelector(tbodySelector);
  var nav   = document.getElementById(navId);
  var pp    = porPagina || 10;
  var pagina = 1;

  function filasFiltradas() {
    return Array.from(tbody.querySelectorAll('tr:not(.fila-vacia)'))
           .filter(function(r) { return !r.dataset.filtrado; });
  }

  function render() {
    var filas   = filasFiltradas();
    var total   = filas.length;
    var paginas = Math.max(1, Math.ceil(total / pp));
    if (pagina > paginas) pagina = 1;

    var inicio   = (pagina - 1) * pp;
    var enPagina = new Set(filas.slice(inicio, inicio + pp));

    Array.from(tbody.querySelectorAll('tr:not(.fila-vacia)')).forEach(function(r) {
      r.style.display = enPagina.has(r) ? '' : 'none';
    });

    var vacia = tbody.querySelector('.fila-vacia');
    if (vacia) vacia.style.display = total === 0 ? '' : 'none';

    if (!nav) return;
    if (paginas <= 1) { nav.innerHTML = ''; return; }

    var desde = total === 0 ? 0 : inicio + 1;
    var hasta  = Math.min(inicio + pp, total);
    var html   = '';
    var SVG_PREV = '<svg width="11" height="11" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M10 3L5 8l5 5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>';
    var SVG_NEXT = '<svg width="11" height="11" viewBox="0 0 16 16" fill="none" aria-hidden="true" style="margin-left:3px"><path d="M6 3l5 5-5 5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>';

    html += pagina > 1
      ? '<a href="#" class="paginador-btn" data-p="' + (pagina - 1) + '">' + SVG_PREV + ' Anterior</a>'
      : '<span class="paginador-btn inactivo">' + SVG_PREV + ' Anterior</span>';

    /* Números con ventana inteligente */
    if (paginas <= 7) {
      for (var i = 1; i <= paginas; i++) {
        html += i === pagina
          ? '<span class="paginador-num activo">' + i + '</span>'
          : '<a href="#" class="paginador-num" data-p="' + i + '">' + i + '</a>';
      }
    } else {
      var pages = [1, 2, pagina - 1, pagina, pagina + 1, paginas - 1, paginas]
        .filter(function(p) { return p >= 1 && p <= paginas; })
        .filter(function(p, idx, arr) { return arr.indexOf(p) === idx; })
        .sort(function(a, b) { return a - b; });
      var prev = 0;
      pages.forEach(function(p) {
        if (prev && p > prev + 1) html += '<span class="paginador-elipsis">…</span>';
        html += p === pagina
          ? '<span class="paginador-num activo">' + p + '</span>'
          : '<a href="#" class="paginador-num" data-p="' + p + '">' + p + '</a>';
        prev = p;
      });
    }

    html += pagina < paginas
      ? '<a href="#" class="paginador-btn" data-p="' + (pagina + 1) + '">Siguiente ' + SVG_NEXT + '</a>'
      : '<span class="paginador-btn inactivo">Siguiente ' + SVG_NEXT + '</span>';

    html += '<span class="paginador-info">' + desde + '–' + hasta + ' / ' + total + '</span>';

    nav.innerHTML = html;
    nav.querySelectorAll('[data-p]').forEach(function(el) {
      el.addEventListener('click', function(e) {
        e.preventDefault();
        var p = parseInt(this.dataset.p);
        if (p >= 1 && p <= paginas) { pagina = p; render(); }
      });
    });
  }

  render();
  return { reset: function() { pagina = 1; render(); }, render: render };
}

/* Muestra el toast pendiente de mantReload al cargar la página */
(function () {
  var raw = sessionStorage.getItem('_mant_toast');
  if (!raw) return;
  sessionStorage.removeItem('_mant_toast');
  try {
    var t = JSON.parse(raw);
    mantToast(t.msg, t.tipo);
  } catch (e) {}
})();