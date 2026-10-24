"""Capa de presentación independiente; no modifica los hechos del currículo."""
from pathlib import Path
import re, shutil

EXPLORADOR = '''
<section class="explorador seccion" id="explorar" aria-labelledby="explorar-titulo">
 <div class="contenedor">
  <div class="explorar-cab"><div><p class="sobre">CUATRO ÁREAS · UNA TRAYECTORIA</p><h2 id="explorar-titulo">Explora lo que puedo aportar.</h2></div><p>Elige un área y descubre las funciones, herramientas y entornos donde he trabajado.</p></div>
  <div class="rutas">
   <a class="ruta ruta-documental" href="#experiencia" data-ruta="documental"><span class="ruta-num">01 / INFORMACIÓN</span><span class="ruta-icono" aria-hidden="true"><svg viewBox="0 0 24 24" focusable="false"><path d="M6 3h8l4 4v14H6Z"/><path d="M14 3v5h4M9 12h6m-6 4h6"/></svg></span><h3>Dar orden<br>a la información.</h3><p>Expedientes, colecciones patrimoniales y publicación académica.</p><span class="ruta-herr">DSpace · XML-JATS · Metadatos</span><span class="ruta-ir">Explorar experiencia <b>↗</b></span></a>
   <a class="ruta ruta-datos" href="#experiencia" data-ruta="datos"><span class="ruta-num">02 / DATOS</span><span class="ruta-icono" aria-hidden="true"><svg viewBox="0 0 24 24" focusable="false"><ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v7c0 4 16 4 16 0V5M4 12v7c0 4 16 4 16 0v-7"/></svg></span><h3>Consultar, registrar<br>y reportar.</h3><p>Consultas SQL, indicadores comerciales y encuestas de opinión.</p><span class="ruta-herr">SQL · Excel · CSPro</span><span class="ruta-ir">Explorar experiencia <b>↗</b></span></a>
   <a class="ruta ruta-comercial" href="#experiencia" data-ruta="comercial"><span class="ruta-num">03 / GESTIÓN</span><span class="ruta-icono" aria-hidden="true"><svg viewBox="0 0 24 24" focusable="false"><rect x="4" y="5" width="16" height="17" rx="2"/><path d="M9 5V2h6v3M8 10l1 1 2-2m3 1h3M8 16l1 1 2-2m3 1h3"/></svg></span><h3>Acompañar<br>cada proceso.</h3><p>Asesoría de ventas, acuerdos de pago y administración de propiedades.</p><span class="ruta-herr">Salesforce · Clientes · Proveedores</span><span class="ruta-ir">Explorar experiencia <b>↗</b></span></a>
   <a class="ruta ruta-tecnica" href="#experiencia" data-ruta="tecnica"><span class="ruta-num">04 / TÉCNICA</span><span class="ruta-icono" aria-hidden="true"><svg viewBox="0 0 24 24" focusable="false"><path d="M14 6a5 5 0 0 0-6 6L2 18l4 4 6-6a5 5 0 0 0 6-6l-4 4-4-4Z"/></svg></span><h3>Llevar las tareas<br>a la práctica.</h3><p>Instalaciones, domótica, mantenimiento y operación de bodega.</p><span class="ruta-herr">Banda ancha · WiFi · Zigbee</span><span class="ruta-ir">Explorar experiencia <b>↗</b></span></a>
  </div>
 </div>
</section>
'''
FILTROS = '''<div class="explorar-filtros solo-sitio" hidden>
 <label class="buscar-puesto">Buscar en la trayectoria<input type="search" id="buscar-puesto" placeholder="Empresa, herramienta o función…" autocomplete="off"></label>
 <div class="filtros-area" role="group" aria-label="Filtrar experiencia"><button type="button" data-area="todas" aria-pressed="true">Todas</button><button type="button" data-area="documental" aria-pressed="false">Información</button><button type="button" data-area="datos" aria-pressed="false">Datos</button><button type="button" data-area="comercial" aria-pressed="false">Gestión</button><button type="button" data-area="tecnica" aria-pressed="false">Técnica</button><button type="button" data-area="operativa" aria-pressed="false">Operación</button></div>
 <p id="resultado-puestos" role="status"></p><button type="button" class="mini" id="limpiar-puestos">Restablecer vista</button>
</div>'''

def mejorar(salida):
 salida=Path(salida); path=salida/'index.html'; pagina=path.read_text()
 if 'id="explorar"' in pagina:return
 pagina=pagina.replace('— Currículo</title>','— Portafolio profesional</title>').replace('Currículo · Costa Rica','Portafolio profesional · Costa Rica')
 pagina=pagina.replace('<section id="perfil"',EXPLORADOR+'\n<section id="perfil"',1)
 pagina=pagina.replace('<div class="linea">',FILTROS+'\n<div class="linea">',1)
 pagina=pagina.replace('<ul class="areas">','<p class="portada-lema">Información, criterio<br>y trabajo aplicado.</p><ul class="areas">',1)
 pagina=pagina.replace('<div class="acciones">','<div class="acciones"><a class="boton primario" href="#explorar">Explorar mi perfil ↗</a>',1)
 pagina=pagina.replace('Ficha de registro','Mi perfil, de un vistazo')
 pagina=re.sub(r'(\d+) logros',r'\1 funciones',pagina)
 pagina=re.sub(r'(\d+) logro',r'\1 función',pagina)
 pagina=pagina.replace('</head>','<link rel="stylesheet" href="assets/css/explorar.css">\n</head>')
 pagina=pagina.replace('</body>','<script src="assets/js/explorar.js" defer></script>\n</body>')
 path.write_text(pagina)
 for ext in ('css','js'):
  dest=salida/'assets'/ext;dest.mkdir(parents=True,exist_ok=True)
  shutil.copyfile(Path(__file__).parent/('explorar.'+ext),dest/('explorar.'+ext))

if __name__=='__main__':
 import sys
 mejorar(sys.argv[1] if len(sys.argv)>1 else Path(__file__).resolve().parents[1])
