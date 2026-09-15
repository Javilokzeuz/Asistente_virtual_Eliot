import json

from google import genai

import config
from tools import system_tools


class EliotAgent:
    """
    Cerebro principal de Eliot.

    Gemini interpreta las instrucciones y puede utilizar
    las herramientas disponibles en system_tools.py.
    """

    def __init__(self):
        if (
            not config.GEMINI_API_KEY
            or config.GEMINI_API_KEY == "TU_API_KEY_AQUI"
        ):
            raise ValueError(
                "No se encontró una API key válida de Gemini."
            )

        self.client = genai.Client(
            api_key=config.GEMINI_API_KEY
        )

        self.modelo = config.MODELO_AGENTE

        self.system_instruction = """
Eres Eliot, un asistente virtual personal.

Tu personalidad:
- Eres inteligente, tranquilo y eficiente.
- Hablas en español.
- Respondes de forma natural y clara.
- No das respuestas innecesariamente largas.
- Puedes llamar al usuario "señor" de vez en cuando.
- Tu objetivo es ayudar al usuario y utilizar las herramientas
  disponibles cuando sea necesario.

IMPORTANTE:
- No inventes que realizaste una acción.
- Si una herramienta puede realizar la acción solicitada,
  utiliza la herramienta.
- Si una petición no necesita una herramienta, responde normalmente.
"""

        self.herramientas = [
            {
                "type": "function",
                "name": "obtener_informacion_sistema",
                "description": (
                    "Obtiene información básica del ordenador "
                    "de Windows donde se ejecuta Eliot."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {},
                },
            },
            {
                "type": "function",
                "name": "abrir_aplicacion",
                "description": (
                    "Abre una aplicación de Windows conocida, "
                    "por ejemplo calculadora, bloc de notas "
                    "o explorador de archivos."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "nombre": {
                            "type": "string",
                            "description": (
                                "Nombre de la aplicación que se desea abrir."
                            ),
                        }
                    },
                    "required": ["nombre"],
                },
            },
            {
                "type": "function",
                "name": "abrir_sitio_web",
                "description": (
                    "Abre una dirección web en el navegador "
                    "predeterminado del ordenador."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": (
                                "Dirección web que se desea abrir."
                            ),
                        }
                    },
                    "required": ["url"],
                },
            },
            {
                "type": "function",
                "name": "obtener_directorio_actual",
                "description": (
                    "Obtiene la carpeta desde la que se está "
                    "ejecutando Eliot."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {},
                },
            },
        ]

        self.funciones = {
            "obtener_informacion_sistema":
                system_tools.obtener_informacion_sistema,

            "abrir_aplicacion":
                system_tools.abrir_aplicacion,

            "abrir_sitio_web":
                system_tools.abrir_sitio_web,

            "obtener_directorio_actual":
                system_tools.obtener_directorio_actual,
        }

        self.ultima_interaccion = None

    def preguntar(self, mensaje):
        """
        Envía una instrucción a Gemini y permite que Eliot
        utilice sus herramientas cuando sea necesario.
        """

        if not mensaje or not mensaje.strip():
            return "No he recibido ninguna instrucción."

        try:
            interaccion = self.client.interactions.create(
                model=self.modelo,
                input=mensaje,
                tools=self.herramientas,
            )

            while True:
                llamada = None

                for paso in interaccion.steps:
                    if paso.type == "function_call":
                        llamada = paso
                        break

                if llamada is None:
                    break

                nombre = llamada.name
                argumentos = llamada.arguments or {}

                funcion = self.funciones.get(nombre)

                if funcion is None:
                    resultado = {
                        "error": f"Herramienta desconocida: {nombre}"
                    }
                else:
                    try:
                        resultado = funcion(**argumentos)
                    except Exception as error:
                        resultado = {
                            "error": str(error)
                        }

                if not isinstance(resultado, (dict, list, str, int, float, bool)):
                    resultado = str(resultado)

                interaccion = self.client.interactions.create(
                    model=self.modelo,
                    previous_interaction_id=interaccion.id,
                    input=[
                        {
                            "type": "function_result",
                            "name": nombre,
                            "call_id": llamada.id,
                            "result": [
                                {
                                    "type": "text",
                                    "text": json.dumps(
                                        resultado,
                                        ensure_ascii=False
                                    ),
                                }
                            ],
                        }
                    ],
                )

            self.ultima_interaccion = interaccion

            return interaccion.output_text

        except Exception as error:
            print(f"[ERROR ELIOT] {error}")

            return (
                "Lo siento, señor. "
                "Tuve un problema al procesar la instrucción."
            )