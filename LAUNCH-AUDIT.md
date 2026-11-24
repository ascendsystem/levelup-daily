# Auditoría de lanzamiento — LEVELUP DAILY

Revisión previa al primer push: 24 de noviembre de 2026. Esta sección registra las comprobaciones previas; no afirma que exista ya un despliegue público.

## 1. Dominio propio, GitHub Pages y HTTPS

**Estado: PENDIENTE DE ACTIVAR GITHUB PAGES Y DEL PRIMER DESPLIEGUE**

- El workflow `.github/workflows/pages.yml` está preparado para publicar desde `main` usando GitHub Actions. Ejecuta el build y la auditoría antes de crear el artefacto; copia `ads.txt` solo con Publisher ID confirmado.
- La API pública confirma que `main` es la rama predeterminada, pero el repositorio todavía no tiene ramas ni commits. La API de GitHub Pages responde 404, así que Pages aún no está habilitado y no hay despliegue que comprobar.
- `site.json` ya apunta a la URL prevista del proyecto: `https://ascendsystem.github.io/levelup-daily`. No se ha configurado dominio propio ni hay archivo `CNAME`.
- **Pendiente antes del primer despliegue:** en **Settings → Pages → Build and deployment**, elegir **GitHub Actions** como origen. Después del push, comprobar el workflow y la URL pública servida.

## 2. Google Search Console

**Estado: PENDIENTE DEL USUARIO**

