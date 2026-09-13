import mss
from PIL import Image
import config

def capturar_pantalla(output_path=config.RUTA_CAPTURAS):
    """Captura el monitor principal y lo guarda como imagen PNG."""
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        sct_img = sct.grab(monitor)
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        img.save(output_path)
        return output_path

if __name__ == "__main__":
    archivo = capturar_pantalla()
    print(f"Captura realizada con éxito: {archivo}")