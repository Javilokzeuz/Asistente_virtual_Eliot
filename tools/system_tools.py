import os
import platform
import subprocess

from pycaw.pycaw import AudioUtilities


# ============================================================
# INFORMACIÓN DEL SISTEMA
# ============================================================

def obtener_informacion_sistema():
    """Devuelve información básica del PC."""
    return {
        "sistema": platform.system(),
        "version": platform.version(),
        "procesador": platform.processor(),
        "nombre_pc": platform.node(),
    }


def obtener_directorio_actual():
    """Devuelve la carpeta desde la que se está ejecutando Eliot."""
    return os.getcwd()


# ============================================================
# APLICACIONES
# ============================================================

def abrir_aplicacion(nombre):
    """Abre una aplicación de Windows conocida."""

    aplicaciones = {
        "calculadora": "calc.exe",
        "bloc de notas": "notepad.exe",
        "notepad": "notepad.exe",
        "explorador": "explorer.exe",
        "explorador de archivos": "explorer.exe",
    }

    programa = aplicaciones.get(nombre.lower())

    if not programa:
        return f"No conozco una aplicación llamada {nombre}."

    try:
        subprocess.Popen(programa)
        return f"He abierto {nombre}."

    except Exception as error:
        return f"No pude abrir {nombre}: {error}"


# ============================================================
# INTERNET
# ============================================================

def abrir_sitio_web(url):
    """Abre una página web en el navegador predeterminado."""

    try:
        os.startfile(url)
        return f"He abierto {url}."

    except Exception as error:
        return f"No pude abrir la página: {error}"


# ============================================================
# VOLUMEN
# ============================================================

def obtener_volumen():
    """Obtiene el volumen actual del sistema."""

    try:
        dispositivos = AudioUtilities.GetSpeakers()
        volumen = dispositivos.EndpointVolume

        nivel = volumen.GetMasterVolumeLevelScalar() * 100

        return round(nivel)

    except Exception as error:
        return f"No pude obtener el volumen: {error}"


def establecer_volumen(nivel):
    """
    Establece el volumen del sistema.
    
    nivel:
        Número entre 0 y 100.
    """

    try:
        nivel = max(0, min(100, float(nivel)))

        dispositivos = AudioUtilities.GetSpeakers()
        volumen = dispositivos.EndpointVolume

        volumen.SetMasterVolumeLevelScalar(
            nivel / 100,
            None
        )

        return f"Volumen establecido al {round(nivel)}%."

    except Exception as error:
        return f"No pude cambiar el volumen: {error}"


def cambiar_volumen(cambio):
    """
    Aumenta o disminuye el volumen actual.

    Ejemplo:
        cambiar_volumen(10)   -> subir 10%
        cambiar_volumen(-10)  -> bajar 10%
    """

    try:
        dispositivos = AudioUtilities.GetSpeakers()
        volumen = dispositivos.EndpointVolume

        actual = volumen.GetMasterVolumeLevelScalar() * 100

        nuevo = max(
            0,
            min(100, actual + float(cambio))
        )

        volumen.SetMasterVolumeLevelScalar(
            nuevo / 100,
            None
        )

        return f"Volumen establecido al {round(nuevo)}%."

    except Exception as error:
        return f"No pude cambiar el volumen: {error}"