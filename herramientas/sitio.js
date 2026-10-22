/* Portafolio — interacción. Sin dependencias. Si este archivo no carga, todo el contenido se ve igual. */
(function () {
  'use strict';
  var raiz = document.documentElement;
  var quieto = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  function $$(s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); }

  /* aviso breve */
  var aviso = document.querySelector('.aviso'), reloj;
  function avisar(t) {
    if (!aviso) return;
    aviso.textContent = t; aviso.hidden = false;
    clearTimeout(reloj); reloj = setTimeout(function () { aviso.hidden = true; }, 2200);
  }

  /* tema claro u oscuro: el del sistema, salvo que el visitante elija */
  var botonTema = document.querySelector('.tema');
  if (botonTema) botonTema.addEventListener('click', function () {
    var oscuro = raiz.dataset.theme ? raiz.dataset.theme === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches;
    raiz.dataset.theme = oscuro ? 'light' : 'dark';
    try { localStorage.setItem('tema', raiz.dataset.theme); } catch (_) {}
  });

  /* barra de progreso, sombra de la barra y botón de volver arriba */
  var barra = document.querySelector('.barra'), arriba = document.querySelector('.arriba'), pendiente = false;
  function alDesplazar() {
    pendiente = false;
    var y = window.scrollY, alto = document.documentElement.scrollHeight - window.innerHeight;
    raiz.style.setProperty('--avance', alto > 0 ? Math.min(1, y / alto) : 0);
    if (barra) barra.classList.toggle('con-sombra', y > 10);
    if (arriba) arriba.classList.toggle('ver', y > window.innerHeight * 0.9);
  }
  window.addEventListener('scroll', function () { if (!pendiente) { pendiente = true; requestAnimationFrame(alDesplazar); } }, { passive: true });
  alDesplazar();

  /* sección activa en la navegación */
  var enlaces = $$('.barra nav a');
  var secciones = enlaces.map(function (a) { return document.getElementById(a.dataset.seccion); }).filter(Boolean);
  if ('IntersectionObserver' in window && secciones.length) {
    var visibles = {};
    var obsSec = new IntersectionObserver(function (ents) {
      ents.forEach(function (en) { visibles[en.target.id] = en.isIntersecting; });
      var actual = null;
      secciones.forEach(function (s) { if (visibles[s.id] && !actual) actual = s.id; });
      enlaces.forEach(function (a) {
        var si = a.dataset.seccion === actual;
        a.classList.toggle('activo', si);
        if (si) {
          a.setAttribute('aria-current', 'true');
          var ul = a.closest('ul');
          if (ul && ul.scrollWidth > ul.clientWidth) ul.scrollTo({ left: a.offsetLeft - ul.clientWidth / 2 + a.offsetWidth / 2, behavior: quieto ? 'auto' : 'smooth' });
        } else a.removeAttribute('aria-current');
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    secciones.forEach(function (s) { obsSec.observe(s); });
  }

  /* aparición al desplazarse */
  var revelables = $$('.revela');
  if ('IntersectionObserver' in window && !quieto) {
    var obsRev = new IntersectionObserver(function (ents) {
      ents.forEach(function (en) {
        if (!en.isIntersecting) return;
        var hermanos = $$('.revela:not(.visto)', en.target.parentNode);
        var i = Math.max(0, hermanos.indexOf(en.target));
        en.target.style.transitionDelay = Math.min(i, 6) * 60 + 'ms';
        en.target.classList.add('visto');
        obsRev.unobserve(en.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    revelables.forEach(function (el) { obsRev.observe(el); });
  } else revelables.forEach(function (el) { el.classList.add('visto'); });

  /* cifras que cuentan hasta su valor (el texto final es el del currículo) */
  $$('[data-cuenta]').forEach(function (el) {
    var meta = parseInt(el.dataset.cuenta, 10), final = el.textContent;
    if (quieto || !('IntersectionObserver' in window)) return;
    var hecho = false;
    var obs = new IntersectionObserver(function (ents) {
      if (hecho || !ents[0].isIntersecting) return;
      hecho = true; obs.disconnect();
      var t0 = performance.now(), dur = 1400;
      (function paso(t) {
        var k = Math.min(1, (t - t0) / dur), v = Math.round(meta * (1 - Math.pow(1 - k, 3)));
        el.textContent = k < 1 ? v.toLocaleString('es-CR').replace(/\s/g, '.') : final;
        if (k < 1) requestAnimationFrame(paso);
      })(t0);
    }, { threshold: 0.6 });
    obs.observe(el);
  });

  /* experiencia: abrir o cerrar todo; la línea de tiempo lleva al puesto */
  var puestos = $$('details.puesto');
  $$('[data-todos]').forEach(function (b) {
    b.addEventListener('click', function () { var abrir = b.dataset.todos === 'abrir'; puestos.forEach(function (p) { p.open = abrir; }); });
  });
  $$('.fila-t').forEach(function (f) {
    var destino = document.getElementById(f.dataset.abre);
    f.addEventListener('click', function (ev) {
      if (!destino) return;
      ev.preventDefault();
      destino.open = true;
      destino.scrollIntoView({ behavior: quieto ? 'auto' : 'smooth', block: 'start' });
      destino.classList.remove('destello'); void destino.offsetWidth; destino.classList.add('destello');
    });
    f.addEventListener('mouseenter', function () { f.classList.add('resalta'); });
    f.addEventListener('mouseleave', function () { f.classList.remove('resalta'); });
  });

  /* competencias: búsqueda */
  var entrada = document.querySelector('[data-buscar]'), resultado = document.querySelector('[data-resultado]'),
      vacio = document.querySelector('[data-vacio]'), tarjetas = $$('[data-comp]');
  function normal(t) { return t.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, ''); }
  if (entrada) entrada.addEventListener('input', function () {
    var q = normal(entrada.value.trim()), total = 0;
    tarjetas.forEach(function (c) {
      var n = 0, enTitulo = q && normal(c.querySelector('h3').textContent).indexOf(q) >= 0;
      $$('.terminos li', c).forEach(function (li) {
        var si = !!q && normal(li.textContent).indexOf(q) >= 0;
        li.classList.toggle('coincide', si); if (si) n++;
      });
      total += n;
      c.classList.toggle('atenua', !!q && !n && !enTitulo);
    });
    var algo = !q || tarjetas.some(function (c) { return !c.classList.contains('atenua'); });
    if (vacio) vacio.hidden = algo;
    if (resultado) resultado.textContent = q ? (total === 1 ? '1 coincidencia' : total + ' coincidencias') : '';
  });

  /* formación: pestañas (sin JS se ven los dos paneles) */
  var tabs = $$('.pestanas [role="tab"]');
  function elegir(t, foco) {
    tabs.forEach(function (x) {
      var si = x === t;
      x.setAttribute('aria-selected', si); x.tabIndex = si ? 0 : -1;
      var p = document.getElementById(x.getAttribute('aria-controls'));
      if (p) p.hidden = !si;
    });
    if (foco) t.focus();
  }
  tabs.forEach(function (t, i) {
    t.addEventListener('click', function () { elegir(t); });
    t.addEventListener('keydown', function (ev) {
      var d = ev.key === 'ArrowRight' ? 1 : ev.key === 'ArrowLeft' ? -1 : 0;
      if (d) { ev.preventDefault(); elegir(tabs[(i + d + tabs.length) % tabs.length], true); }
    });
  });
  if (tabs.length) elegir(tabs[0]);

  /* copiar el correo */
  $$('[data-copiar]').forEach(function (b) {
    var texto = b.textContent;
    b.addEventListener('click', function () {
      var valor = b.dataset.copiar;
      function listo() {
        b.classList.add('listo'); b.textContent = 'Copiado'; avisar('Correo copiado: ' + valor);
        setTimeout(function () { b.classList.remove('listo'); b.textContent = texto; }, 1800);
      }
      function aMano() {
        var s = b.parentNode.querySelector('.copiable, a');
        if (s && window.getSelection) { var r = document.createRange(); r.selectNodeContents(s); var sel = getSelection(); sel.removeAllRanges(); sel.addRange(r); }
        avisar('Seleccionado: ' + valor + ' — cópielo con Ctrl+C');
      }
      try { navigator.clipboard.writeText(valor).then(listo, aMano); } catch (_) { aMano(); }
    });
  });

  /* imprimir: todo abierto y visible */
  $$('[data-imprimir]').forEach(function (b) { b.addEventListener('click', function () { window.print(); }); });
  var abiertos = [];
  window.addEventListener('beforeprint', function () {
    abiertos = puestos.map(function (p) { return p.open; });
    puestos.forEach(function (p) { p.open = true; });
    revelables.forEach(function (el) { el.classList.add('visto'); });
  });
  window.addEventListener('afterprint', function () { puestos.forEach(function (p, i) { p.open = abiertos[i]; }); });
})();
