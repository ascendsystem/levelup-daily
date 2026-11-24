#!/usr/bin/env python3
"""Build the LEVELUP DAILY static site for GitHub Pages."""
from __future__ import annotations

import html
import json
import re
import shutil
import unicodedata
import xml.etree.ElementTree as ET
from collections import defaultdict
from datetime import date
from pathlib import Path
from urllib.parse import urlparse
from image_audit import remember_legacy, write_audit
from adsense import (
    cmp_markup as configured_cmp_markup,
    cmp_preferences_markup,
    global_tag as adsense_global_tag,
    mode as adsense_mode,
    recovery_markup as configured_recovery_markup,
    render_slot as render_adsense_slot,
    sync_ads_txt,
    validate_config as validate_adsense_config,
)
from check_adsense import audit_generated_site

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "content" / "articles.json"
OUT = ROOT
SITE = json.loads((ROOT / "site.json").read_text(encoding="utf-8"))
ARTICLES = json.loads(SOURCE.read_text(encoding="utf-8"))
EXTRA_ARTICLES = json.loads((ROOT / "content" / "additional-articles.json").read_text(encoding="utf-8"))
EXTRA_ARTICLES.extend(json.loads((ROOT / "content" / "gta-launch-guides.json").read_text(encoding="utf-8")))
EXTRA_ARTICLES.extend(json.loads((ROOT / "content" / "gta-update-23-nov.json").read_text(encoding="utf-8")))
EXTRA_ARTICLES.extend(json.loads((ROOT / "content" / "gta-music-23-nov.json").read_text(encoding="utf-8")))
EXTRA_ARTICLES.extend(json.loads((ROOT / "content" / "gta-deep-dive-articles.json").read_text(encoding="utf-8")))
ARTICLES.extend(EXTRA_ARTICLES)
RANKED_ITEMS = json.loads((ROOT / "content" / "ranked-entries.json").read_text(encoding="utf-8"))
INLINE_MEDIA = json.loads((ROOT / "content" / "inline-media.json").read_text(encoding="utf-8"))
EXPANSIONS = json.loads((ROOT / "content" / "expansions.json").read_text(encoding="utf-8"))
FINAL_SECTIONS = json.loads((ROOT / "content" / "final-sections.json").read_text(encoding="utf-8"))
for article in ARTICLES:
    if article["slug"] in RANKED_ITEMS:
        article["ranked_items"] = RANKED_ITEMS[article["slug"]]
    if article["slug"] in INLINE_MEDIA:
        article["inline_media"] = INLINE_MEDIA[article["slug"]]
    article["sections"].extend(EXPANSIONS.get(article["slug"], []))
    article["sections"].extend(FINAL_SECTIONS.get(article["slug"], []))
BASE_URL = SITE["base_url"].rstrip("/")
_base_parts = urlparse(BASE_URL)
PUBLIC_SITE = bool(_base_parts.scheme == "https" and _base_parts.netloc and "." in _base_parts.netloc and not any(token in BASE_URL.lower() for token in ("tu-usuario", "example.com", "localhost", "pendiente")))
SOCIAL_IMAGE = "assets/images/og-cover.webp"
CATEGORIES = {
    "gta-6": ("GTA VI", "Noticias, guías y contexto de GTA VI. Fechas, plataformas y datos separados de las especulaciones."),
    "videojuegos": ("Videojuegos", "Noticias, análisis, recomendaciones y guías para elegir tu próxima partida."),
    "playstation": ("PlayStation", "Juegos, novedades y guías para PS5 y el ecosistema PlayStation."),
    "xbox": ("Xbox", "Novedades, juegos y guías para las consolas y servicios Xbox."),
    "pc-gaming": ("PC Gaming", "Juegos, componentes y guías para jugar en ordenador."),
    "nintendo": ("Nintendo", "Juegos, franquicias y recomendaciones del universo Nintendo."),
    "anime": ("Anime", "Recomendaciones, novedades, rankings y guías de anime."),
    "manga": ("Manga", "Guías para descubrir manga, adaptaciones y lecturas en español."),
    "rankings": ("Rankings", "Listas editoriales con criterios claros, contexto y fuentes."),
    "curiosidades": ("Curiosidades", "Secretos, detalles y descubrimientos sobre videojuegos, anime y cultura digital."),
    "guias": ("Guías", "Consejos prácticos para jugar, comprar y encontrar tu próxima historia."),
    "tecnologia": ("Tecnología", "Hardware y tecnología explicados para jugadores."),
}

