#!/usr/bin/env python3
"""Curated post-launch GTA VI articles; sources and editorial boundaries are explicit."""
import json
from pathlib import Path

D = "2026-11-24"
S = {
 "launch": ["Rockstar: GTA VI ya disponible", "https://www.rockstargames.com/newswire/article/39akk424a9oo53/grand-theft-auto-vi-now-available"],
 "world": ["Rockstar: Only in Leonida", "https://www.rockstargames.com/VI/only-in-leonida"],
 "media": ["Rockstar: galería y descargas oficiales", "https://www.rockstargames.com/VI/media"],
 "patch": ["Rockstar Support: notas de lanzamiento", "https://support.rockstargames.com/articles/sN5pEdFYZdlvijKXd6xpJ/grand-theft-auto-vi-launch-updates-ps5-xbox-series-x-or-s"],
 "index": ["GamesRadar: guía del Índice", "https://www.gamesradar.com/games/grand-theft-auto/gta-6-index-how-to-find-your-missions-objectives/"],
 "save": ["GamesRadar: cómo guardar", "https://www.gamesradar.com/games/grand-theft-auto/gta-6-how-to-save/"],
 "fast": ["GamesRadar: viaje rápido", "https://www.gamesradar.com/games/grand-theft-auto/gta-6-how-to-fast-travel/"],
 "profile": ["GamesRadar: Criminal Profile", "https://www.gamesradar.com/games/grand-theft-auto/gta-6-criminal-profiles/"],
 "wanted": ["GamesRadar: Wanted Level y Heat", "https://www.gamesradar.com/games/grand-theft-auto/gta-6-wanted-levels-heat/"],
 "cars": ["PC Gamer: robar, registrar y vender coches", "https://www.pcgamer.com/games/grand-theft-auto/gta-6-how-to-steal-cars/"],
 "snap": ["GamesRadar: Snap Gun", "https://www.gamesradar.com/games/grand-theft-auto/gta-6-snap-gun-how-to-get-use/"],
 "postgame": ["GamesRadar: mundo libre tras los créditos", "https://www.gamesradar.com/games/grand-theft-auto/gta-6-play-after-credits-beating-the-game/"],
 "controls": ["GamesRadar: controles clásicos", "https://www.gamesradar.com/games/grand-theft-auto/gta-6-classic-controls/"],
 "replay": ["GamesRadar: repetir misiones", "https://www.gamesradar.com/games/grand-theft-auto/gta-6-replay-missions-how-to/"],
 "missions": ["PC Gamer: capítulos y misiones", "https://www.pcgamer.com/games/grand-theft-auto/gta-6-mission-list/"],
 "activities": ["GamesRadar: actividades secundarias", "https://www.gamesradar.com/games/grand-theft-auto/gta-6-side-activities/"],
 "sam": ["GamesRadar: posible referencia a Little Sam", "https://www.gamesradar.com/games/grand-theft-auto/it-sure-looks-like-rockstar-co-founder-sam-houser-is-hiding-in-gta-6-as-fans-find-little-sam-easter-egg-that-calls-back-to-gta-3/"],
 "tech": ["TechRadar: análisis de GTA VI", "https://www.techradar.com/gaming/gta-6-review"],
 "ap": ["Associated Press: análisis de GTA VI", "https://apnews.com/article/82404adf585e7242e61fb42e8aa05481"],
 "bloq": ["Creative Bloq: análisis de GTA VI", "https://www.creativebloq.com/reviews/gta-6-review-holy-sh-t-its-good"],
 "windows": ["Windows Central: análisis en Xbox", "https://www.windowscentral.com/gaming/xbox/grand-theft-auto-6-xbox-review"],
 "robbery": ["TechRadar: lugares que pueden abordarse de varias formas", "https://www.techradar.com/gaming/gta-6-senior-design-director-confirms-even-when-missions-show-a-level-of-completion-locations-can-still-be-hit-again-and-again-tackling-them-in-different-ways-each-time"],
 "ultimate": ["PC Gamer: contenido Ultimate Edition", "https://www.pcgamer.com/games/grand-theft-auto/gta-6-ultimate-edition-bonuses/"],
 "stats": ["GTA Vice Guides: coches por fichas de estadísticas", "https://gtaviceguides.com/guides/gta-6-best-cars/"],
 "firstperson": ["PC Gamer: cámara en primera persona", "https://www.pcgamer.com/games/grand-theft-auto/gta-6-is-playable-in-first-person-heres-how-to-activate-it/"],
}
R = []
def add(slug, title, desc, dek, intro, sections, end, faq, source_keys, cluster, tags=(), spoiler=False, table=None):
    x = {
      "slug":slug,"category":"gta-6","categories":["gta-6","videojuegos","guias"],
      "cluster":cluster,"tags":list(tags),"title":title,"seo_title":title+" | LEVELUP DAILY",
      "description":desc,"dek":dek,"date":D,"updated":D,"readTime":5,
      "cover":"editorial-"+slug,
      "image_alt":"Infografía editorial original sobre "+title+"; no es una captura del videojuego.",
      "image_caption":"Gráfico editorial original de LEVELUP DAILY. No representa una escena ni una captura de GTA VI.",
      "intro":intro,"sections":[{"title":h,"body":b} for h,b in sections],
      "conclusion":end,"faq":[list(q) for q in faq],
      "sources":[S[k] for k in source_keys],"spoiler_warning":spoiler
    }
    if table: x.update(table)
    R.append(x)

add("gta-6-index-misiones-objetivos","Cómo usar el Índice de GTA VI para encontrar misiones y actividades",
"Guía del Índice de GTA VI: localiza historia, robos, actividades, vehículos y objetivos nuevos sin confundirlos en el mapa.",
"El Índice ordena las tareas de Leonida. Aprende qué categorías mirar y cómo reconocer una oportunidad recién disponible.",
"Cuando el mapa se llena de iconos, el Índice ofrece una forma más ordenada de buscar qué hacer. GamesRadar describe apartados para datos personales, historia, robos, actividades, exploración, vehículos, armas, estilo y comida. Esta explicación se limita a funciones documentadas y sirve para elegir un objetivo sin depender de listas de fans o mapas ajenos a tu partida.",
[
("Qué es y para qué sirve","El Índice reúne tareas y puntos de interés. No sustituye al mapa: lo complementa con grupos que responden a preguntas distintas, como qué misión sigue, dónde están tus vehículos o qué actividades has desbloqueado. GamesRadar indica que los objetivos nuevos pueden aparecer con un diamante naranja. Si no ves una entrada, puede depender del progreso o de una llamada pendiente."),
("Categorías que conviene revisar","Story reúne misiones principales y tareas opcionales. Robberies agrupa oportunidades delictivas; Activities y Exploration ayudan a separar pasatiempos y descubrimientos; Vehicles, Weapons y Style ordenan servicios. Personal incluye vehículos propios, vivienda, garajes y cajeros. Los nombres varían con el idioma de la consola: fíjate en la función, no solo en la traducción literal."),
("Rutina para evitar perderte","Al comenzar una sesión, revisa primero los objetivos nuevos; después decide si quieres seguir la trama o explorar. Mira el mapa y marca la ruta solo cuando hayas elegido actividad. Si buscas una tarea secundaria, evita abrir una lista con nombres de misiones si quieres mantener la historia libre de spoilers. Anota capítulo y versión cuando una entrada no aparezca como indica una guía.")
],"El Índice organiza tareas, no garantiza que todo esté desbloqueado. Revisa sus categorías y avisos de actividad nueva, y contrasta el progreso con tu partida.",
[("¿Dónde aparecen las misiones principales?","En Story, separado de las tareas opcionales según la guía consultada."),("¿Cómo detecto una actividad nueva?","GamesRadar describe un diamante naranja junto a oportunidades nuevas."),("¿El Índice muestra todos los secretos?","No hay una lista oficial completa que permita afirmarlo.")],
["index","world"],"guías",("indice","misiones","exploración"))

add("gta-6-repetir-misiones-guardados-manuales","¿Se pueden repetir misiones en GTA VI? Cómo proteger tus partidas",
"GTA VI no incluye un menú de repetición de misiones en su versión de lanzamiento. Te explicamos el papel de los guardados manuales.",
"Si quieres volver a una misión, una ranura guardada antes del evento es más segura que confiar en un replay inexistente.",
"GamesRadar indica que GTA VI no incluye una opción para volver a ejecutar libremente una misión ya completada. Las guías consultadas tampoco documentan un añadido posterior a 24 de noviembre de 2026. Por eso, quien quiera conservar un punto concreto debe gestionar guardados manuales antes de avanzar. Esta página explica la limitación sin prometer que una partida permita repetir escenas o recuperar decisiones.",
[
("Qué significa no tener repetición","Al terminar una misión no puedes abrir un catálogo equivalente al de entregas anteriores y volverla a jugar desde el inicio. La campaña continúa desde el estado actual del mundo. Un reinicio dentro de una misión fallida no es un replay permanente de misiones completadas."),
("Cómo cuidar las ranuras","GamesRadar recoge 15 ranuras manuales y un espacio automático separado. Antes de una misión importante, crea un punto manual sin sobrescribir tu único guardado. Mantén una rotación: partida reciente, comienzo del capítulo y un punto previo a una decisión que te importe. Comprueba fecha, porcentaje y protagonista antes de reemplazar una ranura."),
("Evita spoilers al buscar la respuesta","Las listas de capítulos revelan nombres de misiones. Si solo buscas saber si existe replay, no abras una tabla completa. Comprueba si una guía separa historia de objetivos opcionales y conserva un guardado propio si quieres revisar un tramo. Si Rockstar añade una función de replay, actualizaremos el dato desde notas oficiales.")
],"A día de hoy, planifica los guardados como puntos de retorno: las guías consultadas no muestran un menú de repetición. Conserva ranuras antes de avanzar.",
[("¿Puedo repetir una misión completada?","No hay opción de repetición en el lanzamiento, según GamesRadar."),("¿Cómo vuelvo a un punto anterior?","Carga un guardado manual creado antes de esa misión."),("¿Cuántas ranuras manuales hay?","GamesRadar cuenta 15 ranuras manuales y un espacio separado de autoguardado.")],
["replay","save","missions"],"guías",("repetir-misiones","guardados","spoilers"))

