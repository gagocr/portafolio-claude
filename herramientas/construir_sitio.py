# -*- coding: utf-8 -*-
"""Construye el sitio del portafolio desde el modelo del currículo de referencia (modelo.json).

Solo lleva lo que ya va en el currículo que recibe un empleador, menos: el teléfono, la
residencia y toda ubicación (ni la personal ni la de los lugares de trabajo). Nunca lee la
matriz entera: lee el modelo del CV. No inventa nada: cada texto sale del modelo; lo único
calculado es la línea de tiempo, dibujada a escala desde los periodos de cada puesto.

    python3 construir_sitio.py MODELO.json SALIDA/ [--vista-previa ARCHIVO.html]

--vista-previa escribe además una sola página con el CSS y el JS dentro, sin encabezado de
documento, para publicarla como vista previa privada en claude.ai.
"""
import datetime
import html
import json
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
M = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
OUT = Path(sys.argv[2])
PREVIA = Path(sys.argv[sys.argv.index("--vista-previa") + 1]) if "--vista-previa" in sys.argv else None
d = M["doc"]
e = html.escape

cab = d["cabecera"]
nombre = cab["nombre"]
areas = [x.strip() for x in cab["titular"].split("·")]
correo = "gagocr00@gmail.com"
assert correo in cab["linea1"]
enlaces = [x.strip() for x in cab["linea2"].split("·")]
linkedin = next(x for x in enlaces if "linkedin" in x)
researchgate = next(x for x in enlaces if "researchgate" in x)
iniciales = "".join(w[0] for w in nombre.split()[:2])
co = d["competencias"]


def lista(xs, clase=""):
    return "<ul%s>%s</ul>" % (' class="%s"' % clase if clase else "", "".join("<li>%s</li>" % e(x) for x in xs))


def sin_lugar(mod):
    """La modalidad sin el lugar: lo que sigue al primer « · » es la ubicación del puesto."""
    return mod.split(" · ")[0].strip()


# ---------- línea de tiempo: los periodos, a escala, en meses
MESES = dict(ene=1, feb=2, mar=3, abr=4, may=5, jun=6, jul=7, ago=8, sep=9, set=9, oct=10, nov=11, dic=12)
hoy = datetime.date.today()
FIN = hoy.year * 12 + hoy.month          # el mes en curso, incluido
INI = 2011 * 12 + 1


def tramos(per):
    """[(desde, hasta, aproximado)] en meses absolutos, hasta incluido."""
    m = re.fullmatch(r"(\w{3}) (\d{4}) – (?:(\w{3}) (\d{4})|actualidad)", per)
    if m:
        a = int(m[2]) * 12 + MESES[m[1]]
        b = FIN if m[3] is None else int(m[4]) * 12 + MESES[m[3]]
        return [(a, b, False)]
    m = re.fullmatch(r"(\d{4}) – (\d{4})", per)
    if m:
        return [(int(m[1]) * 12 + 1, int(m[2]) * 12 + 12, True)]
    m = re.fullmatch(r"nov–dic de cada año, (\d{4}) – (\d{4})", per)
    if m:
        return [(y * 12 + 11, y * 12 + 12, False) for y in range(int(m[1]), int(m[2]) + 1)]
    raise SystemExit("periodo sin leer: %r" % per)


def pct(mes):
    return 100.0 * (mes - INI) / (FIN + 1 - INI)


puestos = d["experiencia"]["puestos"]
filas = []
for i, p in enumerate(puestos):
    barras = []
    for a, b, aprox in tramos(p["per"]):
        barras.append('<span class="barra-t%s%s" style="left:%.3f%%;width:%.3f%%"></span>' % (
            " aprox" if aprox else "", " actual" if b == FIN and "actualidad" in p["per"] else "", pct(a), pct(b + 1) - pct(a)))
    filas.append("""
        <a class="fila-t" href="#p-%d" data-abre="p-%d" title="%s · %s">
          <span class="fila-nom">%s</span>
          <span class="fila-pista">%s</span>
          <span class="fila-per">%s</span>
        </a>""" % (i, i, e(p["nom"]), e(p["per"]), e(p["nom"]), "".join(barras), e(p["per"])))
