from google import genai
from google.genai import types

import config


class EliotAgent:
    """
    Cerebro principal de Eliot.

    Se encarga de:
    - Conectarse con Gemini.
    - Mantener una conversación.
    - Aplicar la personalidad de Eliot.
    - Preparar el sistema para añadir herramientas posteriormente.
    """

    def __init__(self):
        if not config.GEMINI_API_KEY:
            raise ValueError(
                "No se encontró GEMINI_API_KEY. "
                "Configura tu clave de Gemini antes de iniciar Eliot."
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
- Puedes llamar al usuario "señor" de vez en cuando, sin exagerar.
- Tu objetivo es ayudar al usuario y ejecutar sus instrucciones
  mediante las herramientas disponibles.

IMPORTANTE:
En esta primera versión todavía estás aprendiendo a utilizar
las herramientas del sistema. No inventes que realizaste una
acción si realmente no tienes una herramienta para realizarla.

Cuando una petición no requiera una herramienta, responde
normalmente.
"""

        self.historial = []

    def preguntar(self, mensaje):
        """
        Envía un mensaje a Gemini y devuelve la respuesta de Eliot.
        """

        if not mensaje or not mensaje.strip():
            return "No he recibido ninguna instrucción."

        self.historial.append(
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=mensaje)
                ]
            )
        )

        try:
            respuesta = self.client.models.generate_content(
                model=self.modelo,
                contents=self.historial,
                config=types.GenerateContentConfig(
                    system_instruction=self.system_instruction,
                    temperature=0.7,
                    max_output_tokens=500,
                ),
            )

            texto = respuesta.text

            if not texto:
                return "No pude generar una respuesta."

            self.historial.append(
                types.Content(
                    role="model",
                    parts=[
                        types.Part.from_text(text=texto)
                    ]
                )
            )

            return texto

        except Exception as error:
            print(f"[ERROR GEMINI] {error}")
            return (
                "Lo siento, señor. "
                "Tuve un problema al comunicarme con Gemini."
            )

    def limpiar_historial(self):
        """
        Borra la conversación actual.
        """

        self.historial = []