add("gta-6-viaje-rapido-transporte","Viaje rápido en GTA VI: taxis, autobuses y trenes",
"Cómo desplazarte rápido en GTA VI con taxis y transporte público, qué servicios requieren ir a una parada y cuándo puedes saltar el trayecto.",
"Leonida tiene varias opciones, pero autobús y tren no funcionan como una teletransportación a demanda.",
"GamesRadar diferencia el transporte público de los taxis: para bus y tren hay que ir a una parada, mientras que el taxi se solicita desde el teléfono. Estos detalles ahorran vueltas, pero pueden cambiar con el progreso o la disponibilidad del servicio. Esta guía no promete que cualquier trayecto sea gratuito ni instantáneo.",
[
("Autobús y tren","La guía describe una red de transporte público, pero no disponible bajo demanda. Usa abajo en la cruceta para buscar paradas; acércate a la estación para consultar cuándo llega el siguiente servicio. Una vez a bordo, selecciona destino y usa el botón que aparece en pantalla para saltar parte del viaje."),
("Taxis desde el teléfono","GamesRadar señala que el contacto de Paradise Taxi se obtiene durante una misión temprana y queda en el móvil. Así puedes llamar al servicio sin caminar hasta una terminal. Consulta coste y destino antes de confirmar: el desplazamiento puede consumir dinero y tiempo del mundo."),
("Qué opción conviene","Para descubrir Leonida, conduce tú mismo y aprovecha el trayecto. Para cruzar una distancia larga, compara taxi con transporte público y considera la espera. Si una actividad exige conservar un coche o cumplir una condición de misión, revisa el objetivo antes de elegir viaje rápido.")
],"El taxi se solicita por teléfono; bus y tren requieren una parada. Comprueba coste y objetivo antes de saltarte el trayecto.",
[("¿Puedo llamar un autobús desde cualquier sitio?","No, hay que esperar en una parada o estación."),("¿Cómo encuentro paradas cercanas?","La guía indica usar abajo en la cruceta."),("¿Se puede saltar el viaje?","Sí, una vez a bordo, con el botón que muestra el juego.")],
["fast","world"],"guías",("viaje-rapido","transporte","taxi"))

add("gta-6-perfil-criminal-consecuencias","Perfil Criminal de GTA VI: qué registra y qué puede cambiar",
"Qué se sabe del Criminal Profile de Jason y Lucia, cómo consultarlo y por qué no es un medidor simple de bien o mal.",
"El juego observa el estilo de ambos protagonistas. Separamos los efectos reportados de interpretaciones sobre finales.",
"Criminal Profile registra acciones de Jason y Lucia y refleja patrones de conducta, según GamesRadar. No equivale a una barra moral con una única respuesta correcta: la guía habla de efectos en el combate y en reacciones del entorno, pero las conclusiones sobre finales requieren cautela. Aquí distinguimos lo descrito de lo que todavía no está probado.",
[
("Qué observa el sistema","La guía dice que el perfil refleja conductas durante la partida y que se consulta manteniendo la cruceta a la derecha. Distingue actos obligatorios de misión de acciones extra que el jugador decide hacer. Por eso, una escena forzada no debería tratarse automáticamente como una elección libre que define la etiqueta."),
("Efectos que se han descrito","GamesRadar menciona cambios en Combat Focus y diferencias sutiles en respuestas de personajes y policía. Describe perfiles que van de conducta más profesional a más violenta. La palabra importante es sutil: no prometemos una rama narrativa concreta basándonos en una sola barra o un comentario de foro."),
("Cómo leerlo sin jugar para una etiqueta","Consulta el estado de ambos personajes y observa cambios después de varias decisiones. Para una partida prudente, evita escalar encuentros innecesariamente y conserva un guardado antes de momentos importantes. No recargues por una variación menor sin saber qué estás midiendo.")
],"El Perfil Criminal registra patrones de los dos protagonistas y puede afectar combate y reacciones. Las consecuencias extremas necesitan pruebas claras.",
[("¿Dónde se consulta?","Mantén la cruceta hacia la derecha, según GamesRadar."),("¿Es igual al honor de Red Dead Redemption 2?","La comparación es orientativa, no significa que sean sistemas idénticos."),("¿Cambia el final?","No generalizamos sin pruebas reproducibles de cada consecuencia.")],
["profile","tech"],"guías",("perfil-criminal","jason","lucia"))

add("gta-6-nivel-busqueda-seis-estrellas","Nivel de búsqueda y Heat en GTA VI: cómo interpretar las seis estrellas",
"Guía del sistema de búsqueda de GTA VI: seis estrellas, indicadores de estado y correcciones del parche inicial.",
"La persecución tiene más matices que un aviso. Entiende qué afirma la guía y qué arregló Rockstar el 23 de noviembre.",
"GamesRadar describe seis estrellas y distintos estados visuales que matizan la respuesta policial. Rockstar corrigió un fallo por el que podía no perderse el nivel de búsqueda. Así separamos una mecánica de un error de lanzamiento, sin asignar unidades exactas a cada estrella si la fuente no las mide.",
[
("Seis estrellas no son seis situaciones idénticas","La guía amplía el medidor a seis estrellas y dice que la apariencia puede variar según estado. La respuesta inicial no tiene por qué ser igual a la escalada posterior. No convertimos esto en una tabla de policías, vehículos o tiempos si no hay datos consistentes para cada nivel."),
("Si el nivel no baja","En sus notas del 23 de noviembre, Rockstar incluye la corrección de un problema que impedía perder el Wanted Level. Si el comportamiento no coincide con una guía anterior al parche, comprueba que la consola instaló la actualización. Anota plataforma y situación si persiste: las notas no explican cada caso ni garantizan reparar partidas afectadas."),
("Cómo interpretar la búsqueda","Una persecución depende de la acción, zona y estado de misión. No presentamos cambiar de coche o huir como fórmula universal hasta comprobarlo en la versión actual. Mira el indicador del juego y no uses capturas de otra plataforma como prueba de los mismos tiempos.")
],"La guía describe seis estrellas. Si la búsqueda no termina, Rockstar corrigió un error relacionado el 23 de noviembre; verifica que el parche está instalado.",
[("¿Cuántas estrellas tiene?","GamesRadar describe seis."),("¿El parche arregló un fallo del Wanted Level?","Sí, Rockstar anotó una corrección para un problema que impedía perderlo."),("¿Cada estrella activa una unidad fija?","No publicamos equivalencias sin datos verificables.")],
["wanted","patch"],"guías",("wanted-level","heat","policía"))

add("gta-6-waink-it-app-coches","Waink It en GTA VI: cómo escanear coches y leer sus datos",
"Waink It muestra modelo, alarma, cierre, rastreador, estado y opciones de venta o registro de los coches.",
"El escáner del móvil ayuda a evaluar un vehículo antes de robarlo; estos son los datos documentados.",
"PC Gamer detalla que Waink It se instala durante una misión del capítulo 1 y permite examinar coches antes de decidir qué hacer. No es un listado completo de modelos ni confirma por sí sola que un vehículo sea seguro: un rastreador o una alarma pueden convertir un atajo en una persecución.",
[
("Cuándo aparece","La guía sitúa su instalación en Unwanted Attention del capítulo 1. La app muestra marca y modelo, cierre, alarma, sistema keyless y rastreador. Si no aparece, comprueba la misión y el teléfono antes de buscar una descarga externa o una supuesta aplicación secreta."),
("Qué datos aporta","PC Gamer dice que Waink It también informa estado, valor estimado y coste de registro. Sirve para decidir si conservar, vender o dejar pasar un coche. El valor es una referencia: el estado, comprador y requisitos pueden alterar el resultado."),
("Decide antes de forzar la entrada","Escanea primero para saber qué método podría requerir el vehículo. Un coche cerrado puede necesitar una herramienta distinta a romper una ventanilla y uno keyless tiene requisitos adicionales. Verifica el registro en el punto de servicio; huir de la escena no elimina automáticamente un rastreador.")
],"Escanea antes de actuar: Waink It identifica riesgos y da datos de valor y registro, pero no reemplaza las herramientas que desbloquea la historia.",
[("¿En qué misión se instala?","PC Gamer la sitúa en Unwanted Attention, capítulo 1."),("¿Detecta rastreadores?","Sí, según la guía."),("¿El valor mostrado es precio final?","No necesariamente; es una referencia de la app.")],
["cars","world"],"guías",("waink-it","coches","aplicaciones"))

add("gta-6-robar-coches-herramientas","Robar coches en GTA VI: cristal, Slim Jim y Key Cloner",
"Qué cambia al robar coches: entradas ruidosas, coches keyless, alarmas y herramientas que se consiguen al avanzar.",
"No todas las puertas se fuerzan igual. La historia introduce varios métodos y dispositivos.",
"PC Gamer documenta varias formas de entrar en vehículos: romper una ventanilla, usar Slim Jim en algunos cierres o recurrir al Key Cloner con coches keyless. La secuencia depende del vehículo y del progreso. Esta guía explica la lógica general, no una ruta universal para cada modelo.",
[
("Romper la ventanilla","Forzar una puerta a golpes es rápido, pero puede activar alarmas o atraer atención. PC Gamer advierte que algunos conductores reaccionan con violencia y pueden estar armados. Comprueba la zona, la salida y si el coche merece el riesgo antes de iniciar el forcejeo."),
("Slim Jim","PC Gamer sitúa la obtención de esta herramienta en el capítulo 2, durante Moses. Sirve para abrir en silencio algunas puertas cerradas, sin romper el cristal ni activar la alarma en casos compatibles. No arranca un coche keyless; para ese paso hace falta otra herramienta."),
("Key Cloner","La guía coloca el Key Cloner en el capítulo 3, en Steal the Zorruso for Randy. Se utiliza con coches keyless desde el teléfono. Comprueba además si el coche tiene rastreador: entrar y tener la llave no garantizan que se convierta en vehículo personal.")
],"Identifica el cierre primero: cristal roto, Slim Jim y Key Cloner cumplen funciones distintas y se desbloquean en capítulos diferentes.",
[("¿Slim Jim abre coches keyless?","No, PC Gamer dice que requieren Key Cloner."),("¿Cuándo se consigue el Key Cloner?","Capítulo 3, en Steal the Zorruso for Randy, según la guía."),("¿Romper la ventana activa siempre una alarma?","La fuente describe el riesgo, no un resultado idéntico para todos los coches.")],
["cars","missions"],"guías",("coches","slim-jim","key-cloner"))