LEGAL = {
    "sobre-nosotros": ("Sobre nosotros", "Qué es LEVELUP DAILY y cómo trabajamos.", """
<p>LEVELUP DAILY es un proyecto editorial independiente sobre videojuegos, anime, manga y cultura digital. Nuestro lema es «Todo lo que juega, importa.»</p>
<h2>Qué publicamos</h2><p>Publicamos noticias cuando podemos verificar sus fuentes, además de guías, rankings y artículos de contexto. Cada pieza debe indicar qué es un hecho, qué es una opinión y cuándo se revisó la información que puede cambiar.</p>
<h2>Quién está detrás del sitio</h2><p><strong>Titular:</strong> [PENDIENTE: nombre del titular]. <strong>Empresa:</strong> [PENDIENTE: empresa, si procede]. <strong>Contacto:</strong> [PENDIENTE: correo de contacto]. Completa estos datos antes de publicar el sitio.</p>
<h2>Independencia editorial</h2><p>Las recomendaciones se elaboran con criterios editoriales. Una futura relación comercial o un contenido patrocinado deberá identificarse de forma clara y no alterar las conclusiones presentadas como independientes.</p>
"""),
    "contacto": ("Contacto", "Cómo escribir a la redacción de LEVELUP DAILY.", """
<p>Utiliza este formulario para preparar una consulta, una corrección o una propuesta editorial. La dirección de correo de contacto todavía está pendiente de configurar.</p>
<form class="contact-form" id="contact-form">
<label for="contact-name">Nombre</label><input id="contact-name" name="name" autocomplete="name" required maxlength="100">
<label for="contact-email">Correo electrónico</label><input id="contact-email" name="email" type="email" autocomplete="email" required maxlength="254">
<label for="contact-subject">Asunto</label><input id="contact-subject" name="subject" required maxlength="160">
<label for="contact-message">Mensaje</label><textarea id="contact-message" name="message" rows="7" required maxlength="5000"></textarea>
<p class="contact-privacy">El navegador valida estos campos. Consulta la <a href="../politica-de-privacidad/">política de privacidad</a>.</p>
<button class="button button-primary" type="button" id="contact-validate" disabled>Validar mensaje</button>
<p class="contact-status" id="contact-status" role="status" aria-live="polite">El envío todavía no está conectado. Este formulario no transmite ni almacena tus datos.</p>
</form>
<h2>Correcciones</h2><p>Incluye la URL del artículo, el dato que consideras incorrecto y un enlace a la fuente primaria que lo corrige. Revisaremos el aviso y, cuando corresponda, actualizaremos el texto y su fecha visible.</p>
<h2>Propuestas y publicidad</h2><p>Las comunicaciones comerciales deben identificarse como tales. El envío de una propuesta no garantiza publicación ni cobertura editorial.</p>
"""),
    "politica-de-privacidad": ("Política de privacidad", "Información que debe completar el titular antes de recoger datos.", """
<div class="notice"><strong>Borrador pendiente de completar y revisar.</strong> No publiques esta página hasta confirmar responsable, finalidad, base jurídica, proveedores, plazos y derechos aplicables.</div>
<h2>Responsable del tratamiento</h2><p>Responsable: [PENDIENTE: nombre o entidad]. NIF: [PENDIENTE]. Domicilio: [PENDIENTE]. Correo para privacidad: [PENDIENTE]. Dominio: [PENDIENTE].</p>
<h2>Datos y finalidades</h2><p>La versión actual del sitio es estática y no solicita cuentas ni comentarios. El formulario de contacto solo valida campos en el navegador: no transmite ni almacena sus valores. El buscador funciona en el navegador. Actualiza este texto antes de conectar el formulario, incorporar analítica, newsletter, publicidad personalizada u otros proveedores que traten datos.</p>
<h2>Cookies y almacenamiento local</h2><p>La web incluye una preferencia local para recordar la elección del aviso de privacidad. No se han insertado etiquetas de analítica ni anuncios de terceros. Antes de activar servicios, identifica qué tecnologías usan, su duración, finalidad y los destinatarios.</p>
<h2>Derechos y reclamaciones</h2><p>Indica aquí el canal y procedimiento para ejercer los derechos que correspondan y la autoridad de control competente, una vez confirmados los datos del responsable. No envíes documentación sensible a una dirección todavía sin configurar.</p>
<h2>Actualizaciones</h2><p>Publica la fecha de revisión y conserva versiones anteriores cuando sea necesario. Este texto es una plantilla informativa, no asesoramiento jurídico.</p>
"""),
    "politica-de-cookies": ("Política de cookies", "Estado actual de cookies y servicios de terceros.", """
<div class="notice"><strong>Estado de la implementación:</strong> no se han añadido cookies publicitarias ni etiquetas de analítica. La web usa almacenamiento local del navegador para recordar la preferencia del aviso.</div>
<h2>Qué se usa actualmente</h2><p>El sitio no integra todavía Google Analytics, Google AdSense, una newsletter ni píxeles de redes sociales. El índice de búsqueda se descarga como un archivo estático. La preferencia de consentimiento queda guardada en el almacenamiento local de este navegador.</p>
<h2>Antes de activar publicidad o analítica</h2><p>Configura una plataforma de gestión del consentimiento (CMP) compatible con tus servicios y jurisdicciones. La herramienta incluida es una interfaz inicial, no una certificación CMP ni una garantía de cumplimiento. No insertes etiquetas de publicidad personalizada antes de obtener el consentimiento que corresponda y configurar las señales de consentimiento requeridas.</p>
<h2>Cómo cambiar la elección</h2><p>Usa «Preferencias de privacidad» en el pie de página para volver a abrir el panel y cambiar tu elección. También puedes borrar el almacenamiento del sitio desde el navegador.</p>
<h2>Revisión</h2><p>Al añadir un proveedor, actualiza esta política con nombre, finalidad, duración, transferencias y forma de rechazar o retirar el consentimiento. Consulta la documentación vigente del proveedor y asesoramiento adecuado para tu caso.</p>
"""),
    "aviso-legal": ("Aviso legal", "Identificación del titular y condiciones de uso del sitio.", """
<div class="notice"><strong>Borrador editable.</strong> Completa los datos identificativos del titular y revisa el texto antes de publicar.</div>
<h2>Datos del titular</h2><p>Titular: [PENDIENTE: nombre o razón social]. NIF: [PENDIENTE]. Domicilio: [PENDIENTE]. Correo: [PENDIENTE]. Dominio: [PENDIENTE].</p>
<h2>Objeto y uso</h2><p>Este sitio ofrece contenidos editoriales sobre videojuegos, anime, manga y entretenimiento digital. El usuario se compromete a utilizarlo conforme a la legislación aplicable y a no interferir con su funcionamiento.</p>
<h2>Propiedad intelectual</h2><p>Los textos y recursos gráficos pertenecen a sus respectivos autores o titulares. Las marcas y nombres de juegos mencionados pertenecen a sus propietarios y se citan con finalidad informativa. Cada imagen debe conservar su procedencia y la atribución que exija su titular.</p>
<h2>Enlaces y responsabilidad</h2><p>Los enlaces externos llevan a páginas de terceros cuyos contenidos pueden cambiar. Se incluyen como referencia; el titular debe revisar su vigencia y finalidad. La información editorial se proporciona con fecha de actualización y no sustituye las fuentes del fabricante para compras, compatibilidad o seguridad.</p>
"""),
    "politica-editorial": ("Política editorial", "Criterios para verificar, redactar y actualizar contenidos.", """
<h2>Verificación</h2><p>Priorizamos anuncios oficiales, documentación del desarrollador, páginas de producto y fuentes primarias. Cuando usamos una fuente secundaria, la identificamos. Rumores y especulación aparecen etiquetados y nunca se presentan como hechos confirmados.</p>
<h2>Rankings y recomendaciones</h2><p>Los rankings son selecciones editoriales salvo que indiquemos una encuesta o clasificación externa verificable. Explicamos el criterio, no inventamos puntuaciones ni atribuimos resultados a una plataforma sin fuente.</p>
<h2>Correcciones y actualizaciones</h2><p>Las páginas muestran fechas de publicación y revisión. Si un dato cambia, actualizamos el texto, comprobamos el enlace de origen y damos contexto cuando el cambio afecta a una recomendación.</p>
<h2>Patrocinios y conflictos</h2><p>El sitio no debe publicar contenido patrocinado sin identificarlo de manera visible. Las relaciones comerciales, productos cedidos y enlaces de afiliación se deben declarar junto al contenido antes de incorporarlos.</p>
<h2>Uso de imágenes</h2><p>El sitio usa capturas y material promocional de videojuegos y anime, además de fotografías proporcionadas para la web. Antes de publicar o monetizar una imagen de terceros, el titular debe confirmar que dispone de autorización o licencia para su uso editorial digital y conservar la atribución exigida por el titular de derechos.</p>
"""),
}

def esc(value: str) -> str:
    return html.escape(str(value), quote=True)

def words(text: str) -> int:
    return len(re.findall(r"\b[\wÁÉÍÓÚÜÑáéíóúüñ]+\b", re.sub("<[^>]+>", " ", text)))

def rel(depth: int, route: str) -> str:
    route = route.lstrip("/")
    if route.endswith("/"):
        route += "index.html"
    return ("../" * depth) + route

def article_path(item: dict) -> str:
    return f"{item['category']}/{item['slug']}/"

def cover_path(item: dict) -> str | None:
    custom = item.get("cover_image")
    if custom and (ROOT / custom).is_file():
        return Path(custom).as_posix()
    for extension in ("webp", "jpg", "jpeg", "png"):
        candidate = ROOT / "assets" / "images" / "covers" / f"{item['cover']}.{extension}"
        if candidate.is_file():
            return candidate.relative_to(ROOT).as_posix()
    return None

def image_request(item: dict, usage="portada") -> str:
    if usage == "portada":
        return item.get("cover_photo_needed") or f"FOTO DE PORTADA — imagen real relacionada con «{item['title']}»."
    sections=item.get("sections",[])
    section=sections[max(0,min(1,len(sections)-1))].get("title",item["title"]) if sections else item["title"]
    return item.get("inline_photo_needed") or f"FOTO INTERIOR — captura o fotograma relacionado con «{item['title']}», para «{section}»."

def photo_request_block(label: str, class_name="photo-request") -> str:
    return f'<div class="{class_name}" role="img" aria-label="{esc(label)}"><span class="photo-request-kicker">FOTO PENDIENTE</span><strong>{esc(label)}</strong></div>'

def cover_visual(item: dict, depth: int, link=True, image_class="") -> str:
    path = cover_path(item)
    article_href = rel(depth, article_path(item))
    if path:
        image_alt = item.get("image_alt") or f"Imagen relacionada con {item['title']}"
        media = f'<img src="{rel(depth,path)}" alt="{esc(image_alt)}" loading="lazy" width="1200" height="720">'
    else:
        media = photo_request_block(image_request(item), "photo-request photo-request-card")
    if link:
        return f'<a class="card-image {image_class}" href="{article_href}">{media}</a>'
    return media

def schema_org() -> str:
    return json.dumps({"@context":"https://schema.org","@type":"Organization","name":SITE["publisher"],"url":BASE_URL,"logo":BASE_URL+"/assets/images/logo.svg"}, ensure_ascii=False)

def breadcrumb_schema(items, current_url=None):
    elements=[]
    for position,(label,route) in enumerate(items,1):
        target=current_url if route is None and current_url else BASE_URL+"/"+route.lstrip("/")
        entry={"@type":"ListItem","position":position,"name":label,"item":target}
        elements.append(entry)
    return {"@type":"BreadcrumbList","itemListElement":elements}

