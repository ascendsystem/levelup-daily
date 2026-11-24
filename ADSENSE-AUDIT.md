# Auditoría de preparación para Google AdSense

Revisión técnica: 24 de noviembre de 2026. **Estado: todavía no se puede solicitar la revisión desde esta copia.** La aceptación depende de Google; esta auditoría no garantiza aprobación.

## Estado comprobado

- `site.json` apunta a la URL prevista `https://ascendsystem.github.io/levelup-daily`; los campos de Analytics y Publisher ID siguen vacíos. No hay un ID real confirmado ni unidades publicitarias activas. GitHub Pages aún no está habilitado.
- La configuración central está en modo `off`. El build local no carga etiquetas de AdSense ni solicita anuncios.
- Hay 238 espacios editoriales reservados en 137 páginas HTML. No muestran texto de anuncio ni contienen unidades activas.
- No se sirve publicidad en contacto, información legal, privacidad, búsqueda ni error 404. Se quitó el espacio lateral junto a enlaces de navegación.
- `ads.txt` no se publica mientras falta el ID real. Cuando se configure un ID confirmado y un dominio público HTTPS, el build añadirá la línea de Google a la raíz y conservará otras líneas existentes.
- El panel local de privacidad no es una CMP certificada ni genera señales TCF. Los archivos para integrar y reabrir una CMP siguen siendo marcadores y AdSense permanece bloqueado.
- Las páginas legales todavía tienen campos de titular, contacto, NIF, domicilio y dominio pendientes.
- La auditoría de imágenes registra 174 archivos, 168 asignados. 151 registros conservan la asignación y tienen derechos por verificar; 18 imágenes Pexels tienen URL, autor y referencia a su licencia, pero la fecha de descarga no consta. Pexels permite uso en sitios web bajo su licencia, con restricciones; eso no resuelve los derechos de imágenes de Rockstar, Riot o procedencia desconocida. Revisa cada uso antes de monetizar.
- Antes del primer push, la carpeta remota `ascendsystem/levelup-daily` no tiene ramas ni commits y este `.git` local no tiene historial. El workflow no se ha ejecutado en GitHub; Pages y HTTPS no se han podido comprobar.
- El formulario de contacto valida en el navegador, pero no envía ni almacena el mensaje. Falta configurar un receptor y actualizar privacidad antes de habilitar envíos.
- AdSense permanece apagado y sin código de editor. No debe solicitarse una revisión hasta completar identidad, páginas legales, derechos de imágenes, consentimiento y demás requisitos aplicables.

## Arquitectura instalada

- `scripts/adsense.py` concentra los modos, la etiqueta global, el renderizado de unidades, la CMP, la inclusión de fragmentos oficiales y la sincronización no destructiva de `ads.txt`.
- `scripts/build.py` utiliza ese módulo desde una plantilla común. Todo artículo nuevo, categoría nueva y portada hereda las mismas posiciones sin añadir código de Google a cada contenido.
- `scripts/check_adsense.py` valida las páginas generadas, verifica que las unidades estén dentro de los espacios centrales, que no se aniden en enlaces/controles y que no aparezcan en páginas excluidas.
- `.github/workflows/pages.yml` ejecuta el auditor de salida antes de preparar el artefacto y solo copia `ads.txt` si el sitio es público y la integración está configurada con un Publisher ID confirmado.
- Los únicos puntos editoriales previstos son la portada, páginas de categoría y cortes dentro del artículo, separados de controles y navegación. No se renderiza una unidad junto al índice clicable ni en la barra lateral.
- El sitemap público se genera con URLs de páginas indexables; un test aislado de configuración pública verificó 127 rutas únicas y existentes. La copia local no tiene dominio real y el XML permanece vacío.
- Los archivos `content/adsense-recovery-tag.html` y `content/adsense-error-protection.html` se mantienen intactos. Solo se leerán cuando el modo esté activo, exista un ID confirmado y haya código real de Google sin marcadores.
- `assets/js/main.js` solo muestra el aviso de bloqueo de anuncios cuando detecta una unidad AdSense activa; el modo de verificación sin unidades no interrumpe la lectura.

## Bloqueos antes de solicitar la revisión

1. Configurar el dominio definitivo, HTTPS, Search Console, sitemap y rastreo público.
2. Completar y revisar la identidad editorial y las páginas legales.
3. Revisar todos los artículos para asegurar contenido original, útil, actualizado y navegable; revisar especialmente afirmaciones de juegos y noticias que cambian con parches.
4. Documentar la licencia o autorización de cada imagen que vaya a monetizarse.
5. Elegir e integrar una CMP adecuada. Para anuncios personalizados en el EEE, Reino Unido y Suiza, Google exige una CMP certificada que integre TCF. Comprobar también el rechazo y el control para reabrir o retirar preferencias.
6. Copiar el Publisher ID y los IDs de unidades desde la cuenta real de AdSense. No rellenar marcadores con valores inventados.
7. Desplegar el sitio, comprobar `https://TU-DOMINIO/ads.txt`, y usar la página **Sites** de AdSense para solicitar la revisión. Solo Google puede cambiar el estado a **Ready**.
8. Revisar manualmente el resultado visual en ordenador y móvil, incluidas páginas largas, y comprobar el Centro de políticas antes y después de activar anuncios.

La revisión inicial de AdSense se realiza sobre el sitio. No hay un paso de aprobación editorial individual que LEVELUP DAILY tenga que ejecutar para cada artículo nuevo; cada página debe cumplir las políticas y Google puede revisar páginas, limitar anuncios o señalar incidencias después de la aprobación. Consulta [gestión de sitios de AdSense](https://support.google.com/adsense/answer/12131223) y los [requisitos de calidad y elegibilidad](https://support.google.com/adsense/answer/7299563?hl=es).

La fecha de revisión de la licencia Pexels y su uso permitido debe comprobarse de nuevo antes de una campaña; la página oficial explica usos y límites: [Pexels License](https://www.pexels.com/license/).

## Revisión de colocación

El preflight automático pasó en la copia actual: 137 HTML, modo `off`, 0 cargadores, 0 unidades activas y 238 espacios reservados. La revisión confirma el marcado, no puede juzgar todos los resultados visuales de una página desplegada.

Las ubicaciones activas deben seguir separadas visualmente de enlaces, botones, descargas, galerías e imágenes editoriales; no se debe animar ni señalar anuncios ni usar encabezados engañosos. Google prohíbe diseños que lleven a clics accidentales o hagan parecer un anuncio parte de la navegación. Revisa las [políticas de colocación de anuncios](https://support.google.com/adsense/answer/1346295?hl=en).

## Referencias oficiales

- [Añadir y administrar sitios de AdSense](https://support.google.com/adsense/answer/12131223)
- [Preparar las páginas para AdSense](https://support.google.com/adsense/answer/7299563?hl=es)
- [Estados de revisión y estado del sitio](https://support.google.com/adsense/answer/12170222)
- [Crear y corregir `ads.txt`](https://support.google.com/adsense/answer/12171612?hl=en-ZZ)
- [CMP certificada y TCF para EEE, Reino Unido y Suiza](https://support.google.com/adsense/answer/13554020?hl=es-GB)
- [Políticas de colocación](https://support.google.com/adsense/answer/1346295?hl=en)
- [Centro de políticas](https://support.google.com/adsense/answer/9485926?hl=en)
- [Recuperación de bloqueadores de anuncios](https://support.google.com/adsense/answer/11576085?hl=es-ES)