add("gta-6-vender-registrar-coches","Cómo vender o registrar coches robados en GTA VI",
"Guía para vender coches: qué puede comprar Pay 'n' Spray, Moses o Randy y cuándo registrar un vehículo para conservarlo.",
"El comprador depende del tipo de coche y del progreso. Waink It ayuda a decidir si vender, registrar o abandonar.",
"Vender un coche robado y quedártelo son decisiones distintas. PC Gamer describe compradores con preferencias diferentes y la opción de registrar algunos vehículos en Pay 'n' Spray. Los requisitos evolucionan con la historia; evitamos fijar precios como universales y explicamos qué comprobar antes de conducir hasta un comprador.",
[
("Pay 'n' Spray y registro","La guía dice que Pay 'n' Spray puede vender vehículos dentro de un límite diario y registrar algunos como personales. Waink It indica coste de registro y valor estimado. Decide si quieres conservarlo para usarlo o convertirlo en dinero. Rastreador y modelo pueden cambiar la disponibilidad."),
("Moses y Randy","PC Gamer diferencia a Moses, interesado en coches antiguos y económicos, de Randy, que busca vehículos más llamativos y caros. Waink It ayuda a comprobar si el modelo encaja. Los contactos se abren con el progreso, así que quizá aún no puedas vender a cada uno."),
("Límites y cifras","La guía consultada atribuye a Pay 'n' Spray un máximo de tres coches al día. No extiendas esa cifra a otros vendedores. Los precios pueden variar según estado y versión. Si el menú rechaza el vehículo, revisa el rastreador y la categoría del comprador.")
],"Escanea y compara la utilidad. Registra el vehículo que quieras conservar; usa Moses, Randy o Pay 'n' Spray cuando modelo y progreso encajen.",
[("¿Puedo vender cualquier coche a Moses?","No; la guía dice que prefiere modelos antiguos y de gama baja."),("¿Qué compra Randy?","Coches más vistosos y caros, según PC Gamer."),("¿Hay límite en Pay 'n' Spray?","La guía informa de tres al día; confirma el comportamiento en tu versión.")],
["cars","index"],"guías",("vender-coches","registrar","dinero"))

add("gta-6-snap-gun-como-se-consigue","Snap Gun de GTA VI: dónde se desbloquea y para qué sirve",
"La Snap Gun abre puertas cerradas sin romperlas. Te contamos el progreso de historia que la desbloquea.",
"Esta herramienta aparece durante el capítulo 3. Incluimos aviso de spoilers leves antes de mencionar la misión.",
"La Snap Gun es un dispositivo de ganzuado. GamesRadar sitúa su obtención después de los encargos de joyería de Yasmani, tras Boobie Time en el capítulo 3. Como esto revela progreso de campaña, el aviso aparece antes del requisito exacto. No la confundas con la Slim Jim, asociada a coches.",
[
("Aviso de spoilers leves","A continuación mencionamos nombres de misiones del capítulo 3, pero no el desenlace. Si quieres descubrir la campaña sin ayuda, detente y vuelve cuando necesites el dato. GamesRadar vincula la Snap Gun a los trabajos de Yasmani posteriores a Boobie Time."),
("Cómo conseguirla","Completa los trabajos de joyería de Yasmani en el capítulo 3, desbloqueados después de Boobie Time. Según GamesRadar, Yasmani entrega la herramienta para ayudar a Jason y Lucia en robos de joyerías. Si no aparece, comprueba las tareas del Índice; buscar un punto aleatorio no sustituye el requisito."),
("Cuándo usarla","La Snap Gun abre ciertas cerraduras sin la entrada ruidosa que puede activar alarmas. No es una llave universal para cualquier puerta: las guías la describen en situaciones de robo y cierres compatibles. Revisa el objetivo antes de forzar la entrada si quieres seguir una ruta o perfil concretos.")
],"La Snap Gun se desbloquea por progreso en el capítulo 3. Consulta el Índice tras completar los trabajos previos de Yasmani.",
[("¿En qué capítulo se obtiene?","GamesRadar sitúa el desbloqueo en el capítulo 3."),("¿Qué trabajos la entregan?","Los encargos de joyería de Yasmani posteriores a Boobie Time."),("¿Es lo mismo que Slim Jim?","No; una abre puertas y la otra algunos coches.")],
["snap","index"],"guías",("snap-gun","cerraduras","robos"),"Aviso: esta guía revela en qué tramo del capítulo 3 se desbloquea la Snap Gun.")

add("gta-6-postgame-despues-creditos","GTA VI después del final: ¿se puede seguir explorando Leonida?",
"Sí, GTA VI permite volver al mundo libre después de la historia. Te explicamos qué ocurre con el guardado y cómo proteger un punto previo.",
"Puedes seguir explorando tras los créditos, pero el juego no te deja justo después del final en un estado neutro.",
"GamesRadar confirma que se puede continuar en mundo libre, con una salvedad sobre dónde carga la partida. La guía dice que se vuelve al autoguardado anterior al punto de no retorno para conservar actividades que dependen de la campaña. Antes de terminar, prepara una ranura manual por si quieres comparar progreso.",
[
("El mundo libre continúa","La guía responde que puedes seguir explorando Leonida tras completar la historia. Eso no implica que cualquier misión principal pueda volver a abrirse: la ausencia de replay es un sistema aparte. Para volver a un tramo concreto necesitarás una partida manual anterior."),
("Qué pasa con el autoguardado","GamesRadar explica que el juego carga un guardado anterior al punto de no retorno, en vez de mantener un mundo posterior con todas las consecuencias. Ese comportamiento puede cambiar con futuras actualizaciones, así que vuelve a comprobarlo tras un parche grande."),
("Prepárate antes del tramo final","Crea un guardado manual y revisa el Índice si quedan objetivos visibles. No hace falta limpiar el mapa entero antes de acabar, según la guía; el juego permite regresar al mundo abierto. La copia manual sigue siendo útil para conservar una decisión anterior.")
],"El mundo libre sigue disponible. Guarda antes del tramo final y recuerda que el retorno descrito usa un autoguardado previo al punto de no retorno.",
[("¿Puedo explorar después de los créditos?","Sí, GamesRadar confirma el mundo libre posterior."),("¿La partida continúa justo después del final?","La guía dice que vuelve a un autoguardado anterior al punto de no retorno."),("¿Puedo repetir una misión?","No hay menú de repetición en el lanzamiento; conserva un guardado previo.")],
["postgame","save","replay"],"guías",("postgame","final","mundo-libre"),"Aviso: este artículo revela detalles del final y del estado del mundo tras los créditos.")

add("gta-6-controles-clasicos-configurar","Controles clásicos de GTA VI: cómo activarlos en PS5 y Xbox",
"Activa el esquema clásico de controles desde Opciones y recupera una distribución más cercana a GTA V.",
"Si la memoria muscular te lleva a pulsar botones equivocados, puedes cambiar el esquema desde Ajustes.",
"GTA VI ofrece un esquema clásico para quienes prefieren una distribución familiar. GamesRadar indica que se activa desde el menú de opciones y resume cambios en correr, saltar y combate. El nombre del botón varía según consola. Esta guía te ayuda a encontrar el ajuste y saber qué probar.",
[
("Dónde cambiar el esquema","Pulsa Options en PS5 o Menu en Xbox y entra en Settings. Allí puedes cambiar de Default a Classic, según GamesRadar. En español busca el apartado de controles; el nombre traducido puede variar por región o parche."),
("Qué acciones cambian","En el esquema predeterminado correr usa L3/LS y saltar X/A, según la guía. En Classic, correr vuelve a X/A y el combate cercano pasa a Circle/B; Square/X queda para escalar o saltar según la tabla del artículo. Comprueba la ayuda en pantalla después del cambio."),
("Prueba antes de una misión exigente","Cambia el ajuste en tiempo libre y prueba correr, saltar, agacharte y pelear. No asumas que todo coincide exactamente con GTA V: es una distribución más cercana, no una garantía de identidad. Revisa también accesibilidad y personalización del mando.")
],"El esquema clásico está en Ajustes. Comprueba las acciones en pantalla y practica antes de volver a una misión.",
[("¿Dónde se activa?","En opciones, dentro de Settings, según GamesRadar."),("¿Qué botón vuelve a correr?","X/A en el esquema clásico."),("¿Es exactamente igual a GTA V?","Es más cercano, pero no todas las acciones tienen que coincidir.")],
["controls","launch"],"guías",("controles","ps5","xbox"))