- Añadí el campo vacío `google_search_console_verification` a `site.json`. El build, si se configura con el valor real, inserta la meta etiqueta solo en la portada. La prueba aislada verificó ubicación y formato sin guardar un token.
- No hay cuenta, propiedad, token ni verificación disponibles en este proyecto.
- **Para continuar:** crea una propiedad Domain y añade en tu proveedor DNS el registro TXT exacto que te muestre Google (nombre/host y valor indicados por el asistente, TTL predeterminado). O crea propiedad URL-prefix y copia solo el valor `content` de la meta etiqueta que te proporcione Google a `google_search_console_verification`. Publica y pulsa «Verificar». No se ha marcado como verificada. Google explica los métodos en [verificar la propiedad del sitio](https://support.google.com/webmasters/answer/9008080?hl=es).

## 3. `sitemap.xml`

**Estado: COMPLETADO EN EL GENERADOR LOCAL**

- El sitemap se regenera desde los datos fuente. Con la URL objetivo configurada, el build local produce 127 URLs absolutas HTTPS únicas con archivos presentes e indexables: inicio, 12 categorías, 112 artículos y 2 páginas informativas.
- Búsqueda, 404 y cuatro páginas legales con datos obligatorios incompletos quedan fuera. Esas cuatro páginas llevan `noindex` hasta que se completen.
- Tras configurar el dominio, se debe revisar la URL publicada y enviarla en Search Console. Google trata el sitemap como una señal de descubrimiento, no como garantía de indexación: [documentación de sitemaps](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap?hl=es).

## 4. `robots.txt`

**Estado: COMPLETADO EN EL GENERADOR LOCAL**

- El archivo generado para la URL objetivo permite el rastreo general, mantiene CSS/JS/imágenes accesibles y declara el sitemap absoluto. No se ha podido verificar todavía la respuesta servida por GitHub Pages.
- **Pendiente tras desplegar:** abrir `https://ascendsystem.github.io/levelup-daily/robots.txt` y comprobar el contenido. Google distingue robots (rastreo) de `noindex` (indexación): [introducción a robots.txt](https://developers.google.com/search/docs/crawling-indexing/robots/intro?hl=es).

## 5. Auditoría de artículos (muestra de 30)

**Estado: PENDIENTE DEL USUARIO PARA CIERRE EDITORIAL**

Se revisaron estructura, título y descripción, fecha, fuentes, imagen y navegación de 25 artículos de GTA VI y cinco de otras categorías. La extensión resultó de 516–790 palabras en la muestra; todos tenían imágenes asignadas, alt, H1 único y enlaces internos; las descripciones no se repitieron. La revisión no sustituye una prueba de juego por la redacción.

Muestra GTA VI:

- `todo-sobre-gta-6`, `mapa-gta-6`, `personajes-gta-6`, `novedades-gta-6-frente-gta-5`, `gta-6-ps5-xbox`, `gta-6-pc`, `traileres-gta-6-detalles`, `lugares-identificados-gta-6`, `precio-ediciones-gta-6`, `preguntas-frecuentes-gta-6`, `vice-city-gta-6`, `vehiculos-gta-6`, `actividades-misiones-gta-6`, `mundo-abierto-gta-6`, `animales-fauna-gta-6`, `trucos-gta-6-codigos`, `lugares-secretos-gta-6`, `ganar-dinero-gta-6`, `robos-gta-6-guia`, `guardar-partida-gta-6`, `consejos-primeras-horas-gta-6`, `misiones-gta-6-capitulos`, `accesibilidad-gta-6-ajustes`, `descubrimientos-gta-6-primeros-dias`, `actualizacion-gta-6-23-noviembre`.

Muestra de otras categorías:

- `mejores-juegos-ps5`, `mejores-juegos-mundo-abierto-pc`, `videojuegos-esperados-proximos-meses`, `mejores-juegos-gratis`, `mejores-juegos-para-jugar-con-amigos`.

Comprobaciones de hechos hechas contra fuentes oficiales en esta muestra: Rockstar confirma disponibilidad mundial el 19/11/2026 para PS5 y Xbox Series X|S ([Newswire](https://www.rockstargames.com/newswire/article/39akk424a9oo53/grand-theft-auto-vi-now-available)); su soporte lista las plataformas y ediciones ([soporte de Rockstar](https://support.rockstargames.com/articles/4QfG4FmZCf5W1gS8jy4UVT/grand-theft-auto-vi-platform-editions-and-versions)); y la nota del 23/11 registra siete arreglos ([actualizaciones de lanzamiento](https://support.rockstargames.com/articles/sN5pEdFYZdlvijKXd6xpJ/grand-theft-auto-vi-launch-updates-ps5-xbox-series-x-or-s)). Detecté una discrepancia entre PC Gamer y PowerPyx sobre el reto de Munición máxima (20 frente a 25 medallas de bronce); `trucos-gta-6-codigos` ahora la atribuye de forma explícita y recomienda confirmar el requisito dentro del juego. Los conteos y códigos de trucos/misiones proceden de guías de terceros, no de Rockstar, y deben volver a revisarse cuando cambien.

Quedan pendientes una revisión de originalidad/voz por una persona responsable, contrastar guías con la partida comercial, comprobar fuentes externas al publicar y actualizar noticias volátiles. `secretos-y-easter-eggs-videojuegos` es una guía editorial general sin enlaces externos; no introduce una cifra ni una función específica de juego. Ver también `SEO-AUDIT.md`.

## 6. Imágenes y derechos

**Estado: PENDIENTE DEL USUARIO**

- `IMAGE-AUDIT.md` y `assets/images/image-credits.json` registran 174 archivos; 168 están asignados. El build comprobó que cargan localmente, registró SHA-256/pHash, dimensiones, alt text y repeticiones. Los 168 raster asignados miden al menos 1067 × 720 px (mínimos independientes), ninguno baja de 640 × 360 px.
- 17 duplicados exactos y 24 coincidencias pHash detectados en el archivo local; hay 32 archivos compartidos entre artículos y 37 grupos SHA-256 compartidos. Se conservaron las asignaciones previas y no se eliminaron archivos.
- Una portada y una foto interior siguen pendientes para `gta-6-easter-egg-little-sam` (2 recursos). No se confirmó visualmente si cada archivo tiene marca de agua.
- 151 asignaciones conservan derechos sin verificar; las fechas de descarga están ausentes. Los 18 registros Pexels tienen autor, URL y referencia a la licencia, que permite uso web bajo sus términos y mantiene restricciones ([Pexels License](https://www.pexels.com/license/)). Las imágenes de Rockstar/Riot y las de origen desconocido requieren autorización o base de uso revisada antes de monetizar.

## 7. Sobre nosotros

**Estado: PENDIENTE DEL USUARIO**

- `/sobre-nosotros/` existe y explica el enfoque, formatos y política editorial sin inventar autores ni experiencia.
- Los campos de titular/empresa/contacto siguen siendo marcadores. El generador deja la página `noindex` mientras falten titular y correo configurado.
- Completa identidad real y revisa el texto antes de indexar/publicar.

## 8. Contacto

**Estado: PENDIENTE DEL USUARIO**

- `/contacto/` tiene formulario visual con nombre, correo, asunto y mensaje, campos requeridos, validación nativa y estado accesible.
- El botón valida solamente; el mensaje indica claramente que no se envió. No hay endpoint, servidor, almacenamiento ni correo real. Falta elegir y configurar receptor y política de privacidad.
- El correo sigue pendiente y la página queda `noindex` hasta configurarlo. No introduje un servicio o email ficticio.

## 9. Aviso legal y privacidad

**Estado: PENDIENTE DEL USUARIO**

- Existen Aviso legal y Política de privacidad con secciones sobre identidad, uso, propiedad intelectual, datos, finalidades, derechos y servicios.
- Faltan titular, NIF, domicilio, correo y dominio reales. El borrador no es asesoramiento legal; requiere revisión del titular y, si corresponde, asesoramiento profesional.
- Se genera `noindex` hasta completar datos; se excluye del sitemap en ese estado.

## 10. Cookies y consentimiento

**Estado: PENDIENTE DEL USUARIO**

- No se cargan analítica ni publicidad. El diálogo local recuerda una preferencia, pero no es una CMP certificada ni comunica señales TCF. AdSense sigue apagado.
- Antes de anuncios en EEE/Reino Unido/Suiza, configura una CMP compatible. Para anuncios personalizados, Google exige CMP certificada con integración TCF ([requisitos oficiales](https://support.google.com/adsense/answer/13554116?hl=es)). Actualiza la política y comprueba aceptar/rechazar, preferencias y retirada según la configuración real. No se ha simulado una certificación.

## 11. Categorías y enlaces

**Estado: COMPLETADO EN COMPROBACIONES ESTÁTICAS**

- Las 12 categorías del menú existen: GTA VI, Videojuegos, PlayStation, Xbox, PC Gaming, Nintendo, Anime, Manga, Rankings, Curiosidades, Guías y Tecnología.
- `scripts/audit_generated.py` comprobó cero enlaces internos rotos en 137 HTML. El generador valida categorías, categorías cruzadas, slugs y títulos duplicados. El buscador tiene índice local generado, menú/footers y breadcrumbs con rutas relativas.
- El JavaScript pasó revisión sintáctica. No se pudo comprobar la interacción real en navegador.

## 12. Versión móvil

**Estado: PENDIENTE DE VERIFICACIÓN VISUAL**

- Se revisaron los media queries en 1120, 900, 640 y 380 px; los anchos solicitados quedan cubiertos por esas reglas.
- No se completó la prueba visual de 360, 390, 430, 768, 1024 y 1440 px. El navegador conectado bloqueó observar archivos `file://`; no se afirma que se hayan probado los seis tamaños. Repetirlos tras publicar o en un entorno autorizado y corregir cualquier desbordamiento real.

## 13. Limpieza y control final

**Estado: COMPLETADO PARA LA COPIA LOCAL; PUBLICACIÓN PENDIENTE**

- `python scripts/build.py`: 112 artículos, 12 categorías, 6 páginas informativas, 137 HTML, 238 espacios de anuncios; AdSense `off`.
- `python scripts/audit_generated.py`: correcto, 0 enlaces internos rotos, imágenes locales presentes, 1 H1 por artículo, sin slugs/títulos duplicados ni texto Lorem Ipsum.
- `python scripts/check_adsense.py`: correcto, 0 cargadores/0 unidades activas, 238 huecos reservados.
- `python -m py_compile ...` en scripts principales y `node --check` en `main.js`/`search.js`: correctos.
- Sitemap local parseable y vacío; prueba pública aislada: 127 URLs únicas con ruta indexable presente. No se probó una acción GitHub ni una respuesta Pages porque el repositorio remoto está vacío.

## Cierre

La estructura local está preparada para continuar el lanzamiento, pero aún no está lista para solicitar AdSense ni indexar públicamente. Los bloqueos que requieren al titular son: repositorio/dominio/HTTPS, verificación Search Console, identidad y textos legales, servicio real de contacto, CMP, revisión de licencias y revisión editorial final. Ningún estado de aprobación de Google se ha afirmado.
