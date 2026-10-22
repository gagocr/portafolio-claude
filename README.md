# Portafolio — Rubén Gago Chavez

Sitio web de una sola página con el currículo de Rubén Gago Chavez, pensado para
reclutadores: perfil, experiencia, competencias, formación, publicación, proyectos y
contacto. Funciona tal cual en GitHub Pages o abriendo `index.html` en un navegador.

## Estructura

```
index.html                 la página
assets/css/estilo.css      el estilo: azul de la Variante B del currículo, modo claro y oscuro, versión para imprimir
assets/img/icono.svg       el icono de la pestaña
herramientas/construir_sitio.py   cómo se genera index.html
.nojekyll                  GitHub Pages sirve los archivos tal cual
```

## De dónde sale el contenido

Del **currículo de referencia** del proyecto de búsqueda de empleo (repositorio privado
`busqueda-empleo`, Registro Maestro v3.20): es el mismo texto que recibe un empleador, sin
redactar nada nuevo. Las tres cifras de la portada son frases del perfil, sin redondear.

## Lo que este sitio no lleva, a propósito

- **Ninguna ubicación personal**: ni la residencia, ni el punto de búsqueda ni sus
  coordenadas. Solo «Costa Rica».
- **El teléfono.** El contacto es el correo, LinkedIn y ResearchGate.
- Nada interno del proyecto: condiciones de búsqueda, límites, notas de trabajo,
  auditorías ni contactos internos.

Se comprobó al construirlo con las guardas del proyecto: ninguna forma de las coordenadas
del centro de búsqueda y ningún nombre de contacto interno.

## Publicarlo

- **Repositorio privado**: GitHub Pages en un repositorio privado exige un plan de pago
  (GitHub Pro o superior), y aun así el sitio publicado es público. Sin Pages, solo lo ven
  las personas con acceso al repositorio.
- **Para que lo vean reclutadores**: Settings → Pages → Deploy from a branch → `main` / raíz.
- La página lleva `noindex`: no aparece en buscadores. Para que aparezca, se quita la
  línea `<meta name="robots" …>` de `index.html`.

## Regenerarlo

`herramientas/construir_sitio.py` lee el modelo del currículo que exporta el proyecto
privado (`modelo.json`, que no se sube porque lleva el teléfono y la residencia) y escribe
`index.html`. El estilo se copia aparte.