add("gta-6-primera-persona-camara","¿Tiene GTA VI modo en primera persona? Qué está integrado y qué no",
"GTA VI no ofrece un modo completo en primera persona como ajuste de cámara. Separa las vistas puntuales de los glitches reportados.",
"Las guías describen momentos de cámara cercana y un método no oficial, inestable y susceptible a parches.",
"Muchos jugadores buscan un ajuste de primera persona como en entregas previas. PC Gamer diferencia las vistas puntuales al mirar el teléfono o inspeccionar algo de una cámara completa para conducir y jugar la campaña. También reportó un glitch de lanzamiento; al ser no oficial, no lo presentamos como función ni prometemos que siga activo.",
[
("Cámara puntual no es modo completo","La cobertura señala momentos en que cambia brevemente la perspectiva para mirar el móvil o un objeto. Eso no equivale a un ajuste general para recorrer Leonida, combatir y conducir desde primera persona. La página oficial no anuncia un modo completo."),
("El glitch puede desaparecer","PC Gamer publicó un método de comunidad que aprovecha una interacción para quedarse en esa vista. Es no oficial, puede fallar y un parche puede corregirlo. No lo uses para juzgar el soporte de cámara ni asumas que Rockstar lo considera una función."),
("Alternativas más seguras","Ajusta distancia de cámara, vibración y controles desde el menú. Si pruebas un glitch, guarda manualmente y asume que tendrás que reiniciar o cargar de nuevo. Evitamos copiar secuencias de botones sin pruebas actuales, porque pueden quedar obsoletas en una actualización.")
],"A la fecha de revisión no hay modo completo oficial documentado. La vista breve y el glitch reportado son cosas distintas.",
[("¿Se puede jugar todo GTA VI en primera persona desde Ajustes?","Las fuentes consultadas no describen un modo completo oficial."),("¿Qué es el método de vídeos?","Un glitch reportado, no una función confirmada por Rockstar."),("¿Puede dejar de funcionar?","Sí, una actualización puede corregir un glitch.")],
["firstperson","world"],"guías",("camara","primera-persona","glitch"))

add("gta-6-coches-rapidos-estadisticas","Mejores coches de GTA VI según las primeras fichas de estadísticas",
"Comparativa provisional basada en fichas vistas en GTA VI: ratings de pista y límites del ranking.",
"El indicador Speed no es una prueba de velocidad máxima. Esta selección explica qué se ha medido y qué sigue abierto.",
"GTA Vice Guides publicó una comparación basada en tarjetas vistas entre el prólogo y los primeros capítulos. Es útil para orientarse, pero el propio medio reconoce que la lista es provisional y muchos coches aún no tienen ficha. Los ratings ayudan a elegir para un circuito; no son km/h ni una clasificación universal.",
[
("Qué significa la comparación","La guía recoge valores de Speed y ratings de carretera o campo a través. Esos datos ayudan a elegir un vehículo según el terreno, pero no son velocidad máxima medida. Su muestra incluye coches alquilables y de historia temprana, no toda la flota."),
("Vehículos destacados en esa muestra","El Bravado '19 Buffalo aparece con rating de carretera 706 y Speed 6,9. El Dinka Sugoi destaca en el circuito mixto descrito por la guía; la Maibatsu Sanchez tiene el mayor rating off-road de esa muestra. El Vapid '70 Ganado y el Declasse '72 Tulip son vehículos de historia, con información comparable incompleta."),
("Elige por carrera y disponibilidad","Para asfalto, revisa rating de carretera y requisitos del evento; para tierra, compara off-road. Considera coste, acceso y si se puede conservar: la guía dice que el Buffalo de alquiler no se guarda. Repite la comparación en la misma versión y con modificaciones equivalentes antes de concluir que un modelo es más rápido.")
],"El ranking inicial es una instantánea de fichas, no una tabla de velocidades máximas. Úsalo para elegir según superficie y confirma los datos después de actualizaciones.",
[("¿Cuál es el coche más rápido?","No se deduce de estas fichas; Speed no equivale a velocidad máxima medida."),("¿Cuál tiene mejor rating de asfalto en esta muestra?","GTA Vice Guides cita el Buffalo con 706."),("¿Cuál destaca en tierra?","La guía destaca la Sanchez por rating off-road, pero la muestra es provisional.")],
["stats","cars"],"vehículos",("coches","estadisticas","velocidad"),False,{
"table_after":2,"table":{"caption":"Muestra inicial publicada por GTA Vice Guides; no son velocidades máximas.",
"headers":["Vehículo","Uso señalado","Dato publicado","Límite"],
"rows":[["Bravado '19 Buffalo","Asfalto","Rating 706; Speed 6,9","Alquiler; no se conserva, según guía"],["Dinka Sugoi","Rallycross","Rating carretera 654; off-road 667","Ficha inicial"],["Maibatsu Sanchez","Campo a través","Rating off-road 715","Muestra parcial"],["Vapid '70 Ganado","Coche de Jason","Rating carretera 492 tras restauración","No compara mejoras idénticas"],["Declasse '72 Tulip","Vehículo personal","Ficha aún no mostrada","Sin rating en fuente"]]}})

add("gta-6-vehiculos-ultimate-edition","Vehículos de la Ultimate Edition de GTA VI: qué está confirmado",
"Qué vehículos se asocian a la Ultimate Edition de GTA VI y cómo separar un extra de edición del catálogo general.",
"Rockstar muestra una selección de vehículos y extras. Comprueba el detalle regional antes de comprar una edición.",
"Las ediciones especiales pueden mezclar vehículos, ropa, actividades y ubicaciones. PC Gamer identifica varios vehículos y el progreso necesario para acceder a algunos; Rockstar publica capturas oficiales del contenido. Esta guía informa de lo mostrado sin asumir que cada modelo sea exclusivo o que todas las tiendas ofrezcan las mismas condiciones.",
[
("Contenido de edición no es todo el catálogo","Que un coche aparezca en la galería Ultimate no demuestra que sea exclusivo de esa edición. PC Gamer describe recompensas y puntos de acceso que dependen del progreso. Comprueba la ficha de tu región y las condiciones de compra, sobre todo si compraste el juego después de una promoción."),
("Modelos identificados","Entre los vehículos nombrados en materiales promocionales están Dinka Enduro, Crest Kayak, Shitzu Squalo, '67 Vapid Dominator Buggy y '95 Grotti Cheetah. PC Gamer sitúa algunos en capítulos posteriores: el buggy tras progresar en capítulo 2 y el Squalo en capítulo 4. Es contenido de guías, no inventario oficial exhaustivo."),
("Extras de otro tipo","La guía también agrupa ropa, armas decorativas, garajes, tiendas y actividades. Sepáralos de los vehículos para no comprar esperando solo coches. Revisa qué contenido aparece en tu edición, qué depende del capítulo y qué es cosmético.")
],"El material promocional confirma varios nombres, pero Ultimate Edition no equivale al catálogo completo. Confirma edición, región y desbloqueos antes de comprar.",
[("¿El Dinka Enduro está confirmado?","Sí, aparece en materiales oficiales de GTA VI."),("¿El Squalo está desde el inicio?","PC Gamer sitúa el acceso en capítulo 4 dentro de la guía de Ultimate Edition."),("¿Todos esos vehículos son exclusivos?","No afirmamos exclusividad solo por aparecer en un paquete promocional.")],
["ultimate","media","launch"],"vehículos",("ultimate-edition","vehículos","extras"))

add("gta-6-barcos-acuaticos-confirmados","Barcos y vehículos acuáticos de GTA VI: modelos mostrados",
"Repaso de modelos acuáticos identificados en fuentes oficiales y guías: kayak, lancha, motos de agua y aerodeslizador.",
"Hay navegación en Leonida, pero no una lista definitiva del rendimiento de cada modelo.",
"Rockstar y las guías de lanzamiento muestran embarcaciones y actividades acuáticas, pero eso no permite ordenar su velocidad ni confirmar todas las ubicaciones. Esta lista separa nombres en materiales oficiales de categorías que aparecen en imágenes, y recuerda que disponibilidad puede depender del capítulo o edición.",
[
("Modelos con nombre","Rockstar identifica Crest Kayak y Shitzu Squalo en sus materiales. PC Gamer explica que el Squalo aparece como beneficio de Ultimate Edition en un punto posterior. Un nombre promocional no implica que cada jugador lo reciba automáticamente ni que sea el mejor en el agua."),
("Tipos de navegación","GamesRadar enumera deportes acuáticos, kayak, motos de agua y navegación. También aparecen aerodeslizadores en entornos naturales. Esto confirma variedad, no una lista completa de modelos. Las fuentes consultadas no ofrecen mediciones homogéneas de aceleración, autonomía o velocidad."),
("Cómo actualizar la guía","Anota el nombre tal como aparece en el juego, región, capítulo y si el vehículo es personal o parte de una actividad. Si una captura no muestra nombre, descríbelo como categoría visual, sin asignarle un fabricante por semejanza. Así la lista crece con hallazgos comprobables.")
],"Los materiales confirman modelos y actividades, no un ranking. Usa la fuente oficial para nombres y pruebas fechadas para comparar rendimiento.",
[("¿Hay kayak?","Sí, Rockstar identifica el Crest Kayak."),("¿Qué es Shitzu Squalo?","Una embarcación de la Ultimate Edition; la guía de PC Gamer detalla un acceso posterior."),("¿Cuál es la lancha más rápida?","No se publica un ganador sin mediciones comparables.")],
["media","ultimate","activities"],"vehículos",("barcos","agua","kayak"))

add("gta-6-duracion-historia-cuanto-se-tarda","¿Cuánto dura la historia de GTA VI? Qué dicen los primeros análisis",
"La duración depende del estilo de juego. Reunimos estimaciones iniciales y separamos campaña directa de exploración.",
"No existe una duración oficial única: las horas dependen de cuánto contenido secundario hagas.",
"Rockstar no publica una cifra universal de horas para completar GTA VI. Los análisis describen una campaña extensa y un mundo con actividades que alargan la partida. Windows Central estima unas 50 horas para ir por la historia ignorando buena parte del contenido lateral; es la experiencia del medio, no una garantía.",
[
("Una estimación no es promesa","La cifra de Windows Central ronda 50 horas para una partida centrada en historia. Cambia según exploración, conducción, escenas, búsquedas y pausas. No es un promedio estadístico: describe el recorrido de un reseñista."),
("La exploración cambia el total","TechRadar y AP destacan misiones junto a actividades y descubrimientos. Si te detienes a explorar, seguir personajes o participar en contenido opcional, el total aumenta. Las listas de capítulos cuentan tareas de maneras distintas, así que no uses una cantidad de misiones como conversión exacta a horas."),
("Estima tu partida sin spoilers","Anota horas y capítulo, separando tiempo de historia y tiempo libre. Si quieres una respuesta sin spoilers, evita listas completas de misiones. Compara análisis de personas con un estilo parecido al tuyo y trata cada tiempo como una referencia individual.")
],"Un análisis estima unas 50 horas si se corre por la historia, pero el tiempo propio depende de cuánto explores. No hay una duración oficial única.",
[("¿Cuántas horas dura?","Windows Central estima alrededor de 50 para una partida centrada en la historia; no es garantía."),("¿Cuánto dura al completar todo?","No hay cifra completa y comparable verificada en las fuentes consultadas."),("¿Las actividades alargan la partida?","Sí; los análisis describen exploración y actividades fuera de la historia.")],
["windows","tech","ap"],"análisis",("duracion","horas","campaña"))

