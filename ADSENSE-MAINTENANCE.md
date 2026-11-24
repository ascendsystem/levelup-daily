# Mantenimiento de Google AdSense — LEVELUP DAILY

Este manual describe la integración central. Google decide si acepta el sitio y puede revisar contenido o limitar anuncios después de la aprobación. La copia actual está en modo `off`: no contiene un Publisher ID real, no sirve anuncios y no se debe enviar a revisión mientras el dominio y los datos legales sigan pendientes.

## Cómo funciona la arquitectura

- `site.json` es el único lugar para el Publisher ID, el modo, los IDs de unidades y el estado de consentimiento.
- `scripts/adsense.py` valida la configuración, genera la etiqueta global una vez en el `<head>` de cada página editorial, renderiza los espacios que tengan un ID real y mantiene `ads.txt`.
- `scripts/build.py` utiliza la misma plantilla en la portada, artículos y categorías. Al añadir un artículo no se pega código de Google en su JSON ni en su HTML.
- `scripts/check_adsense.py` y el propio build comprueban las ubicaciones, el ID, el número de cargadores, los anuncios en páginas excluidas y el `ads.txt`.
- `content/adsense-cmp.html` y `content/adsense-cmp-preferences.html` son los puntos de integración de la CMP. Los fragmentos oficiales de recuperación de bloqueadores están en `content/adsense-recovery-tag.html` y `content/adsense-error-protection.html`.

No edites a mano las páginas HTML generadas. Modifica los datos fuente y vuelve a ejecutar el build; así no se pierden etiquetas ni se duplican unidades.

## Añadir artículos y categorías

1. Añade el artículo a su archivo de contenido y usa su categoría existente. La plantilla central añade los espacios de artículo después de la primera sección y a mitad del contenido.
2. Para una categoría nueva, regístrala en `CATEGORIES` de `scripts/build.py`. Su página hereda la posición `category_mid`.
3. Ejecuta `python scripts/build.py`. El build regenera las páginas y lanza el preflight de AdSense.
4. Comprueba `python scripts/check_adsense.py`. En modo `off` o `review`, debe indicar cero unidades activas. En modo `active`, el resultado debe corresponder a las unidades configuradas.
5. Revisa la página desplegada en escritorio y móvil. Los anuncios deben distinguirse del contenido y quedar apartados de navegación, botones, enlaces, descargas, galerías e imágenes. No pidas a los lectores que hagan clic.

Las páginas de información legal, privacidad, contacto, búsqueda y error 404 no reciben unidades. Mantén esta exclusión; las páginas que no aportan contenido editorial no deben heredar anuncios automáticamente.

## Activación por etapas

### `off` — estado actual

No inserta el cargador ni solicita anuncios. Los espacios conservan su altura sin texto de marcador. El build no crea ni altera `ads.txt`.

### `review` — verificación del sitio

Cuando exista una cuenta real, copia el ID de editor desde AdSense (`ca-pub-` y 16 dígitos) a `adsense_publisher_id` y establece `publisher_id_confirmed` en `true` solo después de comprobarlo en la cuenta. Cambia `adsense.mode` a `review` y despliega sobre el dominio HTTPS definitivo.

El modo `review` carga la etiqueta global en páginas editoriales pero no genera unidades `<ins>`; crea o añade la línea real de Google a `ads.txt` sin reemplazar otras líneas. Mantén Auto Ads desactivado hasta verificar el estado del sitio. También puedes usar un método de verificación ofrecido por Google, como Search Console.

### `active` — anuncios

Actívalo solo después de que AdSense muestre el sitio como **Ready**, de configurar una CMP adecuada y de crear unidades reales en la cuenta.

En `site.json`:

- Mantén el Publisher ID real y `publisher_id_confirmed: true`.
- Cambia `adsense.mode` a `active`.
- Pega los códigos exactos de la CMP en los dos archivos indicados. No inventes ni edites los IDs de CMP, TCF, editor o unidad.
- Marca `certified_tcf_cmp_confirmed` y `preferences_entrypoint_confirmed` como `true` solo después de comprobar la certificación/TCF y que el usuario puede reabrir o retirar su elección.
- Copia en `adsense.units` los IDs numéricos de unidad que cree AdSense. Deja en blanco las ubicaciones que no vayas a usar.

