import os
import platform
import subprocess


def obtener_informacion_sistema():
    """Devuelve información básica del PC."""
    return {
        "sistema": platform.system(),
        "version": platform.version(),
        "procesador": platform.processor(),
        "nombre_pc": platform.node(),
    }


def abrir_aplicacion(nombre):
    """Abre una aplicación de Windows por su nombre."""
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


def abrir_sitio_web(url):
    """Abre una página web en el navegador predeterminado."""
    try:
        os.startfile(url)
        return f"He abierto {url}."
    except Exception as error:
        return f"No pude abrir la página: {error}"


def obtener_directorio_actual():
    """Devuelve la carpeta desde la que se está ejecutando Eliot."""
    return os.getcwd()