add("gta-6-jason-duval-biografia","Jason Duval en GTA VI: biografía, pasado y relación con Leonida",
"Quién es Jason Duval según Rockstar: su pasado militar, su vida en los Keys y su vínculo con Lucia.",
"Una ficha sin spoilers sobre el protagonista, construida con la información oficial.",
"Jason Duval comparte el protagonismo de GTA VI con Lucia Caminos. Rockstar describe una juventud rodeada de estafadores, un paso por el ejército y un trabajo posterior para traficantes en los Keys. La biografía da contexto, no un resumen de su arco completo. Esta página separa lo que se anunció de lo que solo puede conocerse jugando.",
[
("El pasado oficial","Rockstar cuenta que Jason creció entre estafadores y delincuentes, se alistó en el ejército intentando apartarse de una adolescencia difícil y terminó trabajando para traficantes locales. El retrato lo presenta buscando una vida más sencilla, pero no confirma qué decisiones tomará durante la campaña."),
("Su conexión con Brian y Lucia","La página oficial relaciona a Jason con Brian Heder y el contrabando de los Keys. También presenta a Lucia como alguien cuyo encuentro puede ser decisivo para él. La premisa del lanzamiento sitúa a ambos en una conspiración criminal y subraya que deben apoyarse."),
("Qué sigue abierto","La biografía no revela su trayectoria completa, motivaciones durante el juego ni desenlace. Para una lectura sin spoilers, compara la sinopsis oficial con escenas jugadas y evita listas de misiones. Esta ficha solo cambiará con nueva información publicada por Rockstar.")
],"Jason se presenta como exmilitar vinculado al contrabando de los Keys y coprotagonista junto a Lucia. Su arco completo se descubre en la historia.",
[("¿Quién es Jason Duval?","Un protagonista con pasado militar y trabajo para traficantes de los Keys, según Rockstar."),("¿Jason es pareja de Lucia?","Rockstar presenta a ambos como una pareja cuya confianza es central."),("¿Esta ficha cuenta el final?","No; resume solo la biografía promocional.")],
["world","launch"],"personajes",("jason-duval","protagonistas"))

add("gta-6-lucia-caminos-biografia","Lucia Caminos en GTA VI: pasado, objetivos y lo confirmado",
"Biografía de Lucia Caminos: su familia, su estancia en la prisión de Leonida y el plan para cambiar su situación.",
"Rockstar presenta a Lucia como una protagonista decidida a cambiar las probabilidades a su favor.",
"Lucia Caminos comparte el protagonismo con Jason. Rockstar explica que aprendió a luchar desde niña, que los problemas relacionados con su familia la llevaron a prisión y que ahora quiere tomar decisiones calculadas para buscar una vida mejor. La ficha no revela todas las razones de su historia ni su final.",
[
("Una protagonista con objetivo propio","Rockstar describe el deseo de Lucia de lograr la vida que su madre imaginaba para la familia. También la presenta dispuesta a actuar en vez de esperar que cambie su situación. Es su punto de partida, no un resumen de lo que ocurre después."),
("Pasado y prisión","La web oficial señala que su padre le enseñó a luchar pronto y que una pelea por su familia terminó llevándola a la Leonida Penitentiary. Su salida se atribuye a la suerte. La fuente no detalla el caso completo, así que no añadimos delitos ni circunstancias no descritas."),
("Lucia y Jason","La presentación oficial vincula sus planes a la relación con Jason y al crimen que recorre Leonida. AP también caracteriza la historia como centrada en una pareja, aunque esa crítica no reemplaza los hechos. Evitamos decisiones y consecuencias que dependan del progreso.")
],"Lucia parte de una historia familiar y penitenciaria y de un objetivo claro: cambiar su situación. Esta ficha se limita a la biografía oficial.",
[("¿Por qué estuvo en prisión?","Rockstar lo relaciona con una pelea por su familia, sin publicar todos los detalles en la bio."),("¿Lucia es protagonista jugable?","Sí, comparte el protagonismo con Jason."),("¿La página revela el final?","No; resume solo el punto de partida divulgado oficialmente.")],
["world","launch","ap"],"personajes",("lucia-caminos","protagonistas"))

add("gta-6-cal-hampton-quien-es","Cal Hampton en GTA VI: quién es el amigo de Jason",
"Biografía oficial de Cal Hampton: amistad con Jason, vínculo con Brian y personalidad conspirativa.",
"Cal aporta un contraste cómico en el círculo de Jason; sus teorías no son automáticamente pistas del juego.",
"Cal aparece en la presentación oficial como amigo de Jason y asociado de Brian. Rockstar lo describe en casa, escuchando comunicaciones de la Guardia Costera y siguiendo teorías de internet. Ese retrato permite leerlo como parte del tono satírico, pero no convierte cada frase suya en una pista o un secreto confirmado.",
[
("Su lugar en el círculo","Rockstar define a Cal como amigo de Jason y asociado de Brian. La relación lo conecta con los Keys, aunque su biografía no enumera todas sus misiones. Es una base para entender quién aparece en la órbita del protagonista, no un mapa completo de alianzas."),
("Una personalidad desconfiada","La página oficial lo presenta pendiente de comunicaciones y teorías conspirativas. El humor nace de esa desconfianza, pero Cal no es necesariamente un narrador fiable. Si afirma algo sobre fauna, autoridades o fenómenos extraños, comprueba si el juego lo demuestra antes de llamarlo secreto."),
("Qué sabemos y qué no","La ficha no anticipa su destino ni el alcance de su participación. Tampoco confirma que cada comentario desbloquee una misión. Los artículos con contexto de campaña deben indicar el capítulo; esta página sirve antes de empezar.")
],"Cal está ligado a Jason y Brian y se caracteriza por sus teorías conspirativas. Sus comentarios no confirman por sí solos que una teoría sea cierta.",
[("¿Cal es amigo de Jason?","Sí, así lo describe Rockstar."),("¿Qué relación tiene con Brian?","La presentación oficial los llama asociados."),("¿Las teorías de Cal son pistas?","No necesariamente; Rockstar lo define como paranoico.")],
["world","launch"],"personajes",("cal-hampton","personajes-secundarios"))

add("gta-6-boobie-ike-quien-es","Boobie Ike en GTA VI: negocios, música y alianza con Dre'Quan",
"Quién es Boobie Ike: sus negocios en Vice City, el estudio de grabación y la relación profesional con Dre'Quan Priest.",
"Rockstar presenta a Boobie como una figura local que ha convertido su pasado callejero en negocios legales y criminales.",
"Boobie Ike es uno de los personajes secundarios destacados en la web de GTA VI. Rockstar lo define como una leyenda local de Vice City con negocios inmobiliarios, un club y un estudio de grabación. Su relación con Dre'Quan conecta la economía criminal y la música. Esta ficha explica su premisa sin revelar el arco.",
[
("Un empresario con varias fachadas","La bio oficial dice que Boobie convirtió su tiempo en la calle en un imperio de bienes raíces, un club y un estudio. El retrato muestra negocios con distintos orígenes. No damos por hecho que el jugador pueda administrar esas empresas."),
("Only Raw Records","Rockstar presenta la alianza de Boobie con Dre'Quan alrededor del sello. El estudio necesita un éxito y la firma de Real Dimez abre una etapa nueva. Esa conexión convierte la música en parte del tejido social de Vice City, además de la radio."),
("Cómo leer su papel sin spoilers","La bio no resume todas sus misiones. Los artículos que desarrollen la alianza deben advertir antes de revelar escenas. Esta ficha usa solo el punto de partida promocional y no afirma que el jugador pueda cambiar libremente la plantilla del sello.")
],"Boobie representa el cruce entre negocios, ocio y crimen en Vice City; su alianza con Dre'Quan conecta esa trama con la música.",
[("¿Qué negocios tiene?","Rockstar enumera bienes raíces, un club y un estudio."),("¿Qué relación tiene con Dre'Quan?","Son socios de Only Raw Records, según la web oficial."),("¿Boobie es protagonista?","No; Rockstar lo presenta como personaje secundario.")],
["world","launch"],"personajes",("boobie-ike","vice-city","musica"))

