# SEO técnico — LEVELUP DAILY

Revisado: 24 de noviembre de 2026 antes del primer despliegue. Auditoría de archivos locales; la URL objetivo está configurada, pero aún no hay una web publicada ni verificación en Search Console.

## Estado y URL pública

- `site.json` apunta a `https://ascendsystem.github.io/levelup-daily`, la URL prevista para este repositorio. La API confirma la rama predeterminada `main`, pero todavía no hay ramas ni commits y Pages no está habilitado. No hay respuestas HTTP, certificado, canonical en vivo ni Core Web Vitals que comprobar.
- Los HTML generados llevan metadatos canónicos de esa URL; abrir los archivos mediante `file://` no los publica ni permite que Google los rastree. Las páginas legales incompletas, búsqueda y 404 permanecen noindex y fuera del sitemap.
- El generador usa una única `base_url` para canonical, Open Graph, Schema.org, sitemap y robots. No hay dominio propio www/no-www configurado.

## Sitemap y robots

- El build con la URL objetivo configurada genera un `sitemap.xml` válido con **127 URLs HTTPS únicas**: portada, 12 categorías, 112 artículos y 2 páginas informativas indexables. Cada ruta tiene HTML indexable; no incluye 404, búsqueda, duplicados ni páginas noindex.
- `robots.txt` generado declara el sitemap esperado. GitHub Pages aún no está habilitado, por lo que estas rutas no se han podido consultar en producción.
- Se excluyen del sitemap las páginas Sobre nosotros, Contacto, Privacidad y Aviso legal mientras falten datos identificativos obligatorios. El generador añade `noindex,nofollow` a esas páginas; cuando estén completas, pasan a ser aptas para indexación. Cookies y Política editorial se incluyen si sus contenidos siguen completos.
- El robots de producción generado permite el rastreo de páginas, CSS, JavaScript e imágenes; declara el sitemap y solo excluye rutas de fuentes y datos de búsqueda. Debe regenerarse con el dominio definitivo antes de publicar. Google explica que `robots.txt` controla el rastreo y que `noindex` es la señal para excluir páginas de resultados: [guía de robots.txt](https://developers.google.com/search/docs/crawling-indexing/robots/intro?hl=es).
- Google trata la inclusión en sitemap como una señal, no una garantía de indexación: [prácticas recomendadas para sitemaps](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap?hl=es).

## Canónicas, metadatos y datos estructurados

- El generador crea canonical absoluto en páginas públicas a partir de `base_url`; las páginas de búsqueda, 404 y legales incompletas quedan sin canonical e indexación.
- Las páginas públicas generan meta description, Open Graph, Twitter Card y datos JSON-LD acordes con su plantilla: `Organization`/`WebSite` para inicio, `CollectionPage`/`ItemList` y migas para categorías, y `BlogPosting` o `NewsArticle` y migas para artículos. No se generan estrellas ni valoraciones falsas.
- El campo vacío `google_search_console_verification` permite insertar el valor real de una etiqueta HTML de verificación únicamente en el `<head>` de la portada. No hay token ni verificación incorporados. Las propiedades de dominio se verifican mediante el registro DNS TXT que proporciona Search Console; la meta etiqueta es para propiedades de prefijo URL. Consulta [verificar la propiedad de un sitio](https://support.google.com/webmasters/answer/9008080?hl=es).
- En los 112 artículos no se detectaron descripciones duplicadas. Longitud observada: 84–175 caracteres. La longitud no garantiza que el snippet aparezca igual en Google.

## Artículos, enlaces y recursos

- `scripts/audit_generated.py`: 112 artículos, 137 archivos HTML, exactamente un H1 por artículo, imágenes locales existentes y cero enlaces internos rotos. No se encontraron slugs ni títulos duplicados; los artículos tienen alt text. La búsqueda y el menú tienen JavaScript sintácticamente válido y recursos locales presentes; no se pudo hacer una prueba de interacción real en navegador.
- El control local no consulta el estado HTTP de cada URL externa; se revisaron en fuentes oficiales las afirmaciones actuales clave de GTA VI, pero queda pendiente confirmar la disponibilidad de todos los enlaces externos después del despliegue.
- En una muestra editorial de 30 páginas (25 GTA VI y 5 de otros temas), la extensión fue de 516–790 palabras; todas las páginas muestreadas mostraban imagen, fecha, meta description y navegación contextual. Los detalles y límites de la revisión están en `LAUNCH-AUDIT.md`.
- Una página evergreen de métodos para encontrar easter eggs no contiene enlaces de fuentes; sus recomendaciones son editoriales y no incluye datos concretos de juego. Las guías de secretos, dinero y trucos de GTA VI dependen de guías secundarias y requieren mantener la atribución, las fechas y la revisión tras parches.
- Se detectó y se aclaró en el artículo de trucos una discrepancia entre PC Gamer y PowerPyx sobre el reto de Munición máxima (20 frente a 25 medallas de bronce); el dato se presenta atribuido, no como hecho oficial.
- No se encontró texto «Lorem ipsum». El buscador no se incluye en sitemap. La página 404 existe con enlaces a inicio y búsqueda.

## Imágenes

- El build local verificó 168 imágenes asignadas: no hay rutas de imagen local rotas; todas las imágenes asignadas raster son de al menos 1067 × 720 px (mínimos independientes de ancho/alto) y ninguna está por debajo de 640 × 360 px. Todas las imágenes incluidas tienen atributo `alt`.
- SHA-256 y pHash registran 17 duplicados exactos y 24 coincidencias perceptuales entre los archivos locales; 32 archivos asignados y 37 grupos SHA-256 aparecen en más de un artículo. Son asignaciones heredadas que se conservaron, no se deduplicaron ni reasignaron.
- Hay dos imágenes pendientes (portada e interior) en el artículo sobre Little Sam. La auditoría de derechos no puede confirmar ausencia de marcas de agua ni permiso comercial para 151 asignaciones. Ver `IMAGE-AUDIT.md` y `assets/images/image-credits.json`.

## Core Web Vitals y rendimiento

- **Pendiente:** no hay una URL pública para medir LCP, INP, CLS, Lighthouse/PageSpeed, carga real en móvil o errores de red. La reserva de `width`/`height`, imágenes locales y `loading="lazy"` en imágenes no prioritarias ayuda al layout, pero no sustituye una medición de campo.
- La prueba visual solicitada en los anchos 360, 390, 430, 768, 1024 y 1440 px no se pudo hacer: el navegador conectado bloqueó el protocolo local `file://` y no autorizó observar esa página. Solo se revisaron estáticamente las reglas CSS (1120, 900, 640 y 380 px); no afirmo una validación visual.

## Comprobaciones ejecutadas

- `python scripts/build.py` — 112 artículos, 12 categorías, 6 páginas informativas; modo local noindex; 137 HTML, 238 reservas de anuncios.
- `python scripts/audit_generated.py` — correcto, 0 enlaces locales rotos.
- `python scripts/check_adsense.py` — correcto, 0 cargadores/unidades activos y 238 huecos reservados.
- `python -m py_compile scripts/build.py scripts/adsense.py scripts/check_adsense.py scripts/audit_generated.py scripts/image_audit.py` — correcto.
- `node --check assets/js/main.js` y `node --check assets/js/search.js` — correcto.
- XML del sitemap local parseado; 0 URLs según el modo local. Simulación pública aislada: 127 URLs únicas.

## Antes de indexar

1. Configurar dominio y HTTPS en Pages; cambiar `site.json` al dominio canónico real y confirmar redirecciones.
2. Completar páginas legales y contacto, y verificar Search Console con un token real o el TXT que Google proporcione.
3. Desplegar el artefacto correcto, revisar `https://TU-DOMINIO/robots.txt` y `/sitemap.xml` en vivo, y enviar el sitemap en Search Console.
4. Medir Core Web Vitals en la URL publicada y repetir las pruebas responsive visuales. La presencia del sitemap no garantiza que Google rastree o indexe las páginas.
