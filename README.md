# LEVELUP DAILY

Medio digital estático en español sobre videojuegos, anime, manga y cultura digital. El sitio se genera como HTML, CSS y JavaScript y se despliega en GitHub Pages sin backend ni base de datos.

## Abrir la web en el ordenador

Abre `index.html` con doble clic. La portada, categorías, artículos, imágenes, estilos y buscador están guardados en esta carpeta y funcionan sin iniciar un servidor ni instalar nada. Para mover o compartir la versión local, conserva juntas la carpeta `assets`, las carpetas de categorías y el archivo `index.html`.

La versión que se abre con `file://` funciona en el ordenador, pero Google no puede rastrearla como una web pública. `site.json` ya está configurado con la URL prevista de GitHub Pages: `https://ascendsystem.github.io/levelup-daily`. La web solo será pública cuando GitHub Pages acepte un despliegue correcto.

## Publicar en GitHub Pages

1. Si vas a usar un dominio propio, cambia `base_url` en `site.json` por la URL canónica HTTPS, sin barra final. Completa los datos reales del titular antes de indexar las páginas informativas.
2. Ejecuta `python scripts/build.py` desde la raíz. El generador crea portada, categorías, artículos, páginas informativas, sitemap, robots e índice de búsqueda. La salida local continúa funcionando con doble clic.
3. En el repositorio, activa GitHub Pages desde **Settings → Pages → Build and deployment → GitHub Actions**.
4. Sube los cambios a `main`. El workflow `.github/workflows/pages.yml` compila y audita la web antes de desplegarla.
5. Comprueba en **Actions** que el trabajo de construcción y el despliegue hayan terminado correctamente. La URL prevista para este repositorio es `https://ascendsystem.github.io/levelup-daily/`.

## Publicar un artículo

Edita `content/articles.json` o `content/additional-articles.json`. Cada objeto necesita `slug`, `category`, `categories`, `title`, `description`, `dek`, fechas ISO, portada, introducción, secciones, conclusión, preguntas frecuentes y fuentes. `category` determina la carpeta de URL. Contrasta fechas y cifras, y enlaza fuentes primarias para los anuncios o datos que cambian.

Las imágenes originales de los artículos existentes se conservan. Añadí 68 fotos de la carpeta local de GTA VI a 34 artículos nuevos, con sus créditos y ruta de procedencia; el artículo sobre Little Sam queda con dos espacios pendientes de evidencia específica. Los cinco TOP 10 conservan sus imágenes actuales. Los archivos de `pinterest`, ImageAssistant, Valorant y anime no se reasignaron a artículos existentes. `IMAGE-AUDIT.md` registra las imágenes conservadas, las coincidencias anteriores y lo pendiente; `assets/images/image-credits.json` contiene fuentes y hashes. Las imágenes oficiales de GTA quedan sujetas a confirmar permiso comercial antes de publicar con anuncios.

## SEO y analítica

- `base_url` apunta a la URL prevista de GitHub Pages para que canonical, Open Graph, sitemap y robots utilicen el mismo origen. Confirma la URL servida tras el primer despliegue; las páginas legales con datos pendientes siguen marcadas `noindex`.
- Para una propiedad URL-prefix de Search Console, copia el valor real de `google-site-verification` a `google_search_console_verification` en `site.json`. Para una propiedad Domain, verifica el dominio mediante el registro TXT que Google muestre en su asistente; no inventes el token.
- Cada artículo genera una URL estática, título, descripción, canonical, tarjetas sociales, fecha, enlaces internos y schema `BlogPosting`.
- `sitemap.xml` público incluye la portada, categorías, artículos y páginas informativas indexables. Excluye búsqueda, 404 y páginas legales que aún tienen datos obligatorios pendientes. La copia local produce un XML vacío válido y un `robots.txt` que bloquea el rastreo.
- Verifica el dominio en Google Search Console y envía el sitemap público.
- Google Analytics está desactivado. No actives etiquetas hasta configurar privacidad y consentimiento.
- Google AdSense está en `off`; no se ha inventado ni activado ningún ID. La arquitectura, los modos de revisión/activación y los pasos de mantenimiento están en `ADSENSE-MAINTENANCE.md`.

## Bloqueadores de anuncios y espacios publicitarios

Los espacios para anuncios se dejan vacíos. El detector local solo se ejecuta cuando hay una unidad real de AdSense activa; con la configuración actual no hay anuncios ni bloqueo de lectura por tener un bloqueador. Si más adelante se insertan anuncios, la barrera local puede dar falsos positivos y no sustituye al sistema oficial de recuperación de Google.

