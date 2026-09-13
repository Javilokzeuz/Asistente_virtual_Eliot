import os

# Reemplaza con tu clave de Google AI Studio (https://aistudio.google.com/)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "TU_API_KEY_AQUI")

# Modelo multimodal principal
MODELO_AGENTE = "gemini-2.5-flash"

# Ruta temporal para capturas de pantalla
RUTA_CAPTURAS = "temp_screenshot.png"