add("gta-6-drequan-priest-only-raw","Dre'Quan Priest y Only Raw Records en GTA VI",
"Dre'Quan Priest busca abrirse paso en la música de Vice City. Repasamos su vínculo con Boobie Ike y Real Dimez.",
"Su objetivo musical lo distingue de la ruta criminal tradicional de su entorno.",
"Rockstar presenta a Dre'Quan Priest como alguien más interesado en abrirse camino en la música que en ser un gánster. Su camino se cruza con Boobie Ike, el sello Only Raw Records y el dúo Real Dimez. Esta ficha recoge lo oficial y no completa con rumores el catálogo de artistas o los resultados de su ambición.",
[
("Una meta centrada en la música","Rockstar lo describe como un buscavidas que, incluso cuando comerciaba en la calle, quería entrar en la industria musical. Su objetivo no lo separa completamente del crimen; su historia arranca dentro de esa economía."),
("Boobie Ike y el sello","Dre'Quan trabaja con Boobie en Only Raw Records. La biografía sugiere que podría dejar de reservar artistas en el club de Boobie mientras busca oportunidades en la escena. Es una relación narrativa conocida; no implica que puedas crear un sello o cambiar su plantilla."),
("La oportunidad de Real Dimez","La web oficial informa que ficha a Bae-Luxe y Roxy. Ese vínculo conecta la ambición del productor con la presencia online de las artistas. Para saber cómo evoluciona, hay que avanzar en la campaña.")
],"Dre'Quan conecta el mundo musical con el negocio de Boobie y la oportunidad de Real Dimez, según la presentación oficial.",
[("¿Qué es Only Raw Records?","El sello vinculado a Boobie Ike y Dre'Quan Priest."),("¿Dre'Quan ficha a Real Dimez?","Sí, la bio oficial dice que las firma."),("¿El artículo contiene spoilers?","No; resume objetivos y relaciones promocionales.")],
["world","launch"],"personajes",("drequan-priest","only-raw-records","musica"))

add("gta-6-real-dimez-bae-luxe-roxy","Real Dimez en GTA VI: Bae-Luxe, Roxy y su salto a Only Raw",
"Quiénes son Bae-Luxe y Roxy: su amistad, música y estrategia de viralidad en GTA VI.",
"El dúo convierte una presencia online en una oportunidad musical y un contrato con Only Raw Records.",
"Real Dimez está formado por Bae-Luxe y Roxy, amigas desde el instituto según Rockstar. La biografía combina rap, vídeos virales y redes sociales. Tras un primer éxito con DWNPLY, ambas firman con Only Raw Records. Esta ficha se concentra en su trasfondo oficial y no presume que cada aplicación sea una mecánica jugable.",
[
("De la amistad a una identidad musical","Rockstar las presenta como amigas y artistas que desarrollaron presencia online. El trabajo en pareja forma parte de su identidad. La web oficial todavía no ofrece una discografía completa ni una bio individual extensa de cada integrante."),
("El primer éxito y el contrato","La biografía menciona una canción con DWNPLY que les dio proyección local. Después de varios años, el dúo firma con Only Raw Records, asociado a Boobie Ike y Dre'Quan. La ficha no adelanta el resultado de esa apuesta."),
("Redes como parte de la sátira","Rockstar describe música y viralidad como parte del concepto del dúo. Creative Bloq observa una sátira de redes y fama en el juego, pero eso no confirma cada función de las aplicaciones. Mantén separado el marketing del personaje de los sistemas interactivos.")
],"Real Dimez es un dúo de amigas y artistas fichadas por Only Raw; Rockstar las describe mediante música, viralidad e historia compartida.",
[("¿Quiénes forman Real Dimez?","Bae-Luxe y Roxy."),("¿Con quién colaboraron antes de Only Raw?","La bio menciona un tema junto a DWNPLY."),("¿Quién las ficha?","Dre'Quan Priest para Only Raw Records, según Rockstar.")],
["world","bloq"],"personajes",("real-dimez","bae-luxe","roxy"))

add("gta-6-raul-bautista-personaje","Raul Bautista en GTA VI: el atracador que busca talento",
"Rockstar presenta a Raul Bautista como atracador experimentado que busca aliados para golpes arriesgados.",
"Su perfil plantea una tensión entre experiencia, ambición y el coste de subir la apuesta.",
"Raul es parte del reparto anunciado por Rockstar. La compañía lo caracteriza por confianza, encanto y astucia, y lo describe como un atracador veterano que busca personas dispuestas a correr riesgos. También señala que su temeridad puede elevar las apuestas. Esta ficha resume su premisa sin atribuirle capítulos o desenlaces no publicados.",
[
("Experiencia y reclutamiento","La ficha oficial lo presenta buscando talento para golpes arriesgados. Su experiencia lo define como reclutador, pero la página no confirma qué decisiones tomará el jugador. Mantén separados el concepto del personaje y la mecánica de selección de equipo."),
("La temeridad","Rockstar dice que su imprudencia eleva el riesgo con cada golpe y que el equipo tendrá que aumentar la apuesta o retirarse. Es una descripción de tono, no el resultado de la campaña. No basta para predecir traiciones o finales."),
("Qué aporta al grupo","Raul amplía el lado profesional del crimen y abre preguntas sobre confianza y planificación. Para evitar spoilers, esta página se limita a la bio oficial. Un futuro perfil de campaña debe indicar qué capítulo revela cada dato.")
],"Raul se define por experiencia, reclutamiento y tendencia a elevar las apuestas. El resto de su arco requiere contexto y aviso de spoilers.",
[("¿Quién es Raul?","Un atracador de bancos experimentado presentado por Rockstar."),("¿Qué busca?","Talento dispuesto a asumir riesgos en golpes."),("¿La ficha adelanta su final?","No; resume la descripción oficial.")],
["world","launch"],"personajes",("raul-bautista","atracos"))

add("gta-6-brian-heder-personaje","Brian Heder en GTA VI: el vínculo de Jason con los Keys",
"La biografía de Brian Heder: su pasado de contrabandista, el astillero y la relación de conveniencia con Jason.",
"Brian pertenece a una generación anterior del contrabando de los Keys y utiliza a Jason para sus encargos locales.",
"Brian conecta a Jason con los Keys y con una generación de contrabandistas. Rockstar lo describe manteniendo actividad desde un astillero con Lori y dejando que otras personas hagan el trabajo sucio. También explica que Jason vive en una propiedad de Brian a cambio de colaborar en cobros locales. Esta ficha no es un resumen de toda su historia.",
[
("Veterano del contrabando","Rockstar presenta a Brian como contrabandista de la etapa clásica que sigue moviendo mercancía desde su astillero. La bio lo retrata cómodo delegando y protegiendo su posición. No afirmamos que el jugador pueda administrar el negocio como actividad libre."),
("La vivienda y las tareas de Jason","La web oficial dice que Brian permite que Jason viva sin pagar alquiler en una de sus propiedades, siempre que ayude con cobros locales. Es una relación de intercambio, no familiar. Esa premisa conecta la vida cotidiana de Jason con la economía criminal regional."),
("Relación con otros personajes","Brian también es asociado de Cal Hampton, según la presentación de Cal. La relación ayuda a entender la red de Jason, aunque la web no detalla el pasado de Lori ni el destino del astillero.")
],"Brian es un contrabandista veterano que presta vivienda a Jason a cambio de ayuda local. Su papel conecta la historia con los Keys.",
[("¿Quién es Brian Heder?","Un contrabandista veterano ligado a los Keys y asociado de Jason."),("¿Dónde vive Jason al principio?","Rockstar dice que Brian le deja una propiedad sin alquiler."),("¿Qué relación tiene con Cal?","La bio de Cal los presenta como asociados.")],
["world","launch"],"personajes",("brian-heder","keys","jason"))

add("gta-6-leonida-keys-zona","Leonida Keys en GTA VI: qué zona aparece y qué se ha confirmado",
"Guía sin mapa inventado de Leonida Keys: qué confirma Rockstar y qué pistas visuales no prueban mecánicas.",
"Rockstar presenta los Keys como parte de Leonida y vincula la zona al trabajo de Jason y Brian.",
"Leonida Keys es una de las regiones identificadas por Rockstar. La biografía de Jason lo vincula a traficantes locales y la de Brian a un astillero y una tradición de contrabando. La web ofrece postales y materiales visuales, pero no una guía de cada carretera. Aquí separamos el dato de la exploración pendiente.",
[
("Qué confirma Rockstar","La zona forma parte de Leonida y aparece como destino oficial. Las biografías de Jason y Brian la conectan al contrabando local; las imágenes presentan costa e islas. No asignamos rutas o coordenadas porque la fuente no ofrece una guía navegable."),
("Leer el paisaje con cuidado","Una postal permite reconocer el tono, pero no siempre enseña el punto exacto del mapa. Al jugar, anota el nombre de interfaz y la versión. Llama aproximación a una marca de fans hasta comprobarla en la partida."),
("Jason, Brian y la región","La vivienda de Jason y los cobros locales conectan los Keys con su historia. Las actividades concretas deben verificarse por separado. Actualizaremos la guía cuando haya información oficial o pruebas reproducibles.")
],"Rockstar vincula los Keys a Jason y Brian, pero no ofrece una cartografía jugable completa en su página promocional.",
[("¿Leonida Keys es oficial?","Sí, aparece entre los destinos de Rockstar."),("¿Es el único escenario?","No; Leonida incluye varias regiones."),("¿Hay coordenadas en esta página?","No; no se deducen de una postal.")],
["world","media"],"lugares",("leonida-keys","mapa","regiones"))

add("gta-6-port-gellhorn-zona","Port Gellhorn en GTA VI: lo confirmado de esta región",
"Rockstar incluye Port Gellhorn entre los destinos de Leonida. Separamos la región confirmada de mapas especulativos.",
"Port Gellhorn aparece en la galería oficial; su mapa detallado debe comprobarse dentro de la partida.",
"Port Gellhorn es uno de los nombres propios que Rockstar asocia a Leonida. La página promocional lo incluye entre los destinos y la galería conserva capturas identificadas con ese nombre. Esto confirma que la región forma parte del mundo, pero no basta para deducir sus barrios, misiones o actividades.",
[
("Nombre y evidencia","Rockstar enumera Port Gellhorn y agrupa capturas bajo ese nombre. La evidencia confirma una región con esa denominación; una imagen no revela escala, conexiones de carretera ni acceso permanente."),
("Qué observar al llegar","Compara el rótulo del mapa con carteles y nombres de la partida. Si una guía atribuye una tienda o misión concreta, exige capítulo o fuente de gameplay. No ubiques un comprador o actividad solo por una postal."),
("Postal frente a ruta","Las descargas oficiales sirven de referencia visual, no como mapa completo con interiores. Para una ruta reproducible, consulta el mapa del juego y anota puntos descubiertos. Añadiremos detalles con fuentes verificables.")
],"Port Gellhorn está confirmado como destino oficial de Leonida. Las rutas y actividades se añaden cuando el juego o una guía las documentan.",
[("¿Port Gellhorn aparece en GTA VI?","Sí; Rockstar lo identifica entre los destinos."),("¿La postal oficial muestra todas las carreteras?","No, es material promocional."),("¿Puedo fiarme de cualquier mapa de fans?","Comprueba su versión y fuente; puede ser especulativo.")],
["world","media"],"lugares",("port-gellhorn","mapa","regiones"))