def common_head(title: str, description: str, canonical: str, image: str, depth: int, noindex=False, jsonld=None, ads_eligible=False) -> str:
    canonical_url = BASE_URL + "/" + canonical.lstrip("/") if PUBLIC_SITE else ""
    image = image or SOCIAL_IMAGE
    img = BASE_URL + "/" + image.lstrip("/") if PUBLIC_SITE else ""
    robots = "index,follow,max-image-preview:large" if PUBLIC_SITE and not noindex else "noindex,nofollow"
    schema = json.dumps(jsonld or schema_org(), ensure_ascii=False) if PUBLIC_SITE and not noindex else ""
    og_type="article" if canonical.count("/")>=2 else "website"
    cmp = configured_cmp_markup(SITE, ROOT) if PUBLIC_SITE else ""
    cmp_preferences = cmp_preferences_markup(SITE, ROOT) if PUBLIC_SITE else ""
    adsense_tag = adsense_global_tag(SITE) if PUBLIC_SITE and ads_eligible else ""
    recovery_markup = configured_recovery_markup(SITE, ROOT) if PUBLIC_SITE and ads_eligible else ""
    canonical_tag=f'<link rel="canonical" href="{esc(canonical_url)}">' if canonical_url else ""
    verification_token = str(SITE.get("google_search_console_verification", "")).strip()
    verification_tag = f'<meta name="google-site-verification" content="{esc(verification_token)}">' if canonical == "" and verification_token else ""
    social_tags=(f'<meta property="og:url" content="{esc(canonical_url)}"><meta property="og:image" content="{esc(img)}"><meta name="twitter:image" content="{esc(img)}">') if PUBLIC_SITE else ""
    schema_tag=f'<script type="application/ld+json">{schema}</script>' if schema else ""
    return f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(description)}"><meta name="robots" content="{robots}">
{canonical_tag}{verification_tag}<link rel="icon" type="image/svg+xml" href="{rel(depth,'assets/images/favicon.svg')}"><meta name="theme-color" content="#0b0d12">
<meta property="og:type" content="{og_type}"><meta property="og:site_name" content="{esc(SITE['name'])}"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(description)}">{social_tags}
<link rel="preload" href="{rel(depth,'assets/css/style.css')}" as="style"><link rel="stylesheet" href="{rel(depth,'assets/css/style.css')}"><link rel="stylesheet" href="{rel(depth,'assets/css/responsive.css')}">
{cmp}{cmp_preferences}{adsense_tag}{recovery_markup}{schema_tag}<script defer src="{rel(depth,'assets/js/main.js')}"></script></head>'''

def ad_slot(position):
    return render_adsense_slot(SITE, position)

def header(depth: int) -> str:
    home = rel(depth, "index.html")
    nav = [("GTA VI","gta-6/"),("Videojuegos","videojuegos/"),("PlayStation","playstation/"),("Xbox","xbox/"),("PC","pc-gaming/"),("Nintendo","nintendo/"),("Anime","anime/"),("Manga","manga/"),("Rankings","rankings/"),("Curiosidades","curiosidades/"),("Guías","guias/"),("Tecnología","tecnologia/")]
    links = "".join(f'<a href="{rel(depth,path)}">{esc(label)}</a>' for label,path in nav)
    return f'''<a class="skip-link" href="#contenido">Saltar al contenido</a><header class="site-header"><div class="header-inner"><a class="brand" href="{home}" aria-label="LEVELUP DAILY, inicio"><img src="{rel(depth,'assets/images/logo.svg')}" width="46" height="46" alt=""><span><strong>LEVELUP <i>DAILY</i></strong><small>{esc(SITE['tagline'])}</small></span></a>
<button class="menu-toggle" type="button" aria-expanded="false" aria-controls="main-nav"><span class="sr-only">Abrir menú</span><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg></button><nav id="main-nav" class="main-nav" aria-label="Navegación principal">{links}</nav>
<form class="search-form" action="{rel(depth,'buscar/')}" method="get" role="search"><label class="sr-only" for="q-{depth}">Buscar artículos</label><input id="q-{depth}" name="q" type="search" placeholder="Buscar…"><button aria-label="Buscar" type="submit"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="10.8" cy="10.8" r="6.8"/><path d="m16 16 5 5"/></svg></button></form></div></header>'''

def footer(depth: int) -> str:
    links = [("Sobre nosotros","sobre-nosotros/"),("Contacto","contacto/"),("Privacidad","politica-de-privacidad/"),("Cookies","politica-de-cookies/"),("Aviso legal","aviso-legal/"),("Política editorial","politica-editorial/")]
    category_links="".join(f'<a href="{rel(depth,slug+"/")}">{esc(name)}</a>' for slug,(name,_) in CATEGORIES.items())
    if adsense_mode(SITE) == "active":
        footer_controls = f'<div class="footer-bottom"><span>© {date.today().year} LEVELUP DAILY</span><button type="button" class="text-button" data-cmp-settings>Preferencias de privacidad</button><span>Publicidad de Google AdSense</span></div>'
        consent_ui = ""
    else:
        footer_controls = f'<div class="footer-bottom"><span>© {date.today().year} LEVELUP DAILY</span><button type="button" class="text-button" data-open-consent>Preferencias de privacidad</button><span>Sin unidades publicitarias activas</span></div>'
        consent_ui = f'''<section class="consent-banner" id="consent-banner" hidden aria-label="Preferencias de privacidad"><div><strong>Tu privacidad importa</strong><p>Este sitio recuerda tu elección en este navegador. No hay unidades publicitarias activas.</p></div><div class="consent-actions"><button type="button" class="button button-quiet" data-consent="reject">Rechazar opcionales</button><button type="button" class="button button-primary" data-open-consent>Preferencias</button></div></section>
<dialog class="consent-dialog" id="consent-dialog" aria-labelledby="consent-title"><div class="dialog-inner"><button class="dialog-close" type="button" aria-label="Cerrar" data-close-consent>×</button><span class="eyebrow">PRIVACIDAD</span><h2 id="consent-title">Elige tus preferencias</h2><p>Ahora no se cargan unidades de anuncios. Esta preferencia local no es una CMP ni envía señales TCF.</p><label class="consent-choice"><span><strong>Almacenamiento esencial</strong><small>Recuerda tu decisión.</small></span><input type="checkbox" checked disabled aria-label="Siempre activo"></label><label class="consent-choice"><span><strong>Analítica</strong><small>No está instalada.</small></span><input type="checkbox" data-purpose="analytics" disabled></label><label class="consent-choice"><span><strong>Publicidad</strong><small>No hay etiquetas publicitarias activas.</small></span><input type="checkbox" data-purpose="ads" disabled></label><div class="dialog-actions"><button type="button" class="button button-quiet" data-consent="reject">Rechazar opcionales</button><button type="button" class="button button-primary" data-consent="save">Guardar selección</button></div><p class="fine-print">Para más información, consulta la <a href="{rel(depth,'politica-de-cookies/')}">política de cookies</a>.</p></div></dialog>'''
    return f'''<footer class="site-footer"><div class="footer-top"><a class="brand" href="{rel(depth,'index.html')}"><img src="{rel(depth,'assets/images/logo.svg')}" width="42" height="42" alt=""><span><strong>LEVELUP <i>DAILY</i></strong><small>{esc(SITE['tagline'])}</small></span></a><p>Gaming, anime y cultura digital con contexto y criterio editorial.</p></div><nav class="footer-topic-links" aria-label="Categorías">{category_links}</nav><nav class="footer-links" aria-label="Información">{''.join(f'<a href="{rel(depth,path)}">{esc(label)}</a>' for label,path in links)}<a href="{rel(depth,'sitemap.xml')}">Sitemap</a></nav>{footer_controls}</footer>
{consent_ui}<button class="to-top" type="button" aria-label="Volver arriba" title="Volver arriba">↑</button>'''

def card(item: dict, depth: int, compact=False) -> str:
    cls = "story-card story-card-compact" if compact else "story-card"
    path = rel(depth, article_path(item))
    return f'''<article class="{cls}">{cover_visual(item,depth)}<div class="card-body"><a class="category-label" href="{rel(depth,item['category']+'/')}">{esc(CATEGORIES[item['category']][0])}</a><h3><a href="{path}">{esc(item['title'])}</a></h3><p>{esc(item['description'])}</p><div class="card-meta"><time datetime="{item['updated']}">{date.fromisoformat(item['updated']).strftime('%d/%m/%Y')}</time><span>{item['readTime']} min</span></div></div></article>'''

def breadcrumbs(items, depth):
    parts = [f'<a href="{rel(depth,"index.html")}">Inicio</a>']
    for label,path in items:
        if path:
            parts.append(f'<a href="{rel(depth,path)}">{esc(label)}</a>')
        else:
            parts.append(f'<span aria-current="page">{esc(label)}</span>')
    return '<nav class="breadcrumbs" aria-label="Migas de pan">' + '<span class="crumb-sep" aria-hidden="true">/</span>'.join(parts) + '</nav>'

def page_shell(title, description, canonical, image, depth, body, jsonld=None, noindex=False, ads_eligible=False):
    return common_head(title, description, canonical, image, depth, noindex, jsonld, ads_eligible) + f'<body>{header(depth)}{body}{footer(depth)}</body></html>'

def home_page():
    depth=0
    ordered=sorted(ARTICLES,key=lambda x:(x["updated"],x["date"],x["slug"]),reverse=True)
    def in_category(slug):
        return [a for a in ordered if slug in a["categories"]]
    gta=in_category("gta-6")
    anime=in_category("anime")
    rankings=[a for a in ordered if a["category"]=="rankings" or "rankings" in a["categories"]]
    guides=in_category("guias")
    hero=next(a for a in ARTICLES if a["slug"]=="todo-sobre-gta-6")
    side=[a for a in ordered if a is not hero][:3]
    popular_slugs=("mapa-gta-6","mejores-juegos-ps5","animes-mejor-valorados-crunchyroll","mejores-juegos-gratis","elegir-pc-gaming-2026","mejores-animes-para-empezar","mejores-juegos-terror","mejores-juegos-xbox","mejores-animes-accion","secretos-y-easter-eggs-videojuegos")
    popular=[next(a for a in ARTICLES if a["slug"]==slug) for slug in popular_slugs]
    featured_slugs={hero["slug"],*(a["slug"] for a in side),*(a["slug"] for a in ordered[:12]),*(a["slug"] for a in popular)}
    more=[a for a in ordered if a["slug"] not in featured_slugs][:12]
    body=f'''<main id="contenido"><section class="hero-section page-wrap"><div class="hero-copy"><span class="eyebrow"><span class="live-dot"></span> EL JUEGO YA ESTÁ AQUÍ · ACTUALIZADO</span><a class="category-label" href="{rel(depth,'gta-6/')}">GTA VI</a><h1>{esc(hero['title'])}</h1><p>{esc(hero['dek'])}</p><div class="hero-meta"><time datetime="{hero['updated']}">Actualizado el {date.fromisoformat(hero['updated']).strftime('%d/%m/%Y')}</time><span>{hero['readTime']} min de lectura</span></div><a class="button button-primary" href="{rel(depth,article_path(hero))}">Leer artículo <span aria-hidden="true">↗</span></a></div><a class="hero-art" href="{rel(depth,article_path(hero))}"><img src="{cover_path(hero)}" alt="{esc(hero.get('image_alt') or 'Imagen promocional relacionada con GTA VI')}" fetchpriority="high" width="1200" height="720"><span>REPORTAJE PRINCIPAL <b>01 / 06</b></span></a></section>