anios = list(range(2011, hoy.year + 1))
regla = "".join('<span class="anio%s" style="left:%.3f%%">%d</span>' % (" par" if (y - 2011) % 2 else "", pct(y * 12 + 1), y)
                for y in anios)

# ---------- experiencia
exp = []
for i, p in enumerate(puestos):
    actual = "actualidad" in p["per"]
    vin = p.get("vinetas", [])
    exp.append("""
      <details class="puesto revela" id="p-%d"%s>
        <summary>
          <span class="puesto-punto%s" aria-hidden="true"></span>
          <span class="puesto-cab">
            <span class="puesto-per">%s%s</span>
            <span class="puesto-cargo">%s</span>
            <span class="puesto-org">%s</span>
            <span class="puesto-meta">%s%s</span>
          </span>
          <span class="puesto-flecha" aria-hidden="true"></span>
        </summary>
        %s
      </details>""" % (i, " open" if i < 2 else "", " actual" if actual else "", e(p["per"]),
                       ' <em class="sello">Actual</em>' if actual else "", e(p["cargo"]), e(p["nom"]),
                       e(sin_lugar(p["mod"])) if p.get("mod") else "",
                       ' <span class="cuenta">%d %s</span>' % (len(vin), "función" if len(vin) == 1 else "funciones") if vin else "",
                       lista(vin, "vinetas")))

# ---------- competencias
comp = []
for r in co["rubros"]:
    comp.append("""
      <article class="comp revela" data-comp>
        <h3>%s <span class="comp-n">%d</span></h3>
        %s
      </article>""" % (e(r["rotulo"]), len(r["terminos"]), lista(r["terminos"], "terminos")))
notas = "".join('<div class="nota"><span class="nota-rot">%s</span><p>%s</p></div>' % (e(co[k]["rotulo"]), e(co[k]["seg"]))
                for k in ("idiomas", "aprendizaje") if co.get(k))
n_terminos = sum(len(r["terminos"]) for r in co["rubros"])

# ---------- formación
form = []
for f in d["formacion"]["items"]:
    partes = [x.strip() for x in f["cv_fecha"].split(" · ")]
    estado = partes[-1] if len(partes) > 1 else ""
    clase = {"En curso": "curso", "Pausado": "pausa"}.get(estado, "hecho")
    form.append("""
        <li class="estudio revela">
          <span class="estado %s">%s</span>
          <p class="f-titulo">%s</p>
          <p class="f-inst">%s</p>
          <p class="f-fecha">%s</p>
        </li>""" % (clase, e(estado), e(f["cv"]), e(f["inst"]), e(partes[0])))

compl = "".join("""
        <li class="curso revela"><span class="c-fecha">%s</span><span class="c-act">%s</span><span class="c-inst">%s</span></li>"""
                % (e(c["fecha"]), e(c["act"]), e(c["inst"])) for c in d["complementaria"]["items"])
creds = "".join('<li class="credencial revela"><span class="c-fecha">Credencial</span><span class="c-act">%s</span></li>' % e(c)
                for c in d["complementaria"].get("credenciales", []))

pubs = "".join("""
      <article class="pub revela">
        <p class="pub-anio">%s</p>
        <div class="pub-cuerpo"><h3>%s</h3><p>%s</p></div>
      </article>""" % (e(p["fecha"]), e(p["titulo"]), e(p["detalle"])) for p in d["publicaciones"]["items"])

proys = "".join("""
      <article class="obra revela">
        <p class="obra-tipo">%s</p>
        <h3>%s</h3>
        <p class="obra-per">%s</p>
        %s
      </article>""" % (e(d["proyectos"]["titulo"][:-1]), e(p["titulo"]), e(p["periodo"]), lista(p["segs"], "vinetas"))
                for p in d["proyectos"]["items"])
otros = "".join("""
      <article class="obra revela">
        <p class="obra-tipo">%s</p>
        <h3>%s</h3>
        <p class="obra-per">%s</p>
        %s
      </article>""" % (e(p["cargo"]), e(p["nom"]), e(p["per"]), lista(p.get("vinetas", []), "vinetas"))
                for p in d["otros"]["puestos"])

