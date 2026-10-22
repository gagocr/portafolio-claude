# -*- coding: utf-8 -*-
"""Construye el sitio del portafolio desde el modelo del currículo de referencia (modelo.json).

Solo lleva lo que ya va en el currículo que recibe un empleador, menos: el teléfono, la
residencia y toda ubicación personal. Nunca lee la matriz entera: lee el modelo del CV.
    python3 construir_sitio.py MODELO.json SALIDA/
"""
import html
import json
import sys
from pathlib import Path

M = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
OUT = Path(sys.argv[2])
d = M["doc"]
e = html.escape

cab = d["cabecera"]
nombre = cab["nombre"]
areas = [x.strip() for x in cab["titular"].split("·")]
# Contacto público: correo y perfiles. Sin teléfono ni ubicación personal.
correo = "gagocr00@gmail.com"
assert correo in cab["linea1"]
enlaces = [x.strip() for x in cab["linea2"].split("·")]
linkedin = next(x for x in enlaces if "linkedin" in x)
researchgate = next(x for x in enlaces if "researchgate" in x)


def lista(xs, clase=""):
    return "<ul%s>%s</ul>" % (' class="%s"' % clase if clase else "", "".join("<li>%s</li>" % e(x) for x in xs))


# ---------- secciones
perfil = "".join('<p>%s</p>' % e(p) for p in d["perfil"]["segs"][1:])      # el primer párrafo abre la portada

exp = []
for i, p in enumerate(d["experiencia"]["puestos"]):
    nom = p["nom"]
    exp.append("""
      <article class="puesto">
        <div class="puesto-marca" aria-hidden="true"></div>
        <header class="puesto-cab">
          <h3>%s</h3>
          <p class="puesto-org">%s</p>
          <p class="puesto-meta"><span class="periodo">%s</span>%s</p>
        </header>
        %s
      </article>""" % (e(p["cargo"]), e(nom), e(p["per"]),
                       ('<span class="sep">·</span><span>%s</span>' % e(p["mod"])) if p.get("mod") else "",
                       lista(p.get("vinetas", []), "vinetas")))

comp = []
for r in d["competencias"]["rubros"]:
    comp.append("""
      <article class="tarjeta">
        <h3>%s</h3>
        %s
      </article>""" % (e(r["rotulo"]), lista(r["terminos"], "terminos")))
co = d["competencias"]
extra = []
for k in ("idiomas", "aprendizaje"):
    if co.get(k):
        extra.append('<div class="nota-comp"><strong>%s.</strong> %s</div>' % (e(co[k]["rotulo"]), e(co[k]["seg"])))

form = "".join("""
      <li>
        <p class="f-titulo">%s</p>
        <p class="f-inst">%s</p>
        <p class="f-fecha">%s</p>
      </li>""" % (e(f["cv"]), e(f["inst"]), e(f["cv_fecha"])) for f in d["formacion"]["items"])

compl = "".join("""
      <li><span class="c-act">%s</span><span class="c-inst">%s · %s</span></li>""" % (e(c["act"]), e(c["inst"]), e(c["fecha"]))
                for c in d["complementaria"]["items"])
creds = "".join("<li>%s</li>" % e(c) for c in d["complementaria"].get("credenciales", []))

pubs = "".join("""
      <article class="pub">
        <p class="pub-anio">%s</p>
        <div><h3>%s</h3><p>%s</p></div>
      </article>""" % (e(p["fecha"]), e(p["titulo"]), e(p["detalle"])) for p in d["publicaciones"]["items"])

proys = "".join("""
      <article class="tarjeta">
        <h3>%s</h3>
        <p class="periodo">%s</p>
        %s
      </article>""" % (e(p["titulo"]), e(p["periodo"]), lista(p["segs"], "vinetas")) for p in d["proyectos"]["items"])

otros = "".join("""
      <article class="tarjeta">
        <h3>%s</h3>
        <p class="tarjeta-sub">%s</p>
        <p class="periodo">%s</p>
        %s
      </article>""" % (e(p["nom"]), e(p["cargo"]), e(p["per"]), lista(p.get("vinetas", []), "vinetas")) for p in d["otros"]["puestos"])

chips = "".join('<li>%s</li>' % e(a) for a in areas)

# Tres cifras del perfil, con sus palabras: no se resumen ni se redondean
cifras = [("Desde 2011", "trayectoria laboral"),
          ("Más de 6.000", "ítems de colecciones patrimoniales descritos en DSpace"),
          ("Más de 500", "artículos marcados en XML-JATS validados para su indexación en SciELO")]
texto_perfil = " ".join(d["perfil"]["segs"])
assert "comenzó en 2011" in texto_perfil and "más de 6.000 ítems de colecciones patrimoniales en DSpace" in texto_perfil \
    and "más de 500 artículos académicos y científicos marcados en XML-JATS para su indexación en SciELO" in texto_perfil
cif = "".join('<li><span class="cifra">%s</span><span class="cifra-txt">%s</span></li>' % (e(a), e(b)) for a, b in cifras)