<section class="page-wrap secondary-stories" aria-label="Otras historias"><div class="section-kicker">HOY EN LEVELUP <span></span></div>{''.join(card(a,depth,True) for a in side)}</section>
<div class="page-wrap">{ad_slot("home_after_headlines")}</div>
{latest_block(ordered[:12],depth)}
{ranked_block(popular,depth)}
{gta_home_block(gta[:8],depth)}
{section_block("Anime", "Rankings, recomendaciones y guías para encontrar tu próxima serie.", anime[:8], depth, "anime-section", "anime/")}
{section_block("PlayStation", "Juegos, comparativas y partidas para PS5.", in_category("playstation")[:6], depth, "platform-section", "playstation/")}
{section_block("Xbox", "Aventuras, cooperativo y recomendaciones para el ecosistema Xbox.", in_category("xbox")[:6], depth, "platform-section", "xbox/")}
{section_block("PC Gaming", "Juegos, requisitos y recomendaciones para jugar en ordenador.", in_category("pc-gaming")[:6], depth, "platform-section", "pc-gaming/")}
{section_block("Nintendo", "Mundos, carreras y juegos para Switch y otras plataformas Nintendo.", in_category("nintendo")[:6], depth, "platform-section", "nintendo/")}
{section_block("Rankings", "Listas editoriales con criterios claros, contexto y fuentes.", rankings[:6], depth, "ranking-section", "rankings/")}
{section_block("Guías", "Consejos prácticos para elegir juegos, plataformas y equipo.", guides[:6], depth, "guide-section", "guias/")}
{section_block("Curiosidades", "Secretos, personajes y detalles del medio que merece la pena explorar.", [a for a in ordered if "curiosidades" in a["categories"] or "secreto" in a["slug"] or "iconicos" in a["slug"]][:6], depth, "curiosity-section", "rankings/")}
<div class="page-wrap">{ad_slot("home_mid")}</div>
{section_block("Descubre más", "Sigue explorando artículos nuevos de gaming, anime y entretenimiento.", more, depth, "discover-section", "videojuegos/")}
<section class="page-wrap newsletter-card"><div class="newsletter-mark"><span>LVL</span><b>UP</b></div><div><span class="eyebrow">NOVEDADES EDITORIALES</span><h2>Una buena recomendación empieza con contexto.</h2><p>Estamos preparando una selección editorial por correo. No pedimos tu dirección hasta tener el servicio y la política de privacidad configurados.</p></div><span class="newsletter-note">NEWSLETTER<br><b>PRÓXIMAMENTE</b></span></section>
</main>'''
    home_schema={"@context":"https://schema.org","@graph":[
        {"@type":"Organization","name":SITE["publisher"],"url":BASE_URL,"logo":BASE_URL+"/assets/images/logo.svg"},
        {"@type":"WebSite","name":SITE["name"],"url":BASE_URL+"/","potentialAction":{"@type":"SearchAction","target":BASE_URL+"/buscar/?q={search_term_string}","query-input":"required name=search_term_string"}}
    ]}
    return page_shell(SITE["name"]+" — Gaming, anime y entretenimiento", "Noticias, guías y rankings de videojuegos, anime, manga y tecnología. Todo lo que juega, importa.", "", SOCIAL_IMAGE, 0, body,home_schema,ads_eligible=True)

def section_block(title, desc, items, depth, extra="", more=""):
    link = f'<a class="text-link" href="{more}">Ver sección <span aria-hidden="true">↗</span></a>' if more else ""
    return f'''<section class="content-section page-wrap {extra}"><div class="section-heading"><div><span class="eyebrow">LECTURAS SELECCIONADAS</span><h2>{esc(title)}</h2><p>{esc(desc)}</p></div>{link}</div><div class="story-grid">{''.join(card(a,depth) for a in items)}</div></section>'''

def latest_block(items, depth):
    return f'''<section class="content-section page-wrap latest-feed"><div class="section-heading"><div><span class="eyebrow">ACTUALIDAD Y RECOMENDACIONES</span><h2>Últimas noticias</h2><p>12 artículos recientes para seguir lo que pasa en videojuegos, anime y cultura digital.</p></div><a class="text-link" href="buscar/">Buscar artículos ↗</a></div><div class="home-news-grid">{''.join(card(a,depth) for a in items)}</div></section>'''

def ranked_block(items, depth):
    rows=[]
    for position,item in enumerate(items,1):
        rows.append(f'''<article class="ranked-item"><span class="rank-number">{position:02d}</span>{cover_visual(item,depth,True,"rank-image")}<div><a class="category-label" href="{rel(depth,item['category']+'/')}">{esc(CATEGORIES[item['category']][0])}</a><h3><a href="{rel(depth,article_path(item))}">{esc(item['title'])}</a></h3><p>{esc(item['description'])}</p></div></article>''')
    return f'''<section class="content-section page-wrap popular-section"><div class="section-heading"><div><span class="eyebrow">SELECCIÓN DE REDACCIÓN</span><h2>Los más leídos</h2><p>10 recomendaciones editoriales; el orden no representa métricas de visitas.</p></div></div><div class="ranked-list">{''.join(rows)}</div></section>'''

def gta_home_block(items, depth):
    intro='GTA VI ya recorre Leonida. Descubre los detalles confirmados, personajes, mapa, vehículos, secretos y guías del nuevo mundo de Rockstar.'
    return f'''<section class="content-section page-wrap gta-feature-section"><div class="section-heading"><div><span class="eyebrow">DOSSIER ESPECIAL</span><h2>TODO SOBRE GTA VI</h2><p>{esc(intro)}</p></div><a class="button button-primary" href="{rel(depth,'gta-6/')}">Explorar GTA VI <span aria-hidden="true">↗</span></a></div><div class="gta-feature-grid">{''.join(card(a,depth) for a in items)}</div></section>'''

def category_page(slug):
    depth=1
    title,description=CATEGORIES[slug]
    items=[a for a in ARTICLES if slug in a["categories"]]
    items.sort(key=lambda x:(x["updated"],x["date"],x["slug"]),reverse=True)
    featured=items[0] if items else None
    crosslinks={
        "gta-6":["videojuegos","guias","rankings"],"videojuegos":["playstation","xbox","pc-gaming","nintendo"],
        "playstation":["videojuegos","xbox","guias"],"xbox":["videojuegos","playstation","pc-gaming"],
        "pc-gaming":["tecnologia","videojuegos","guias"],"nintendo":["videojuegos","anime","guias"],
        "anime":["manga","rankings","guias"],"manga":["anime","guias","rankings"],
        "rankings":["videojuegos","anime","gta-6"],"curiosidades":["videojuegos","gta-6","anime"],"guias":["videojuegos","tecnologia","gta-6"],
        "tecnologia":["pc-gaming","guias","videojuegos"]
    }
    recommended=items[1:4]
    latest=items[1:7]
    remaining=items[7:]
    gta_cluster_html=""
    if slug=="gta-6":
        clusters=defaultdict(list)
        for item in items:
            clusters[item.get("cluster", "GTA VI")].append(item)
        cluster_cards=[]
        for cluster,cluster_items in sorted(clusters.items(),key=lambda pair:pair[0].casefold()):
            links="".join(f'<li><a href="{rel(depth,article_path(item))}">{esc(item["title"])}</a></li>' for item in cluster_items)
            cluster_cards.append(f'<section class="gta-topic-card"><h3>{esc(cluster.title())}</h3><ul>{links}</ul></section>')
        gta_cluster_html=f'<section class="gta-topic-hub"><div class="listing-intro"><span class="eyebrow">DOSSIER GTA VI</span><h2>Guías y análisis por tema</h2><p>Atajos a las guías de juego, personajes, lugares de Leonida, vehículos, secretos y análisis. Las páginas distinguen hechos confirmados de teorías.</p></div><div class="gta-topic-grid">{"".join(cluster_cards)}</div></section>'
    related_categories="".join(f'<a class="topic-chip" href="{rel(depth,target+"/")}">{esc(CATEGORIES[target][0])}<span aria-hidden="true">↗</span></a>' for target in crosslinks.get(slug,[]) if target in CATEGORIES)
    feature=card(featured,depth) if featured else ""
    recommended_html="".join(f'<li><a href="{rel(depth,article_path(item))}">{esc(item["title"])}<span>↗</span></a></li>' for item in recommended)
    latest_html="".join(card(a,depth) for a in latest)
    more_html="".join(card(a,depth) for a in remaining)
    body=f'''<main id="contenido" class="page-wrap listing-page">{breadcrumbs([(title,None)],depth)}<header class="category-hero"><span class="eyebrow">PORTAL EDITORIAL / {len(items):02d} LECTURAS</span><h1>{esc(title)}</h1><p>{esc(description)}</p>{'<a class="button button-primary" href="'+rel(depth,article_path(featured))+'">Lectura destacada <span aria-hidden="true">↗</span></a>' if featured else ''}</header>{gta_cluster_html}<section class="category-portal"><div class="category-feature">{feature}</div><aside class="category-recommended"><span class="eyebrow">PARA SEGUIR LEYENDO</span><h2>Recomendados</h2><ol>{recommended_html}</ol></aside></section>{ad_slot("category_mid")}<section class="category-section"><div class="listing-intro"><span class="eyebrow">RECIÉN REVISADOS</span><h2>Últimas publicaciones</h2><p>Ordenadas por última actualización. Cada artículo muestra la fecha de revisión.</p></div><div class="story-grid">{latest_html}</div></section><section class="category-section"><div class="listing-intro"><span class="eyebrow">ARCHIVO EDITORIAL</span><h2>Todos los artículos de {esc(title)}</h2><p>Explora la biblioteca por tema y formato.</p></div><div class="story-grid" data-progressive-grid>{more_html}</div><button class="button button-quiet load-more" type="button" data-load-more hidden>Mostrar más artículos <span aria-hidden="true">↓</span></button></section><section class="category-links"><div class="listing-intro"><span class="eyebrow">EXPLORA MÁS</span><h2>Temas relacionados</h2></div><div class="topic-links">{related_categories}</div></section></main>'''
    schema={"@context":"https://schema.org","@graph":[{"@type":"CollectionPage","name":title,"description":description,"url":BASE_URL+"/"+slug+"/","mainEntity":{"@type":"ItemList","itemListElement":[{"@type":"ListItem","position":i+1,"url":BASE_URL+"/"+article_path(a)} for i,a in enumerate(items)]}},breadcrumb_schema([("Inicio",""),(title,slug+"/")])]}
    return page_shell(f"{title}: noticias y guías | LEVELUP DAILY",description,slug+"/",SOCIAL_IMAGE,depth,body,schema,ads_eligible=True)

def article_page(item):
    depth=2
    catlabel=CATEGORIES[item["category"]][0]
    path=article_path(item)
    cover=cover_path(item)
    image_alt=esc(item.get("image_alt") or f"Imagen relacionada con {item['title']}")
    image_caption=item.get("image_caption") or f"Imagen relacionada con {item['title']}."
    if item.get("image_source") and item.get("image_credit"):
        image_caption_html=f'{esc(image_caption)} <a href="{esc(item["image_source"])}" target="_blank" rel="noopener noreferrer">Fuente: {esc(item["image_credit"])}</a>'
    else:
        image_caption_html=esc(image_caption)
    if cover:
        cover_visual_html=f'<img src="{rel(depth,cover)}" alt="{image_alt}" width="1200" height="720" fetchpriority="high">'
    else:
        cover_visual_html=photo_request_block(image_request(item), "photo-request photo-request-cover")
        image_caption_html="Portada pendiente: consulta la lista de imágenes solicitadas para conocer la foto exacta."
    contents=[]
    sections=[]
    inline_media=item.get("inline_media",[])
    default_inline_index=max(1,min(2,len(item["sections"])))
    if not item.get("ranked_items") and not inline_media:
        default_filename=item.get("inline_photo_filename") or f"{item['slug']}-interior.webp"
        default_path="assets/images/inline/"+default_filename
        inline_media=[{"after_section":default_inline_index,"image":default_path if (ROOT/default_path).is_file() else None,"needed":image_request(item,"interior"),"filename":default_filename,"caption":f"Imagen relacionada con {item['title']}."}]
    def render_inline(media):
        image=media.get("image")
        if image and (ROOT/image).is_file():
            caption=media.get("caption", "Imagen relacionada con el artículo.")
            credit=media.get("credit")
            source=media.get("source")
            if credit and source:
                caption+=f' <a href="{esc(source)}" target="_blank" rel="noopener noreferrer">Fuente: {esc(credit)}</a>'
            return f'<figure class="article-inline-image"><img src="{rel(depth,image)}" alt="{esc(media.get("alt", "Imagen relacionada con el artículo"))}" loading="lazy" width="1200" height="675"><figcaption>{caption}</figcaption></figure>'
        label=media.get("needed") or f"FOTO INTERIOR — captura relacionada con «{item['title']}»."
        filename=media.get("filename", f"{item['slug']}-interior.webp")
        return f'<figure class="article-inline-image article-inline-pending" data-image-filename="{esc(filename)}">{photo_request_block(label, "photo-request photo-request-inline")}<figcaption>Imagen pendiente para esta sección · archivo sugerido: <code>{esc(filename)}</code></figcaption></figure>'
    inline_by_section=defaultdict(list)
    for media in inline_media:
        inline_by_section[int(media.get("after_section",default_inline_index))].append(media)
    for i,s in enumerate(item["sections"],1):
        sid=f"seccion-{i}"
        contents.append(f'<a href="#{sid}"><span>{i:02d}</span>{esc(s["title"])}</a>')
        section_html=f'<section id="{sid}" class="article-section"><h2>{esc(s["title"])}</h2><p>{esc(s["body"])}</p>'
        table=item.get("table")
        if table and i==item.get("table_after",1):
            table_html=f'<div class="editorial-table-wrap"><table class="editorial-table"><caption>{esc(table["caption"])}</caption><thead><tr>{"".join(f"<th scope=\"col\">{esc(head)}</th>" for head in table["headers"])}</tr></thead><tbody>{"".join("<tr>"+"".join(f"<td>{esc(cell)}</td>" for cell in row)+"</tr>" for row in table["rows"])}</tbody></table></div>'
            section_html+=table_html
        for media in inline_by_section.get(i,[]):
            section_html+=render_inline(media)
        sections.append(section_html+'</section>')
        if i == 1:
            sections.append(ad_slot("article_after_first_section"))
        if i==max(2,(len(item["sections"])+1)//2) and i<len(item["sections"]):
            sections.append(ad_slot("article_mid"))
    candidates=[]
    for candidate in ARTICLES:
        if candidate["slug"]==item["slug"]:
            continue
        shared=set(item["categories"]) & set(candidate["categories"])
        if shared:
            score=(5 if candidate["category"]==item["category"] else 0)+(3 if item["category"] in candidate["categories"] else 0)+len(shared)
            candidates.append((score,candidate))
    candidates.sort(key=lambda pair:(pair[0],pair[1]["updated"],pair[1]["slug"]),reverse=True)
    related=[candidate for _,candidate in candidates[:6]]
    if len(related)<3:
        related_ids={candidate["slug"] for candidate in related}
        related.extend(a for a in ARTICLES if a["slug"] not in related_ids and a["slug"]!=item["slug"] and a["category"]==item["category"])
        related=related[:6]
    category_articles=sorted((a for a in ARTICLES if item["category"] in a["categories"]),key=lambda a:(a["date"],a["slug"]))
    current_index=next(i for i,a in enumerate(category_articles) if a["slug"]==item["slug"])
    previous=category_articles[current_index-1] if current_index>0 else None
    following=category_articles[current_index+1] if current_index+1<len(category_articles) else None
    faqs="".join(f'<details class="faq-item"><summary>{esc(q)}</summary><p>{esc(ans)}</p></details>' for q,ans in item["faq"])
    spoiler_notice=f'<aside class="notice spoiler-warning"><strong>Aviso de spoilers.</strong> {esc(item["spoiler_warning"])}</aside>' if item.get("spoiler_warning") else ""
    sources="".join(f'<li><a href="{esc(url)}" target="_blank" rel="noopener noreferrer">{esc(label)} <span aria-hidden="true">↗</span></a></li>' for label,url in item.get("sources",[]))
    sourceblock=f'<section class="source-list"><h2>Fuentes y lecturas</h2><p>Consulta la fuente original cuando exista y su fecha; los anuncios, el catálogo y las guías de terceros pueden cambiar.</p><ul>{sources}</ul></section>' if sources else ""
    ranked_html=""
    if item.get("ranked_items"):
        ranked_rows=[]
        for position,entry in enumerate(item["ranked_items"],1):
            filename=entry.get("filename") or re.sub(r"[^a-z0-9]+","-",unicodedata.normalize("NFKD",entry["title"]).encode("ascii","ignore").decode().lower()).strip("-")+".webp"
            image=entry.get("image") or "assets/images/inline/rankings/"+filename
            if image and (ROOT/image).is_file():
                caption=esc(entry.get("image_caption", "Imagen del juego o serie."))
                if entry.get("image_source") and entry.get("image_credit"):
                    caption+=f' <a href="{esc(entry["image_source"])}" target="_blank" rel="noopener noreferrer">Foto: {esc(entry["image_credit"])}</a>'
                media=f'<figure class="ranked-guide-image"><img src="{rel(depth,image)}" alt="{esc(entry.get("image_alt", entry["title"]))}" loading="lazy" width="1200" height="675"><figcaption>{caption}</figcaption></figure>'
            else:
                media=f'<figure class="ranked-guide-image ranked-guide-pending" data-image-filename="{esc(filename)}">{photo_request_block(entry.get("photo_needed", "FOTO " + entry["title"].upper()), "photo-request photo-request-ranked")}<figcaption>Archivo sugerido: <code>{esc(filename)}</code></figcaption></figure>'
            ranked_rows.append(f'<li class="ranked-guide-entry"><span class="ranked-guide-number">{position:02d}</span><div class="ranked-guide-copy"><h3>{esc(entry["title"])}</h3><p>{esc(entry["body"])}</p>{media}</div></li>')
        ranked_html=f'<section class="ranked-guide-list"><div class="ranked-guide-heading"><span class="eyebrow">LISTA EDITORIAL</span><h2>TOP 10: {esc(item["title"])}</h2><p>Cada puesto incluye una imagen. El pie de foto indica si es una fotografía temática o material oficial del título.</p></div><ol>{"".join(ranked_rows)}</ol></section>'
    article_type=item.get("schema_type") or ("NewsArticle" if item["category"]=="gta-6" and "fecha" in item["title"].lower() else "BlogPosting")
    schema={"@context":"https://schema.org","@graph":[{"@type":article_type,"headline":item["title"],"description":item["description"],"image":[BASE_URL+"/"+(cover or SOCIAL_IMAGE)],"datePublished":item["date"],"dateModified":item["updated"],"author":{"@type":"Organization","name":SITE["author"]},"publisher":{"@type":"Organization","name":SITE["publisher"],"logo":{"@type":"ImageObject","url":BASE_URL+"/assets/images/logo.svg"}},"mainEntityOfPage":{"@type":"WebPage","@id":BASE_URL+"/"+path}},breadcrumb_schema([("Inicio",""),(catlabel,item["category"]+"/"),(item["title"],None)],BASE_URL+"/"+path)]}
    body=f'''<main id="contenido" class="page-wrap article-page">{breadcrumbs([(catlabel,item["category"]+"/"),(item["title"],None)],depth)}<div class="article-layout"><article class="article-main"><header class="article-header"><a class="category-label" href="{rel(depth,item['category']+'/')}">{esc(catlabel)}</a><h1>{esc(item['title'])}</h1><p class="article-dek">{esc(item['dek'])}</p><div class="byline"><span class="author-avatar">L</span><span><strong>{esc(SITE['author'])}</strong><small>Medio independiente · Contenido con fuentes</small></span><time datetime="{item['updated']}">Actualizado {date.fromisoformat(item['updated']).strftime('%d/%m/%Y')}</time><span>{item['readTime']} min</span></div><figure class="article-cover" data-cover="{esc(item['cover'])}">{cover_visual_html}<figcaption>{image_caption_html}</figcaption></figure></header><div class="article-prose"><p class="article-lead">{esc(item['intro'])}</p><div class="article-tools"><button type="button" data-share>Compartir artículo <span aria-hidden="true">↗</span></button><span data-reading-time>Lectura estimada: {item['readTime']} min</span></div><nav class="toc" aria-label="Índice del artículo"><details open><summary>En este artículo</summary><ol>{''.join(f'<li>{c}</li>' for c in contents)}</ol></details></nav><div class="article-content">{ranked_html}{''.join(sections)}<section class="article-section conclusion"><h2>En resumen</h2><p>{esc(item['conclusion'])}</p></section><section class="article-section faq-section"><h2>Preguntas frecuentes</h2>{faqs}</section>{sourceblock}</div><div class="article-share-bottom"><span>¿Te resultó útil esta guía?</span><button type="button" class="button button-quiet" data-share>Compartir</button></div></div></article><aside class="article-sidebar"><div class="sidebar-sticky"><div class="sidebar-card"><span class="eyebrow">SIGUE EXPLORANDO</span><h2>Más sobre {esc(catlabel)}</h2>{''.join(f'<a href="{rel(depth,article_path(a))}">{esc(a["title"])}<span>↗</span></a>' for a in related)}<a class="sidebar-more" href="{rel(depth,item['category']+'/')}">Ver todos los artículos <span>→</span></a></div></div></aside></div><section class="related-section"><div class="section-heading"><div><span class="eyebrow">SIGUIENTE NIVEL</span><h2>También te puede interesar</h2></div><a class="text-link" href="{rel(depth,item['category']+'/')}">Más de {esc(catlabel)} ↗</a></div><div class="story-grid">{''.join(card(a,depth) for a in related)}</div></section></main>'''
    body=body.replace(f'<p class="article-lead">{esc(item["intro"])}</p>',spoiler_notice+f'<p class="article-lead">{esc(item["intro"])}</p>')
    previous_next=f'''<nav class="article-neighbors" aria-label="Navegación entre artículos">{f'<a href="{rel(depth,article_path(previous))}"><span>← Anterior</span><strong>{esc(previous["title"])}</strong></a>' if previous else '<span></span>'}{f'<a class="next-article" href="{rel(depth,article_path(following))}"><span>Siguiente →</span><strong>{esc(following["title"])}</strong></a>' if following else '<span></span>'}</nav>'''
    body=body.replace('</div></div></article><aside class="article-sidebar">','</div></div>'+previous_next+'</article><aside class="article-sidebar">')
    return page_shell(item.get("seo_title",item["title"]+" | LEVELUP DAILY"),item["description"],path,cover or SOCIAL_IMAGE,depth,body,schema,ads_eligible=True)

def build_search_index():
    return [{"title":a["title"],"description":a["description"],"category":CATEGORIES[a["category"]][0],"categoryUrl":a["category"]+"/","url":article_path(a),"image":cover_path(a) or "","coverRequest":image_request(a),"updated":a["updated"],"readTime":a["readTime"],"text":" ".join([a["title"],a["description"],a["dek"],a["intro"],*[CATEGORIES[c][0] for c in a["categories"]],*[s["title"]+" "+s["body"] for s in a["sections"]],*[entry["title"]+" "+entry["body"] for entry in a.get("ranked_items",[])],*sum(a.get("table",{}).get("rows",[]),[])])} for a in ARTICLES]

def search_page(search_index):
    depth=1
    schema={"@context":"https://schema.org","@graph":[{"@type":"WebPage","name":"Buscar | LEVELUP DAILY","url":BASE_URL+"/buscar/"},breadcrumb_schema([("Inicio",""),("Buscar","buscar/")])]}
    inline_index=json.dumps(search_index,ensure_ascii=False,separators=(",",":")).replace("<","\\u003c").replace(">","\\u003e").replace("&","\\u0026")
    body=f'''<main id="contenido" class="page-wrap search-page">{breadcrumbs([("Buscar",None)],depth)}<header class="listing-intro"><span class="eyebrow">BUSCADOR EDITORIAL</span><h1>Buscar en LEVELUP DAILY</h1><p>Encuentra noticias, artículos, guías y rankings. La búsqueda se ejecuta en tu navegador y también funciona sin servidor.</p><form class="search-form search-form-large" id="results-search" action="./index.html" method="get" role="search"><label class="sr-only" for="results-q">Buscar artículos</label><input id="results-q" name="q" type="search" placeholder="Ej. mapa GTA VI, anime…"><button class="button button-primary" type="submit">Buscar <span aria-hidden="true">⌕</span></button></form></header><p class="search-status" id="search-status" aria-live="polite">Preparando el índice editorial…</p><div class="story-grid" id="search-results"></div><noscript><p>Activa JavaScript para filtrar el índice local de artículos.</p></noscript></main><script type="application/json" id="search-data">{inline_index}</script><script defer src="{rel(depth,'assets/js/search.js')}"></script>'''
    return page_shell("Buscar artículos | LEVELUP DAILY","Busca en el índice de noticias, guías, artículos y rankings de LEVELUP DAILY.","buscar/",SOCIAL_IMAGE,depth,body,schema,True)

def legal_page(slug, data):
    title,description,content=data
    depth=1
    email=str(SITE["contact_email"])
    replacements={
        "[PENDIENTE: nombre del titular]":str(SITE["owner"]),
        "[PENDIENTE: empresa, si procede]":str(SITE["company"]),
        "[PENDIENTE: empresa]":str(SITE["company"]),
        "[PENDIENTE: NIF]":str(SITE["tax_id"]),
        "[PENDIENTE: domicilio]":str(SITE["address"]),
        "[PENDIENTE: correo de contacto]":email,
        "[PENDIENTE: correo para privacidad]":email,
        "[PENDIENTE: dominio]":str(SITE["domain"]),
        "[PENDIENTE: dominio definitivo]":str(SITE["domain"]),
        "mailto:PENDIENTE":"mailto:"+email.replace(" ","%20"),
    }
    for marker,value in replacements.items():
        content=content.replace(marker,esc(value))
    body=f'''<main id="contenido" class="page-wrap legal-page">{breadcrumbs([(title,None)],depth)}<header class="category-hero"><span class="eyebrow">INFORMACIÓN DEL SITIO</span><h1>{esc(title)}</h1><p>{esc(description)}</p></header><article class="legal-content">{content}<p class="legal-updated">Página preparada el {date.today().strftime('%d/%m/%Y')}. Completa la información pendiente antes de publicar.</p></article></main>'''
    schema={"@context":"https://schema.org","@graph":[{"@type":"WebPage","name":title,"description":description,"url":BASE_URL+"/"+slug+"/"},breadcrumb_schema([("Inicio",""),(title,slug+"/")])]}
    return page_shell(title+" | LEVELUP DAILY",description,slug+"/",SOCIAL_IMAGE,depth,body,schema,noindex=not legal_page_is_indexable(slug))

def _configured_site_value(value) -> bool:
    text = str(value or "").strip().casefold()
    return bool(text and not any(marker in text for marker in ("pendiente", "xxxxxxxx", "example.com", "tu-usuario")))

def legal_page_is_indexable(slug: str) -> bool:
    required_fields = {
        "sobre-nosotros": ("owner", "contact_email"),
        "contacto": ("contact_email",),
        "politica-de-privacidad": ("owner", "tax_id", "address", "contact_email", "domain"),
        "aviso-legal": ("owner", "tax_id", "address", "contact_email", "domain"),
    }.get(slug, ())
    return all(_configured_site_value(SITE.get(field)) for field in required_fields)

def validate_search_console_config() -> None:
    token = str(SITE.get("google_search_console_verification", "")).strip()
    if token and (not re.fullmatch(r"[A-Za-z0-9_-]{10,}", token) or any(marker in token.casefold() for marker in ("pendiente", "xxxxxxxx", "example"))):
        raise ValueError("google_search_console_verification debe ser el contenido real de la etiqueta HTML de Search Console, sin etiquetas ni texto de ejemplo.")

def build_sitemap(urls) -> str:
    ET.register_namespace("", "http://www.sitemaps.org/schemas/sitemap/0.9")
    namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    root = ET.Element(namespace + "urlset")
    seen = set()
    for route, lastmod in urls:
        url = BASE_URL + "/" + route.lstrip("/")
        if url in seen:
            raise ValueError("Duplicate sitemap URL: " + url)
        if not url.startswith("https://") or urlparse(url).netloc != _base_parts.netloc or "?" in url or "#" in url:
            raise ValueError("Invalid sitemap URL: " + url)
        target = ROOT / (Path(route.strip("/")) / "index.html" if route else "index.html")
        if not target.is_file():
            raise ValueError("Sitemap route has no generated page: " + route)
        page = target.read_text(encoding="utf-8")
        if 'name="robots" content="index,follow,max-image-preview:large"' not in page:
            raise ValueError("Non-indexable page included in sitemap: " + route)
        entry = ET.SubElement(root, namespace + "url")
        ET.SubElement(entry, namespace + "loc").text = url
        if lastmod:
            ET.SubElement(entry, namespace + "lastmod").text = lastmod
        seen.add(url)
    output = ET.tostring(root, encoding="utf-8", xml_declaration=True).decode("utf-8") + "\n"
    ET.fromstring(output)
    return output

def not_found_page():
    body='''<main id="contenido" class="page-wrap error-page"><span class="eyebrow">ERROR 404</span><h1>Esta página se ha perdido en el mapa.</h1><p>Puede que el enlace haya cambiado. Vuelve al inicio o encuentra otro tema en el buscador.</p><a class="button button-primary" href="./index.html">Volver a LEVELUP DAILY</a><a class="text-link" href="./buscar/index.html">Buscar artículos ↗</a></main>'''
    page=page_shell("Página no encontrada | LEVELUP DAILY","No encontramos esta página. Vuelve a la portada o busca un artículo.","404.html",SOCIAL_IMAGE,0,body,noindex=True)
    if not PUBLIC_SITE:
        return page
    base_path=urlparse(BASE_URL).path.strip("/")
    base=("/"+base_path+"/") if base_path else "/"
    return page.replace("<head>",f'<head><base href="{esc(base)}">',1)

def write_page(route, content):
    target=ROOT/route
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(content,encoding="utf-8")

def build_image_manifest() -> str:
    requests={}
    def add(filename, target, description, article, group):
        entry=requests.setdefault(filename,{"target":target,"description":description,"group":group,"articles":set()})
        entry["articles"].add(article)
    for item in ARTICLES:
        if not cover_path(item):
            filename=f"{item['cover']}.webp"
            add(filename,"assets/images/covers/"+filename,image_request(item),item["title"],"Portadas")
        if item.get("ranked_items"):
            for entry in item["ranked_items"]:
                filename=entry.get("filename") or re.sub(r"[^a-z0-9]+","-",unicodedata.normalize("NFKD",entry["title"]).encode("ascii","ignore").decode().lower()).strip("-")+".webp"
                image=entry.get("image") or "assets/images/inline/rankings/"+filename
                if image and (ROOT/image).is_file():
                    continue
                label=entry.get("photo_needed") or "FOTO " + entry["title"].upper()
                add(filename,"assets/images/inline/rankings/"+filename,label,item["title"]+" · "+entry["title"],"Imágenes de los TOP 10")
        else:
            media=item.get("inline_media")
            if not media:
                filename=item.get("inline_photo_filename") or f"{item['slug']}-interior.webp"
                candidate=ROOT/"assets"/"images"/"inline"/filename
                if candidate.is_file():
                    continue
                media=[{"needed":image_request(item,"interior"),"filename":filename}]
            for image in media:
                if image.get("image") and (ROOT/image["image"]).is_file():
                    continue
                filename=image.get("filename") or f"{item['slug']}-interior.webp"
                label=image.get("needed") or f"FOTO INTERIOR — imagen relacionada con «{item['title']}»."
                add(filename,"assets/images/inline/"+filename,label,item["title"],"Imágenes interiores de artículos")
    if not requests:
        return "# Imágenes pendientes para LEVELUP DAILY\n\nNo quedan imágenes pendientes: todos los artículos tienen portada e imagen interior y cada puesto de los rankings tiene una ficha visual propia. La procedencia, licencia y hashes están en `assets/images/image-credits.json`; el detalle de asignaciones está en `IMAGE-AUDIT.md`.\n"
    groups=("Portadas","Imágenes de los TOP 10","Imágenes interiores de artículos")
    lines=["# Imágenes pendientes para LEVELUP DAILY","","Descarga o prepara estas fotografías/capturas y guárdalas en la ruta indicada. Cada petición aparece también en su artículo como una ficha «FOTO PENDIENTE». Las imágenes deben corresponder al juego, anime o tema exacto; evita dibujos abstractos y conserva el crédito/licencia del titular.","","**Formato recomendado:** WebP, 1200 × 675 px o superior para imágenes horizontales. Respeta recortes verticales cuando la imagen original lo requiera.",""]
    for group in groups:
        entries=sorted(((name,data) for name,data in requests.items() if data["group"]==group),key=lambda pair:pair[0].casefold())
        if not entries:
            continue
        lines.extend([f"## {group} ({len(entries)})","", "| Archivo | Qué imagen hace falta | Se usa en | Ruta de destino |","|---|---|---|---|"])
        for name,data in entries:
            places="; ".join(sorted(data["articles"],key=str.casefold))
            lines.append(f"| `{name}` | {data['description'].replace('|','\\|')} | {places.replace('|','\\|')} | `{data['target']}` |")
        lines.append("")
    lines.extend([f"**Total de imágenes pendientes:** {len(requests)}.","","Consulta `IMAGE-AUDIT.md` y `assets/images/image-credits.json` para revisar procedencia, licencia y estado antes de publicar o monetizar una imagen.",""])
    return "\n".join(lines)

def main():
    validate_adsense_config(SITE, ROOT)
    validate_search_console_config()
    if adsense_mode(SITE) == "active" and not PUBLIC_SITE:
        raise ValueError("AdSense active requiere un dominio HTTPS real; el build local seguirá sin etiquetas publicitarias.")
    # Validate internal taxonomy and article routes before writing generated pages.
    seen=set()
    seen_titles=set()
    for item in ARTICLES:
        if item["slug"] in seen:
            raise ValueError("Duplicate article slug: "+item["slug"])
        seen.add(item["slug"])
        title_key=re.sub(r"\s+"," ",item["title"].strip().casefold())
        if title_key in seen_titles:
            raise ValueError("Duplicate article title: "+item["title"])
        seen_titles.add(title_key)
        if item["category"] not in CATEGORIES:
            raise ValueError("Unknown primary category: "+item["category"])
        unknown_categories=set(item["categories"])-set(CATEGORIES)
        if unknown_categories:
            raise ValueError("Unknown article categories: "+", ".join(sorted(unknown_categories))+" in "+item["slug"])
        if not item["sections"] or not item["faq"]:
            raise ValueError("Article missing sections or FAQ: "+item["slug"])
        editorial_text=[item["title"],item["dek"],item["intro"],item["conclusion"]]
        editorial_text.extend(section["title"]+" "+section["body"] for section in item["sections"])
        editorial_text.extend(question+" "+answer for question,answer in item["faq"])
        word_count=sum(len(re.findall(r"\b[\wÁÉÍÓÚÜÑáéíóúüñ]+\b",text)) for text in editorial_text)
        item["readTime"]=max(1,(word_count+209)//210)
        for _, url in item.get("sources", []):
            if urlparse(url).scheme != "https":
                raise ValueError("Source must use HTTPS: "+url)

    ads_txt_status=sync_ads_txt(ROOT,SITE) if PUBLIC_SITE else "sin generar: dominio público aún no configurado"
    legacy_image_meta=remember_legacy(ROOT,ARTICLES,RANKED_ITEMS,INLINE_MEDIA)
    stock_credits=json.loads((ROOT/"assets/images/stock/credits.json").read_text(encoding="utf-8"))
    write_audit(ROOT,ARTICLES,legacy_image_meta,stock_credits,date.today().isoformat())
    search_index=build_search_index()
    (ROOT/"assets/images/covers").mkdir(parents=True,exist_ok=True)
    (ROOT/"LISTA_IMAGENES_PENDIENTES.md").write_text(build_image_manifest(),encoding="utf-8")
    write_page("index.html",home_page())
    for slug in CATEGORIES:
        write_page(f"{slug}/index.html",category_page(slug))
    for item in ARTICLES:
        write_page(article_path(item)+"index.html",article_page(item))
    for slug,data in LEGAL.items():
        write_page(f"{slug}/index.html",legal_page(slug,data))
    write_page("buscar/index.html",search_page(search_index))
    write_page("404.html",not_found_page())

    (ROOT/"assets/data").mkdir(parents=True,exist_ok=True)
    (ROOT/"assets/data/search-index.json").write_text(json.dumps(search_index,ensure_ascii=False,separators=(",",":")),encoding="utf-8")

    urls=[("",None)]+[(slug+"/",None) for slug in CATEGORIES]+[(article_path(a),a["updated"]) for a in ARTICLES]+[(slug+"/",None) for slug in LEGAL if legal_page_is_indexable(slug)] if PUBLIC_SITE else []
    sitemap=build_sitemap(urls)
    (ROOT/"sitemap.xml").write_text(sitemap,encoding="utf-8")
    robots=(f"User-agent: *\nAllow: /\nDisallow: /content/\nDisallow: /scripts/\nDisallow: /assets/data/\nSitemap: {BASE_URL}/sitemap.xml\n" if PUBLIC_SITE else "User-agent: *\nDisallow: /\n")
    (ROOT/"robots.txt").write_text(robots,encoding="utf-8")
    ads_report=audit_generated_site(ROOT,SITE)
    if ads_report["errors"]:
        raise RuntimeError("AdSense preflight no superado:\n- "+"\n- ".join(ads_report["errors"]))
    print(f"Built {len(ARTICLES)} articles, {len(CATEGORIES)} category pages, {len(LEGAL)} information pages.")
    print("Public domain configured: "+("yes" if PUBLIC_SITE else "no; local build marked noindex"))
    print(f"AdSense preflight: {ads_report['pages']} HTML, mode={ads_report['mode']}, {ads_report['units']} active units, {ads_report['slots']} reserved slots.")
    print(f"ads.txt: {ads_txt_status}.")

if __name__ == "__main__":
    main()
