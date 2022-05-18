import unicodedata

def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                if unicodedata.category(c) != 'Mn')




class Msgs:
    """ Class where standard message are defined """
    
    dont_understand = ["Perdona, tengo problemas para responder la pregunta, reformula la pregunta",
                      "Lo siento, pero no te he entendido ¿Puedes escribir la pregunta de otra forma?",
                      "Perdón, pero no he entendido bien lo que me quieres preguntar. ¿Puedes preguntarlo de otra forma?",
                      "Creo que no te he entendido bien, lo siento, pregúntamelo de otra forma."]

    message = [
        {
            "key": ["paro", "empleo", "desempleo", "parado", "parados", "desempleado", "desempleados", "autonomo", "autónomos"],
            "suggestion": "Sobre  empleo puedes preguntarme por el número de autónomos, nuevos contratos, etc. Por ejemplo: ¿Cuántos autónomos hay dados de alta en marzo del 2012 en Aragón? ¿Cuántos nuevos contratos de mujeres hubo en marzo de 2012 en la comarca la Jacetania?"
        },
        {
            "key": ["cafeteria", "restaurante", "restaurantes", "bar", "bares", "asador", "comer", "cafe"],
            "suggestion": "De ocio y restauración tengo mucha información. Sabes que tengo registradas muchas cafeterías y restaurantes de Aragón. Puedes preguntarme, por ejemplo, ¿Dónde puedo comer en Zuera?¿Dónde puedo tomar un café en Alcañiz?"
        },
        {
            "key": ["turismo", "ocio", "vacaciones", "reserva", "reservas", "oficina de turismo", "oficinas de turismo", "viajes", "viaje", "pernoctaciones"],
            "suggestion": " Sobre turismo tengo mucha información sobre los alojamientos en Aragón, oficinas de turismo, agencias de viajes, etc. Puedes preguntarme, por ejemplo:  ¿Dónde puedo alojarme en Jaca?  ¿Cómo puedo reservar en el hotel Ciudad de Teruel?  ¿Qué agencias de Viajes hay que Barbastro?"
        },
        {
            "key": ["cultura", "museo", "museos", "obra", "pintura", "escultura", "obras", "pinturas", "esculturas"],
            "suggestion": "De cultura tengo información de algunos museos de Aragón.  Por ejemplo, pregúntame:  ¿Dime los museos del municipio de Huesca? ,  ¿Qué obras tiene el museo provincial de Zaragoza?  "
        },
        {
            "key": ["agricultura", "hectárea", "hectareas", "cultivo", "secano", "regadio", "cultivos", "ecologica", "olivar", "olivo", "viñedo", "viña", "vid"],
            "suggestion": "De  temas agrícolas tengo información sobre los distintos usos de la tierra y cultivos que se producen. Por ejemplo, pregúntame:  ¿Cuántas hectáreas de agricultura ecológica hay la provincia de Zaragoza?  ¿Cuántas hectáreas de olivar hay en la provincia de Teruel? ¿Cuántas hectáreas de viñedo hay en la provincia de Teruel?    "
        },
        {
            "key": ["firma digital ", "firma electronica", "certificado", "revocar", "tramitación electrónica", "telematica", "tramitación electronica"],
            "suggestion": "De  temas relativos a Sociedad de la Información  y tramitación electrónica dispongo de numerosa información  Por ejemplo, pregúntame: ¿Qué es la firma electrónica?, ¿Cómo puedo presentar una solicitud telemática de un procedimiento?, ¿Qué pasos hay que seguir para instalar la firma digital? "
        },
        {
            "key": ["habitante", "habitantes", "poblacion", "municipio", "municipios", "comarca", "comarcas", "ayuntamiento", "ayuntamientos", "concejal", "concejales", "alcalde", "alcaldesa", "alcaldes"],
            "suggestion": "De  Aragón y su territorio dispongo de información de municipios y comarcas, datos de población, ayuntamientos y sus alcaldes, etc. Prueba a preguntarme por ejemplo: ¿Cuántos habitantes había en Aragón en 2019? ¿Cuál es el CIF del ayuntamiento de Fraga?¿Cómo se llama el alcalde de Monzón? "

        },
        {
            "key": ["infraestructura", "infraestructuras", "carretera", "carreteras", "autovia", "autovias", "autopista", "autopistas", "trafico", "trafico", "incidencia", "incidencias", "trasporte", "transportes", "bus", "autobus", "autobuses", "paradas", "ruta", "rutas", "semaforo", "semaforos", "circulacion"],
            "suggestion": "De  Infraestructura y Transportes dispongo de información de carreteras, incidencias, rutas de autobús, paradas, etc. Por ejemplo, puedes preguntarme: ¿existe alguna incidencia de tráfico en la provincia de Teruel? ¿A qué velocidad se puede circular por la carretera Z-40? ¿Hay servicio de autobús en Boltaña?"
        }
    ]


    @staticmethod
    def get_suggestion(userQuestion):
        for word in userQuestion.split():
            for sugg in Msgs.message:
                if strip_accents(word.lower()) in sugg['key']:
                    return sugg['suggestion']
        return ""