pagina = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{nombre} — Currículo</title>
<meta name="description" content="{nombre}: organización documental y de la información, SQL, Excel e indicadores, gestión comercial y servicios técnicos.">
<meta name="robots" content="noindex, nofollow">
<link rel="icon" href="assets/img/icono.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,500;8..60,600;8..60,700&family=Inter:wght@400;500;600&display=swap">
<link rel="stylesheet" href="assets/css/estilo.css">
</head>
<body>
<a class="saltar" href="#perfil">Ir al contenido</a>
<header class="barra">
  <div class="contenedor barra-in">
    <a class="marca" href="#inicio">{iniciales}</a>
    <nav aria-label="Secciones">
      <ul>
        <li><a href="#perfil">Perfil</a></li>
        <li><a href="#experiencia">Experiencia</a></li>
        <li><a href="#competencias">Competencias</a></li>
        <li><a href="#formacion">Formación</a></li>
        <li><a href="#contacto">Contacto</a></li>
      </ul>
    </nav>
  </div>
</header>

<main id="inicio">
  <section class="portada">
    <div class="contenedor portada-in">
      <p class="sobre">Currículo</p>
      <h1>{nombre}</h1>
      <ul class="areas">{chips}</ul>
      <p class="entrada">{entrada}</p>
      <div class="acciones">
        <a class="boton primario" href="mailto:{correo}">Escribirme</a>
        <a class="boton" href="https://{linkedin}" rel="noopener" target="_blank">LinkedIn</a>
        <a class="boton" href="https://{researchgate}" rel="noopener" target="_blank">ResearchGate</a>
      </div>
      <ul class="cifras">{cif}</ul>
    </div>
  </section>

  <section id="perfil" class="seccion">
    <div class="contenedor estrecho">
      <h2><span class="num">01</span>{t_perfil}</h2>
      <div class="prosa">{perfil}</div>
    </div>
  </section>

  <section id="experiencia" class="seccion alterna">
    <div class="contenedor">
      <h2><span class="num">02</span>{t_exp}</h2>
      <div class="linea">{exp}
      </div>
    </div>
  </section>

  <section id="competencias" class="seccion">
    <div class="contenedor">
      <h2><span class="num">03</span>{t_comp}</h2>
      <div class="rejilla">{comp}
      </div>
      <div class="notas-comp">{extra}</div>
    </div>
  </section>

  <section id="formacion" class="seccion alterna">
    <div class="contenedor">
      <h2><span class="num">04</span>{t_form}</h2>
      <div class="dos">
        <div>
          <h3 class="sub">Estudios</h3>
          <ul class="formacion">{form}
          </ul>
        </div>
        <div>
          <h3 class="sub">{t_compl}</h3>
          <ul class="complementaria">{compl}
          </ul>
          <ul class="credenciales">{creds}</ul>
        </div>
      </div>
    </div>
  </section>

  <section id="publicaciones" class="seccion">
    <div class="contenedor">
      <h2><span class="num">05</span>{t_pub}</h2>
      {pubs}
    </div>
  </section>

  <section id="proyectos" class="seccion alterna">
    <div class="contenedor">
      <h2><span class="num">06</span>{t_proy}, {t_otros_min}</h2>
      <p class="aclara">{nota_otros}</p>
      <div class="rejilla">{proys}{otros}
      </div>
    </div>
  </section>

  <section id="contacto" class="seccion contacto">
    <div class="contenedor estrecho">
      <h2><span class="num">07</span>Contacto</h2>
      <p class="contacto-txt">Para una entrevista o para recibir el currículo completo, escríbame:</p>
      <p class="correo"><a href="mailto:{correo}">{correo}</a></p>
      <ul class="perfiles">
        <li><a href="https://{linkedin}" rel="noopener" target="_blank">{linkedin}</a></li>
        <li><a href="https://{researchgate}" rel="noopener" target="_blank">{researchgate}</a></li>
      </ul>
    </div>
  </section>
</main>

<footer class="pie">
  <div class="contenedor">
    <p>{nombre} · Costa Rica</p>
    <p class="pie-fuente">Contenido tomado del currículo de referencia, Registro Maestro v{registro}.</p>
  </div>
</footer>
</body>
</html>
""".format(nombre=e(nombre), iniciales=e("".join(w[0] for w in nombre.split()[:2])), chips=chips,
           entrada=e(d["perfil"]["segs"][0]), correo=e(correo), linkedin=e(linkedin), researchgate=e(researchgate),
           cif=cif, t_perfil=e(d["perfil"]["titulo"]), perfil=perfil, t_exp=e(d["experiencia"]["titulo"]), exp="".join(exp),
           t_comp=e(d["competencias"]["titulo"]), comp="".join(comp), extra="".join(extra), t_form=e(d["formacion"]["titulo"]),
           form=form, t_compl=e(d["complementaria"]["titulo"]), compl=compl, creds=creds, t_pub=e(d["publicaciones"]["titulo"]),
           pubs=pubs, t_proy=e(d["proyectos"]["titulo"]), t_otros_min=e(d["otros"]["titulo"].lower()),
           nota_otros=e(d["otros"]["nota"]), proys=proys, otros=otros, registro=e(M["registro"]))

(OUT / "assets" / "css").mkdir(parents=True, exist_ok=True)
(OUT / "assets" / "img").mkdir(parents=True, exist_ok=True)
(OUT / "index.html").write_text(pagina, encoding="utf-8")
print("index.html", len(pagina))