# ---------- cifras: con las palabras del perfil; no se resumen ni se redondean
texto_perfil = " ".join(d["perfil"]["segs"])
assert "comenzó en 2011" in texto_perfil and "más de 6.000 ítems de colecciones patrimoniales en DSpace" in texto_perfil \
    and "más de 500 artículos académicos y científicos marcados en XML-JATS para su indexación en SciELO" in texto_perfil
cifras = [("Desde", "2011", "", "trayectoria laboral", ""),
          ("Más de", "6.000", "6000", "ítems de colecciones patrimoniales descritos en DSpace", ""),
          ("Más de", "500", "500", "artículos marcados en XML-JATS validados para su indexación en SciELO", "")]
cif = "".join("""
          <li class="cifra revela"><span class="cifra-pre">%s</span><span class="cifra-num"%s>%s</span><span class="cifra-txt">%s</span></li>"""
              % (e(a), (' data-cuenta="%s"' % c) if c else "", e(b), e(t)) for a, b, c, t, _ in cifras)

chips = "".join('<li>%s</li>' % e(a) for a in areas)
perfil = "".join('<p class="revela">%s</p>' % e(p) for p in d["perfil"]["segs"][1:])
idioma = co["idiomas"]["seg"]

SECC = [("perfil", "Perfil"), ("trayectoria", "Trayectoria"), ("experiencia", "Experiencia"), ("competencias", "Competencias"),
        ("formacion", "Formación"), ("obra", "Publicaciones y proyectos"), ("contacto", "Contacto")]
nav = "".join('<li><a href="#%s" data-seccion="%s">%s</a></li>' % (a, a, e(b)) for a, b in SECC)