Para usar la recuperación oficial de AdSense en una versión publicada, configura primero el mensaje y la etiqueta de recuperación específicos de tu cuenta. Google explica el proceso en [Recuperación de bloqueadores de anuncios](https://support.google.com/adsense/answer/11576085?hl=es-ES). Para configurarlo:

1. En AdSense, abre **Privacidad y mensajería → Recuperación de bloqueadores de anuncios** y crea un mensaje para el sitio.
2. Elige **modal centrado (no descartable)** si quieres que la lectura espere hasta que la persona permita los anuncios.
3. Publica el mensaje y copia el código de recuperación que AdSense genera en `content/adsense-recovery-tag.html`.
4. Copia también el código de protección frente a errores de bloqueo en `content/adsense-error-protection.html`.
5. Sigue `ADSENSE-MAINTENANCE.md` para confirmar el Publisher ID, CMP y modo antes de publicar. La integración y las etiquetas de recuperación permanecen apagadas en `off`; `active` exige además unidades reales y la CMP verificada.

La etiqueta es específica de la cuenta y del sitio; no se debe inventar. Google puede ofrecer también una alternativa de apoyo y la experiencia exacta se administra desde AdSense. El estado y los pasos pendientes están en `ADSENSE-AUDIT.md`.

## Privacidad, newsletter y publicidad

El aviso actual almacena una elección local, pero no es una CMP certificada ni una garantía legal. Las etiquetas de analítica y anuncios están desactivadas. Antes de integrar AdSense u otros servicios, instala una CMP compatible, actualiza las políticas y verifica que las etiquetas respeten la elección aplicable. Google exige una CMP certificada e integrada con TCF para los anuncios personalizados en el EEE, Reino Unido y Suiza.

Para añadir contenido sin duplicar etiquetas, consulta [ADSENSE-MAINTENANCE.md](ADSENSE-MAINTENANCE.md). El build centraliza los espacios y ejecuta las comprobaciones de marcado con `python scripts/check_adsense.py`.

Las páginas legales contienen campos pendientes. Completa titular, empresa, NIF, domicilio, correo y dominio; revisa los textos para España antes de publicar. El formulario de contacto valida en el navegador pero no envía ni almacena nada: configura primero un servicio receptor y actualiza la política de privacidad. La newsletter es informativa y no recoge direcciones.

## Estructura

- `content/articles.json` y `content/additional-articles.json`: contenido editorial.
- `content/expansions.json` y `content/final-sections.json`: secciones ampliadas de artículos.
- `content/adsense-recovery-tag.html` y `content/adsense-error-protection.html`: código de AdSense pendiente de la cuenta del titular.
- `content/adsense-cmp.html` y `content/adsense-cmp-preferences.html`: integración y control de preferencias pendientes de la CMP elegida.
- `scripts/adsense.py` y `scripts/check_adsense.py`: configuración central, renderizado, `ads.txt` y preflight de ubicaciones.
- `content/gta-launch-guides.json`: guías nuevas de lanzamiento de GTA VI y Valorant.
- `content/gta-music-23-nov.json`: noticias y guías recientes sobre el álbum Deluxe y las emisoras de GTA VI.
- `content/gta-deep-dive-articles.json`: 35 guías nuevas de GTA VI con fuentes, FAQs y etiquetas de cluster.
- `scripts/author_gta_expansion.py`: genera y valida el lote de guías nuevas.
- `scripts/import_gta_downloads.py`: asignación de fotos GTA aportadas por el usuario sin reemplazar las imágenes anteriores.
- `scripts/image_audit.py`: créditos, hashes y auditoría de imágenes repetidas.
- `scripts/audit_generated.py`: control de artículos, H1, imágenes de portada/interior, rutas locales, enlaces, SEO local y duplicados.
- `IMAGE-AUDIT.md`, `ADSENSE-AUDIT.md` y `ADSENSE-MAINTENANCE.md`: auditoría visual/publicitaria y manual de mantenimiento.
- `content/ranked-entries.json` y `content/inline-media.json`: fotografías para los rankings y el interior de cada artículo.
- `assets/images/stock/credits.json`: autores, páginas de origen y licencia de las fotos de Pexels.
- `scripts/build.py`: generador estático.
- `LAUNCH-AUDIT.md`, `SEO-AUDIT.md` y `ADSENSE-AUDIT.md`: estado real de lanzamiento, indexación y monetización.
- `assets/css/`: estilos de escritorio y responsive.
- `assets/js/`: menú, consentimiento inicial, compartir, carga progresiva y buscador.
- `assets/data/search-index.json`: índice de búsqueda generado.
- `.github/workflows/pages.yml`: despliegue de GitHub Pages.

## Requisitos

Python 3 para regenerar. El contenido se sirve como archivos estáticos. El buscador y el menú requieren JavaScript; los artículos permanecen en el HTML para que se puedan leer e indexar sin una API.