add("gta-6-grassrivers-zona","Grassrivers en GTA VI: humedales y personajes vinculados",
"Qué se ha confirmado de Grassrivers y cómo se conecta con el reparto oficial, sin inventar puntos de interés.",
"Rockstar incluye Grassrivers entre sus destinos; el nombre no demuestra qué actividades o secretos contiene.",
"Grassrivers figura entre los lugares de Leonida presentados por Rockstar. El sitio vincula el destino a materiales del reparto, incluido Cal Hampton. El nombre evoca humedales, pero por sí solo no prueba qué animales, misiones o rutas existen. Esta página prioriza fuentes oficiales y deja las ubicaciones jugables para verificarlas dentro del juego.",
[
("Qué sabemos","Rockstar incluye Grassrivers en la lista de destinos y en la galería de capturas. Eso confirma su presencia, pero no un inventario de fauna, actividades o caminos. Si una noticia atribuye un secreto a un pantano, hace falta evidencia reproducible y contexto de capítulo."),
("El vínculo con Cal","La web oficial presenta a Cal como amigo de Jason y asociado de Brian, con interés por teorías y comunicaciones costeras. Sus materiales aparecen junto a Grassrivers, pero no inferimos que viva exclusivamente allí ni que una captura sea su domicilio."),
("Explora sin falsos datos","Registra el nombre del mapa, punto de entrada y condiciones. Una guía de fans puede servir como pista, pero hay que verificarla antes de presentar coordenadas como definitivas. No publicamos mapa de calor ni lista de secretos sin prueba.")
],"Grassrivers es un destino oficial; sus detalles jugables deben verificarse en la partida y no deducirse del nombre.",
[("¿Grassrivers está en Leonida?","Sí, Rockstar lo incluye."),("¿Cal vive allí?","La web lo presenta junto a material de la región, pero no afirma residencia exclusiva."),("¿Hay lista oficial de secretos?","No en las fuentes consultadas.")],
["world","media"],"lugares",("grassrivers","mapa","regiones"))

add("gta-6-ambrosia-zona","Ambrosia en GTA VI: lugar confirmado y datos que faltan",
"Ambrosia es uno de los destinos oficiales de Leonida. Separamos la región de ubicaciones y actividades todavía no documentadas.",
"Una guía de contexto para reconocer Ambrosia y añadir descubrimientos con evidencia reproducible.",
"Ambrosia aparece entre los destinos de Leonida en la web oficial y en la galería de capturas. Esos datos confirman una región, pero no permiten afirmar qué misiones, negocios o secretos contiene. Esta página marca el límite y explica cómo convertir una observación en una referencia útil.",
[
("Presencia oficial","Rockstar enlaza Ambrosia como destino y la incluye en su colección visual. Eso la diferencia de un nombre inventado en un mapa de fans. La página no ofrece un inventario de barrios ni un plano calle a calle."),
("Qué falta para una guía jugable","Documentar una ubicación requiere el nombre exacto en el juego, cómo llegar, si depende de historia y qué actividad ocurre allí. Una captura puede mostrar arquitectura, no probar horarios o recompensas. No asignamos esas características a Ambrosia sin fuente."),
("Cómo registrar un hallazgo","Anota versión, plataforma, punto marcado en el mapa y los pasos para reproducirlo. Si contiene un giro, añade aviso antes. Así podemos incorporar descubrimientos con fecha sin convertir una teoría viral en dato.")
],"Ambrosia está confirmada como destino. La información granular se añadirá cuando exista una fuente oficial o prueba en juego contrastable.",
[("¿Ambrosia es un lugar oficial?","Sí, Rockstar la incluye."),("¿Qué actividades hay?","No enumeramos actividades sin una guía verificable."),("¿Una captura prueba un secreto?","Puede mostrar una escena, no necesariamente sus condiciones o ubicación exacta.")],
["world","media"],"lugares",("ambrosia","mapa","regiones"))

add("gta-6-mount-kalaga-zona","Mount Kalaga en GTA VI: qué muestra Rockstar del parque nacional",
"Mount Kalaga National Park es una zona nombrada oficialmente. Reunimos evidencia disponible y los límites de las postales.",
"El nombre identifica una región; senderos, rutas y especies deben confirmarse dentro del juego.",
"Rockstar incluye Mount Kalaga National Park en Leonida y en su galería. Las imágenes permiten reconocer un entorno natural, pero no son una guía de senderos ni prueban qué fauna o actividades existen. Esta página sirve como punto de partida y separa paisaje mostrado de datos jugables.",
[
("Nombre y contexto oficial","Mount Kalaga National Park aparece entre los destinos de GTA VI. Rockstar lo sitúa dentro de un estado con regiones distintas a Vice City. No publicamos superficie, altitud ni una equivalencia exacta con un parque real."),
("El vehículo de edición especial","PC Gamer vincula el Dominator Buggy de Ultimate Edition con el terreno de Mount Kalaga y alrededores. Ese ejemplo depende de edición y progreso; no significa que el buggy sea necesario para entrar al parque."),
("Qué confirmar jugando","Registra nombre, hora, acceso y capítulo al encontrar una actividad o animal. La galería ayuda a reconocer ambientes, no a fijar coordenadas. Evita mapas que dibujan carreteras o secretos sin evidencia.")
],"Mount Kalaga es una región confirmada. Las capturas muestran su entorno; una guía menciona un buggy especial, pero no hay mapa completo de rutas.",
[("¿Mount Kalaga aparece en el juego?","Sí, Rockstar lo identifica como destino."),("¿Necesito el Dominator Buggy?","No; PC Gamer lo relaciona con el terreno, no como requisito de acceso."),("¿Hay coordenadas oficiales detalladas?","No encontramos una cartografía oficial de coordenadas.")],
["world","media","ultimate"],"lugares",("mount-kalaga","parque","mapa"))

add("gta-6-easter-egg-little-sam","El easter egg de Little Sam en GTA VI: qué aparece y qué es teoría",
"GamesRadar reporta una aparición llamada Little Sam en Boobie Time. Te contamos qué se ve y por qué su identidad sigue siendo una lectura.",
"Aviso de spoiler leve: la referencia aparece durante una misión del capítulo 3.",
"GamesRadar informó de una posible referencia a Sam Houser durante Boobie Time. El personaje aparece llamado Little Sam y el artículo lo compara con una figura menor de GTA III asociada por jugadores al cofundador de Rockstar. El medio mantiene cautela, así que no lo etiquetamos como confirmación oficial del estudio.",
[
("Aviso antes de la escena","Esta guía menciona Boobie Time, del capítulo 3, y el nombre Little Sam. Si aún no llegaste ahí, vuelve después de jugar. GamesRadar sitúa la aparición cuando Jason conecta con Boobie Ike; no contamos el resto del encargo."),
("Qué reportó el medio","El artículo observa a una figura llamada Little Sam y recoge la interpretación de jugadores que la relacionan con Sam Houser y una referencia a GTA III. La redacción es prudente: parece un cameo y recuerda una identificación discutida por la comunidad. No encontramos declaración de Rockstar confirmando la identidad."),
("Cómo clasificarlo","La escena puede estar documentada por gameplay, pero la intención del homenaje y la identidad detrás del apodo siguen siendo interpretación. El estado correcto es referencia reportada o posible easter egg, no personaje confirmado como Sam Houser.")
],"Little Sam se ha reportado en Boobie Time; vincularlo con Sam Houser es una interpretación, no una confirmación oficial.",
[("¿Dónde aparece?","GamesRadar lo sitúa en Boobie Time, capítulo 3."),("¿Rockstar confirmó que es Sam Houser?","No en las fuentes consultadas."),("¿Hay spoilers?","Sí, se menciona una misión del capítulo 3.")],
["sam","world"],"secretos",("easter-egg","little-sam","spoilers"),"Aviso: contiene spoilers leves del capítulo 3 y analiza una referencia no confirmada como teoría.")

add("gta-6-vida-cotidiana-detalles-mundo","Los detalles cotidianos que hacen que Leonida parezca vivida",
"Qué observan los primeros análisis en GTA VI: gimnasios, paseos, conversaciones y actividad social.",
"La vida del mundo no se mide solo por el tamaño del mapa. Atribuimos las observaciones a sus reseñistas.",
"Los análisis de GTA VI destacan situaciones pequeñas junto a los atracos: personajes que pasean, entrenan, conversan y reaccionan al entorno. AP y Creative Bloq ofrecen ejemplos. Esta pieza no pretende verificar cada NPC ni usar adjetivos como hechos; explica qué describieron los medios y por qué pueden influir en la sensación de mundo abierto.",
[
("Rutinas entre misiones","AP menciona acciones tranquilas como ir al gimnasio, caminar juntos y pasar tiempo sin una misión de alto riesgo. Creative Bloq describe escenas sociales y respuestas de personas en la calle. Son ejemplos de reseñas en consola; no prueban que cada actividad esté disponible en cualquier zona."),
("El entorno como fuente de historias","Creative Bloq destaca carteles, conversaciones, objetos legibles y situaciones callejeras que pueden llevar la atención hacia lugares o personajes. Así parte de la exploración surge de observar, no solo seguir un marcador. Es una valoración del medio; otro jugador puede priorizar combate o conducción."),
("Cómo evaluar el detalle","Para distinguir decoración de interacción, mira si responde a tus acciones, reaparece o conecta con otro objetivo. Anota capítulo y actividad. Una imagen promocional enseña un instante seleccionado; una observación reproducible en partida es una evidencia más sólida.")
],"Las reseñas destacan vida cotidiana además de acción. El valor depende de cómo los detalles conectan con la exploración, no de contarlos como mecánicas.",
[("¿Qué momentos cotidianos menciona AP?","Gimnasio, caminar y pasar tiempo juntos, entre otros."),("¿Todos los carteles desbloquean misiones?","No; una reseña menciona que algunos elementos llevan a personajes o historias."),("¿Es una prueba propia?","No; es una síntesis atribuida a análisis publicados.")],
["ap","bloq","tech"],"análisis",("mundo-vivo","detalles","exploracion"))