cuerpo = """<a class="saltar" href="#perfil">Ir al contenido</a>
<div class="progreso" aria-hidden="true"><span></span></div>
<header class="barra">
  <div class="contenedor barra-in">
    <a class="marca" href="#inicio" aria-label="Inicio"><span>{iniciales}</span></a>
    <nav aria-label="Secciones"><ul>{nav}</ul></nav>
    <button class="tema" type="button" aria-label="Cambiar entre tema claro y oscuro" title="Tema claro u oscuro">
      <svg viewBox="0 0 24 24" aria-hidden="true"><path class="sol" d="M12 4V2m0 20v-2m8-8h2M2 12h2m13.66-5.66 1.41-1.41M4.93 19.07l1.41-1.41m0-11.32L4.93 4.93m14.14 14.14-1.41-1.41M12 7a5 5 0 1 0 0 10 5 5 0 0 0 0-10Z"/><path class="luna" d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5Z"/></svg>
    </button>
  </div>
</header>

<main id="inicio">
  <section class="portada">
    <div class="trama" aria-hidden="true"></div>
    <div class="contenedor portada-in">
      <div class="portada-txt">
        <p class="sobre"><span class="pulso" aria-hidden="true"></span>Currículo · Costa Rica</p>
        <h1>{nombre}</h1>
        <ul class="areas">{chips}</ul>
        <p class="entrada">{entrada}</p>
        <div class="acciones">
          <a class="boton primario" href="mailto:{correo}">
            <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 6h18v12H3z"/><path d="m3 7 9 6 9-6"/></svg>Escribirme</a>
          <a class="boton" href="https://{linkedin}" rel="noopener" target="_blank">LinkedIn</a>
          <a class="boton" href="https://{researchgate}" rel="noopener" target="_blank">ResearchGate</a>
          <button class="boton fantasma solo-sitio" type="button" data-imprimir>
            <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 9V3h10v6"/><path d="M7 17H4v-7h16v7h-3"/><path d="M7 14h10v7H7z"/></svg>Imprimir</button>
        </div>
      </div>

      <aside class="ficha" aria-label="Ficha de registro">
        <div class="ficha-cab">
          <span class="monograma" aria-hidden="true">{iniciales}</span>
          <div>
            <p class="ficha-rot">Ficha de registro</p>
            <p class="ficha-nom">{nombre}</p>
          </div>
        </div>
        <dl class="ficha-campos">
          <div><dt>Materias</dt><dd>{n_areas} áreas · {n_terminos} competencias</dd></div>
          <div><dt>Trayectoria</dt><dd>Desde 2011 · {n_puestos} puestos</dd></div>
          <div><dt>Idiomas</dt><dd>{idioma}</dd></div>
          <div><dt>Correo</dt><dd><span class="copiable">{correo}</span>
            <button class="copiar" type="button" data-copiar="{correo}">Copiar</button></dd></div>
        </dl>
        <p class="ficha-pie">Registro Maestro v{registro}</p>
      </aside>
    </div>
  </section>

  <section class="banda" aria-label="Cifras">
    <div class="contenedor"><ul class="cifras">{cif}
    </ul></div>
  </section>

  <section id="perfil" class="seccion">
    <div class="contenedor dos-col">
      <header class="sec-cab revela">
        <p class="sec-num">01</p>
        <h2>{t_perfil}</h2>
      </header>
      <div class="prosa">{perfil}</div>
    </div>
  </section>

  <section id="trayectoria" class="seccion alterna">
    <div class="contenedor">
      <header class="sec-cab revela">
        <p class="sec-num">02</p>
        <h2>Trayectoria en el tiempo</h2>
        <p class="sec-desc">Cada puesto, a escala, de 2011 a hoy. Los tramos rayados son periodos dados solo en años.
          Toque una fila para ver el puesto.</p>
      </header>
      <div class="cronologia-marco revela">
        <div class="cronologia" style="--anio:{anio}%">
          <div class="regla"><span class="fila-nom"></span><span class="regla-pista">{regla}</span><span class="fila-per"></span></div>
          {filas}
        </div>
      </div>
      <ul class="leyenda">
        <li><span class="mues"></span>Periodo con meses</li>
        <li><span class="mues aprox"></span>Periodo dado en años</li>
        <li><span class="mues actual"></span>Puesto actual</li>
      </ul>
    </div>
  </section>

  <section id="experiencia" class="seccion">
    <div class="contenedor">
      <header class="sec-cab revela">
        <p class="sec-num">03</p>
        <h2>{t_exp}</h2>
        <div class="sec-herr">
          <button type="button" class="mini" data-todos="abrir">Abrir todo</button>
          <button type="button" class="mini" data-todos="cerrar">Cerrar todo</button>
        </div>
      </header>
      <div class="linea">{exp}
      </div>
    </div>
  </section>

  <section id="competencias" class="seccion alterna">
    <div class="contenedor">
      <header class="sec-cab revela">
        <p class="sec-num">04</p>
        <h2>{t_comp}</h2>
        <label class="buscador">
          <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="6"/><path d="m20 20-4.5-4.5"/></svg>
          <input type="search" placeholder="Buscar: SQL, DSpace, cobranza…" aria-label="Buscar una competencia" data-buscar>
          <span class="buscador-n" aria-live="polite" data-resultado></span>
        </label>
      </header>
      <div class="rejilla-comp">{comp}
      </div>
      <p class="sin-resultado" hidden data-vacio>Ninguna competencia coincide con la búsqueda.</p>
      <div class="notas">{notas}</div>
    </div>
  </section>

  <section id="formacion" class="seccion">
    <div class="contenedor">
      <header class="sec-cab revela">
        <p class="sec-num">05</p>
        <h2>Formación</h2>
      </header>
      <div class="pestanas" role="tablist" aria-label="Formación">
        <button role="tab" type="button" id="tab-est" aria-controls="pan-est" aria-selected="true">{t_form}</button>
        <button role="tab" type="button" id="tab-com" aria-controls="pan-com" aria-selected="false">{t_compl}</button>
      </div>
      <div class="panel" role="tabpanel" id="pan-est" aria-labelledby="tab-est">
        <ul class="estudios">{form}
        </ul>
      </div>
      <div class="panel" role="tabpanel" id="pan-com" aria-labelledby="tab-com">
        <ul class="cursos">{compl}{creds}
        </ul>
      </div>
    </div>
  </section>

  <section id="obra" class="seccion alterna">
    <div class="contenedor">
      <header class="sec-cab revela">
        <p class="sec-num">06</p>
        <h2>{t_pub} y {t_proy_min}</h2>
      </header>
      {pubs}
      <h3 class="sub-obra revela">{t_proy}</h3>
      <div class="rejilla-obra">{proys}
      </div>
      <h3 class="sub-obra revela">{t_otros}</h3>
      <p class="aclara revela">{nota_otros}</p>
      <div class="rejilla-obra">{otros}
      </div>
    </div>
  </section>

  <section id="contacto" class="seccion contacto">
    <div class="contenedor">
      <div class="contacto-caja revela">
        <p class="sec-num">07</p>
        <h2>Conversemos</h2>
        <p class="contacto-txt">Para una entrevista o para recibir el currículo completo, escríbame:</p>
        <div class="correo">
          <a href="mailto:{correo}">{correo}</a>
          <button class="copiar grande" type="button" data-copiar="{correo}">Copiar correo</button>
        </div>
        <ul class="perfiles">
          <li><a class="boton" href="https://{linkedin}" rel="noopener" target="_blank">LinkedIn</a></li>
          <li><a class="boton" href="https://{researchgate}" rel="noopener" target="_blank">ResearchGate</a></li>
        </ul>
      </div>
    </div>
  </section>
</main>

<footer class="pie">
  <div class="contenedor">
    <p>{nombre} · Costa Rica</p>
    <p>Contenido tomado del currículo de referencia, Registro Maestro v{registro}.</p>
  </div>
</footer>
<a class="arriba" href="#inicio" aria-label="Volver arriba">↑</a>
<div class="aviso" role="status" aria-live="polite" hidden></div>
""".format(iniciales=e(iniciales), nav=nav, nombre=e(nombre), chips=chips, entrada=e(d["perfil"]["segs"][0]),
           correo=e(correo), linkedin=e(linkedin), researchgate=e(researchgate), n_areas=len(areas),
           n_terminos=n_terminos, anio="%.4f" % (1200.0 / (FIN + 1 - INI)), n_puestos=len(puestos), idioma=e(idioma), registro=e(M["registro"]), cif=cif,
           t_perfil=e(d["perfil"]["titulo"]), perfil=perfil, regla=regla, filas="".join(filas),
           t_exp=e(d["experiencia"]["titulo"]), exp="".join(exp), t_comp=e(co["titulo"]), comp="".join(comp), notas=notas,
           t_form=e(d["formacion"]["titulo"]), t_compl=e(d["complementaria"]["titulo"]), form="".join(form), compl=compl,
           creds=creds, t_pub=e(d["publicaciones"]["titulo"]), t_proy_min=e(d["proyectos"]["titulo"].lower()),
           t_otros=e(d["otros"]["titulo"]), t_proy=e(d["proyectos"]["titulo"]), pubs=pubs, nota_otros=e(d["otros"]["nota"]), proys=proys, otros=otros)

