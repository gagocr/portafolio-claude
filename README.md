# Portafolio — Rubén Gago Chavez

Sitio web de una sola página con el currículo de Rubén Gago Chavez, pensado para
reclutadores: perfil, experiencia, competencias, formación, publicación, proyectos y
contacto. Funciona tal cual en GitHub Pages o abriendo `index.html` en un navegador.

## Estructura

```
index.html                 la página
assets/css/estilo.css      el estilo: azul de la Variante B del currículo, modo claro y oscuro, versión para imprimir
assets/js/sitio.js         la interacción, sin dependencias (sin él, todo el contenido se ve igual)
assets/img/icono.svg       el icono de la pestaña
herramientas/              construir_sitio.py y las fuentes de estilo.css y sitio.js
.nojekyll                  GitHub Pages sirve los archivos tal cual
```

## Qué ofrece al visitante

- Portada con una «ficha de registro» (áreas, trayectoria, idiomas y correo con botón de copiar)
  y una banda con las tres cifras del perfil, que cuentan hasta su valor.
- **Trayectoria en el tiempo**: los once puestos dibujados a escala de 2011 a hoy; tocar una
  fila abre ese puesto. Los periodos dados solo en años se ven rayados.
- **Experiencia** en tarjetas desplegables, con «Abrir todo» y «Cerrar todo».
- **Competencias** con un buscador que resalta los términos (por ejemplo, «SQL»).
- **Formación** en dos pestañas, con el estado de cada estudio (en curso, pausado, concluido).
- Navegación que marca la sección visible, barra de avance, tema claro u oscuro, botón para
  imprimir (sale como currículo limpio) y animaciones que se apagan si el sistema pide menos
  movimiento.

## De dónde sale el contenido

Del **currículo de referencia** del proyecto privado de búsqueda de empleo (Registro
Maestro v3.20): es el mismo texto que recibe un empleador, sin
redactar nada nuevo. Las tres cifras de la portada son frases del perfil, sin redondear.

## Lo que este sitio no lleva, a propósito

- **Ninguna ubicación personal**: ni la residencia, ni el punto de búsqueda ni sus
  coordenadas. Solo «Costa Rica».
- **Tampoco la ubicación de cada puesto**: de la modalidad solo queda la jornada
  («Presencial, tiempo parcial»), sin cantón ni barrio.
- **El teléfono.** El contacto es el correo, LinkedIn y ResearchGate.
- Nada interno del proyecto: condiciones de búsqueda, límites, notas de trabajo,
  auditorías ni contactos internos.

Se comprobó al construirlo con las guardas del proyecto: ninguna forma de las coordenadas
del centro de búsqueda y ningún nombre de contacto interno.

## Publicarlo

- **El repositorio es público**: cualquiera puede leer estos archivos. Por eso no lleva nada
  que no esté ya en el currículo que recibe un empleador, y menos que eso (ver arriba).
- **Para tener la dirección web**: Settings → Pages → Build and deployment → Deploy from a
  branch → `main` y `/ (root)` → Save. A los pocos minutos queda en
  `https://gagocr.github.io/portafolio-claude/`. En un repositorio público, Pages es gratis.
- La página lleva `noindex`: quien tenga el enlace la ve, pero no aparece en buscadores. Para
  que aparezca, se quita la línea `<meta name="robots" …>` de `index.html`.

## Regenerarlo

`herramientas/construir_sitio.py` lee el modelo del currículo que exporta el proyecto
privado (`modelo.json`, que no se sube porque lleva el teléfono y la residencia) y escribe
`index.html`, `assets/css/estilo.css` y `assets/js/sitio.js`:

    python3 herramientas/construir_sitio.py modelo.json .