add("gta-6-analisis-reviews-lanzamiento","GTA VI en los primeros análisis: mundo, personajes y ritmo",
"Síntesis de reseñas de GTA VI: qué destacan AP, TechRadar y Windows Central y qué matices conviene considerar.",
"Una lectura cruzada de críticas de lanzamiento, sin copiar puntuaciones ni convertir gustos individuales en consenso.",
"Los primeros análisis describen un mundo abierto ambicioso, pero cada medio resalta elementos distintos. AP centra su valoración en la pareja protagonista; TechRadar destaca inmersión y variedad; Windows Central comenta su prueba en Xbox Series X. Esta síntesis resume temas recurrentes y diferencias de perspectiva, no sustituye una reseña propia.",
[
("Qué valoran varias reseñas","Las fuentes destacan la presentación de Leonida y la atención al entorno. AP elogia la relación de Jason y Lucia; TechRadar habla de un mundo con actividades y cambios de ritmo. Son juicios críticos, no propiedades medibles ni garantía de que cada zona esté igual de llena."),
("El ritmo admite matices","AP describe alternancia entre acción y momentos tranquilos. Las primeras horas pueden sentirse pausadas para quien espera atracos constantes. Una guía de inicio responde a cómo empezar; un análisis completo explica cómo cambia la experiencia."),
("Qué mirar antes de decidir","Comprueba consola, tiempo de juego y si el análisis habla de rendimiento, narrativa o diseño. Windows Central declara que probó principalmente Xbox Series X; no extrapoles a Series S o PS5. Compara varias perspectivas y revisa la tienda regional para precio y edición.")
],"Los análisis iniciales resaltan mundo y protagonistas, pero dependen de plataforma, ritmo y preferencias. Ninguna reseña representa a todos los jugadores.",
[("¿Qué destacan los primeros análisis?","Ambientación, mundo abierto y relación entre protagonistas."),("¿Todos coinciden en el ritmo?","No exactamente; cada medio prioriza aspectos distintos."),("¿Una prueba de Series X vale igual para Series S?","No automáticamente; revisa plataforma y condiciones.")],
["ap","tech","windows"],"análisis",("reseñas","criticas","lanzamiento"))

add("gta-6-redes-sociales-telefono-satira","Redes sociales y móvil en GTA VI: qué papel tienen en la sátira",
"Los análisis observan redes, fama y teléfonos en GTA VI. Separa la crítica cultural de funciones aún no confirmadas.",
"La presencia de publicaciones dentro de Leonida no confirma que cada app sea una mecánica completa.",
"La cultura online forma parte de la ambientación de GTA VI. Creative Bloq relaciona la sátira con redes, celebridad y consumo; Rockstar presenta a Real Dimez como artistas que convierten su presencia online en oportunidad musical. Analizamos esos elementos sin inventar nombres de apps o funciones no confirmadas.",
[
("Real Dimez y la viralidad","Rockstar describe a Bae-Luxe y Roxy con rap y presencia constante en redes. Su historia enlaza fama online e industria musical. El material oficial ofrece el concepto del dúo, pero no especifica una lista completa de apps jugables."),
("La sátira del entorno","Creative Bloq observa una sátira de redes, fama y consumo, dentro de una ciudad llena de anuncios y reacciones públicas. Es una lectura crítica, no prueba de que cada mensaje de un NPC active una misión o replique una plataforma real."),
("Separa funciones y ambientación","Un feed visto en una escena acredita que está en la presentación, no que el jugador pueda publicar o buscar. Mantén una lista de herramientas probadas y otra de elementos promocionales. Así no convertimos una teoría previa al lanzamiento en dato.")
],"Las redes tienen un papel temático en las biografías y reseñas; las funciones del teléfono requieren evidencia de juego específica.",
[("¿Real Dimez está vinculada a redes?","Sí, Rockstar menciona su presencia online."),("¿GTA VI copia una app concreta?","No afirmamos equivalencias sin una fuente clara."),("¿Cada publicación del móvil da una misión?","No hay base para afirmarlo en general.")],
["world","bloq","media"],"análisis",("redes-sociales","telefono","real-dimez"))

add("gta-6-jason-lucia-relacion-analisis","Jason y Lucia en GTA VI: cómo se presenta su relación sin spoilers",
"Qué se sabe de la relación: premisa oficial, objetivos y lecturas críticas tras el lanzamiento.",
"Rockstar define a ambos como pareja que debe confiar el uno en el otro; los análisis leen el vínculo como eje narrativo.",
"La relación entre Jason y Lucia no es un detalle menor de la sinopsis: Rockstar la coloca en el centro del conflicto. Cuando un golpe sale mal, ambos quedan en una conspiración criminal y deben apoyarse. Esta lectura no revela el final; contrasta la premisa oficial con la valoración de AP.",
[
("La premisa oficial","Rockstar presenta a ambos como pareja enfrentada a circunstancias difíciles y resume el argumento alrededor de la confianza. Las biografías añaden metas propias: Jason quiere una vida sencilla y Lucia quiere cambiar sus probabilidades. La tensión nace de esos objetivos y de cómo se cruzan."),
("La mirada de la crítica","AP considera eficaz la historia de pareja y dice que el vínculo sostiene el viaje cuando sus ambiciones los llevan a más peligro. Es una opinión de reseña, no respuesta definitiva a cada escena. Leerlo como romance sencillo deja fuera crimen, supervivencia e intereses personales."),
("Qué observar al jugar","Fíjate en cómo se reparten tareas, conversaciones y decisiones fuera de misión. No supongas que un gesto aislado determina el final; hacen falta pruebas para afirmar consecuencias. Si quieres evitar spoilers, no consultes tablas de decisiones antes de completar la campaña.")
],"Rockstar sitúa la confianza en el centro y AP valora la química de la pareja. El desarrollo y sus consecuencias se descubren jugando.",
[("¿Jason y Lucia son pareja?","Sí, Rockstar presenta su historia como la de una pareja que debe apoyarse."),("¿La relación afecta al argumento?","Es central en la premisa; las consecuencias específicas dependen de la campaña."),("¿Esta página revela el final?","No.")],
["launch","world","ap"],"personajes",("jason","lucia","relacion"))

add("gta-6-detalles-analisis-lanzamiento","15 detalles de GTA VI que destacan los primeros análisis",
"Quince observaciones documentadas en reseñas y fuentes oficiales, separando escenas vistas de interpretaciones editoriales.",
"Detalles cotidianos y de diseño citados por medios, sin presentar teorías como secretos confirmados.",
"Los detalles que merecen una segunda mirada no tienen por qué ser easter eggs. Las reseñas y materiales oficiales describen interacciones y cambios de ritmo que ayudan a entender Leonida. Esta lista atribuye cada afirmación a Rockstar, AP, TechRadar, GamesRadar o Creative Bloq. Algunas son datos oficiales; otras son impresiones de reseñistas.",
[
("Del 1 al 5: el mundo más allá de misiones","1) Rockstar presenta Leonida como escenario de varias regiones. 2) Jason y Lucia son la pareja protagonista. 3) El Índice separa tareas y áreas. 4) AP observó momentos tranquilos como caminar y hacer ejercicio. 5) Creative Bloq destaca conversaciones y señales ambientales. Los dos últimos son ejemplos de una reseña, no un inventario exhaustivo."),
("Del 6 al 10: personajes y formas de vida","6) Cal aparece con perfil conspirativo. 7) Boobie combina negocios, ocio y música. 8) Dre'Quan busca una carrera musical. 9) Real Dimez conecta rap y redes. 10) AP destaca el vínculo de Jason y Lucia. Son datos promocionales o lecturas críticas, no spoilers de misiones."),
("Del 11 al 15: sistemas y límites","11) El transporte público exige ir a una parada, según GamesRadar. 12) La guía describe seis estrellas de búsqueda. 13) Criminal Profile observa a ambos protagonistas. 14) Waink It da datos de coches según PC Gamer. 15) Rockstar publicó una galería de lanzamiento. Ninguno es un secreto nuevo descubierto por esta redacción.")
],"La lista atribuye los detalles a sus fuentes: no son quince secretos ocultos ni quince funciones probadas personalmente por LEVELUP DAILY.",
[("¿Son 15 easter eggs?","No; son observaciones de reseñas, bios oficiales y guías."),("¿Qué puntos son opiniones?","Las descripciones de ritmo y vida cotidiana se atribuyen a reseñas."),("¿Sustituye a una guía de secretos?","No; un secreto requiere evidencia y ubicación reproducible.")],
["launch","media","fast","profile","ap","bloq","cars"],"análisis",("detalles","observaciones","vida-cotidiana"))

assert len(R) == 35, f"Se esperaban 35 artículos, hay {len(R)}"
assert len({x["slug"] for x in R}) == 35
output_path=Path("content/gta-deep-dive-articles.json")
if output_path.exists():
    previous={item["slug"]:item for item in json.loads(output_path.read_text(encoding="utf-8"))}
    image_fields=("cover_image","image_alt","image_caption","image_credit","image_source","image_source_file",
                  "image_rights_status","inline_media","cover_photo_needed","inline_photo_needed")
    for item in R:
        old=previous.get(item["slug"],{})
        for field in image_fields:
            if field in old:
                item[field]=old[field]
output_path.write_text(json.dumps(R, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
print("Artículo nuevos:", len(R))