FUENTES = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
           '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,500;8..60,600;8..60,700'
           '&family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@500&display=swap">')
titulo = "%s — Currículo" % nombre
desc = "%s — %s" % (nombre, " · ".join(areas))

pagina = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{titulo}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#0d4a8d">
<link rel="icon" href="assets/img/icono.svg" type="image/svg+xml">
{fuentes}
<link rel="stylesheet" href="assets/css/estilo.css">
<script>document.documentElement.classList.add('js');try{{var t=localStorage.getItem('tema');if(t)document.documentElement.dataset.theme=t}}catch(_){{}}</script>
</head>
<body>
{cuerpo}<script src="assets/js/sitio.js" defer></script>
</body>
</html>
""".format(titulo=e(titulo), desc=e(desc), fuentes=FUENTES, cuerpo=cuerpo)

css = (AQUI / "estilo.css").read_text(encoding="utf-8")
js = (AQUI / "sitio.js").read_text(encoding="utf-8")
for sub in ("assets/css", "assets/img", "assets/js"):
    (OUT / sub).mkdir(parents=True, exist_ok=True)
(OUT / "index.html").write_text(pagina, encoding="utf-8")
(OUT / "assets/css/estilo.css").write_text(css, encoding="utf-8")
(OUT / "assets/js/sitio.js").write_text(js, encoding="utf-8")
from mejorar_presentacion import mejorar
mejorar(OUT)
print("index.html", len(pagina))

if PREVIA:
    previa = ("<title>Portafolio de Rubén Gago</title>\n%s\n<style>\n%s\n.solo-sitio{display:none!important}\n</style>\n"
              "<script>document.documentElement.classList.add('js')</script>\n%s<script>\n%s\n</script>\n") % (FUENTES, css, cuerpo, js)
    PREVIA.write_text(previa, encoding="utf-8")
    print("vista previa", len(previa))