El build se detiene si falta un ID confirmado, una unidad, la CMP o el control para reabrir preferencias. Ese bloqueo evita activar por error un panel local que no sea CMP. Para el tráfico del EEE, Reino Unido y Suiza, Google exige una CMP certificada e integrada con TCF al servir anuncios personalizados; revisa la política vigente y el proveedor elegido antes de activar.

## Ubicaciones admitidas

Los nombres de posición configurables están en `POSITIONS` dentro de `scripts/adsense.py` y sus IDs en `site.json`:

- `home_after_headlines`, `home_mid`: cortes en la portada.
- `category_mid`: entre el bloque destacado de una categoría y el archivo de artículos.
- `article_after_first_section`, `article_mid`: cortes dentro del cuerpo editorial, alejados del índice clicable y de los controles.

No se coloca publicidad en la barra lateral junto a enlaces, ni junto al botón de compartir, ni en páginas legales, de búsqueda o 404. Si se necesita una ubicación nueva, añádela al módulo central, al config y a la comprobación; no insertes una unidad directa en una página concreta. Google prohíbe colocaciones que puedan confundirse con navegación o provocar clics accidentales. Consulta sus [políticas de colocación](https://support.google.com/adsense/answer/1346295?hl=en).

## `ads.txt` y códigos oficiales

- En modo `off`, el generador no toca un `ads.txt` existente ni inventa uno.
- En `review` o `active`, y con dominio público HTTPS, genera la línea oficial de Google a partir del Publisher ID confirmado. No escribe IDs de ejemplo.
- Si `ads.txt` ya contiene una línea diferente para el mismo ID, el build se detiene y conserva el archivo para revisión manual. No elimina registros de otros vendedores.
- Tras desplegar, abre `https://TU-DOMINIO/ads.txt` y confirma el estado en **AdSense → Sites**. Los cambios pueden tardar en reflejarse en la cuenta.
- Nunca pegues códigos de Google en HTML generado ni sobreescribas los archivos de fragmentos oficiales. El build solo los lee; no los modifica.

## Imágenes y contenido

Antes de monetizar una página, confirma la licencia o autorización comercial de sus imágenes y conserva pruebas y atribuciones en `assets/images/image-credits.json`. En la auditoría actual, el permiso comercial de 68 imágenes GTA VI aportadas por el usuario sigue pendiente. Una imagen descargada de Pinterest o de una galería pública no queda automáticamente autorizada para monetización.

Revisa cada artículo para que ofrezca información original y útil, tenga fuentes y navegación clara, y no presente rumores como hechos. Las páginas nuevas usan la integración compartida; eso evita configurar anuncios por artículo, pero no exime a cada página de cumplir las políticas. La aprobación inicial es de sitio y Google puede volver a revisar o limitar contenido.

## Rutina de mantenimiento

| Cuándo | Comprobación |
|---|---|
| Cada cambio del sitio | Ejecutar `python scripts/build.py` y `python scripts/check_adsense.py`; revisar errores antes de publicar. |
| Cada despliegue | Comprobar `ads.txt`, estado del sitio y del archivo en **AdSense → Sites**; abrir páginas nuevas en móvil y escritorio. |
| Mensualmente | Revisar **AdSense → Policy center**, alertas por correo, cobertura/estado de anuncios, CMP y derechos de nuevas imágenes. |
| Cuando cambien Google, la CMP o la legislación | Revisar las políticas, la lista de CMP certificadas, las señales TCF, la política de privacidad/cookies y esta configuración. |
| Al recibir una incidencia | Revisar la URL y la captura que indique Google, corregir todas las páginas con el mismo problema y solicitar la revisión correspondiente en el Centro de políticas. |

Google indica que las políticas pueden cambiar y recomienda comprobarlas con frecuencia. El Centro de políticas es la fuente para incidencias de cumplimiento, regulación y preferencias de anunciantes. Consulta [la guía de AdSense](https://support.google.com/adsense/answer/9485926?hl=en) y [sus políticas del programa](https://support.google.com/adsense/answer/48182?hl=en-EN).
