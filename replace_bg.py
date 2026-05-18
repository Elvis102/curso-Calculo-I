from PIL import Image, ImageDraw
import os
import sys

WHITE = (255, 255, 255)
THRESH = 20  # tolerancia de color (±20 por canal)

def process_folder(folder):
    exts = (".jpg", ".jpeg", ".png")
    files = [f for f in os.listdir(folder) if f.lower().endswith(exts)]

    if not files:
        print(f"No se encontraron imágenes en: {folder}")
        return

    for fname in sorted(files):
        path = os.path.join(folder, fname)
        img = Image.open(path).convert("RGB")
        w, h = img.size

        # Flood fill desde las 4 esquinas para reemplazar solo el fondo
        for corner in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]:
            ImageDraw.floodfill(img, corner, WHITE, thresh=THRESH)

        img.save(path, "JPEG", quality=95)
        print(f"✓ {fname}")

    print(f"\n{len(files)} imágenes procesadas en: {folder}")


AYUDA = """
╔══════════════════════════════════════════════════════════════════╗
║              REPLACE_BG — Fondo gris → Blanco puro              ║
╠══════════════════════════════════════════════════════════════════╣
║  Reemplaza el fondo gris de todas las imágenes de una carpeta   ║
║  por blanco puro (#ffffff) usando flood fill desde las esquinas. ║
╠══════════════════════════════════════════════════════════════════╣
║  CÓMO CORRER EN LA TERMINAL:                                     ║
║                                                                  ║
║  1. Abre la terminal y ve al proyecto:                           ║
║     cd /Users/elvissanchez/Documents/GitHub/curso-calculo-I     ║
║                                                                  ║
║  2. Ejecuta el script pasando la carpeta como argumento:         ║
║     python3 replace_bg.py "ruta/a/tu/carpeta"                   ║
║                                                                  ║
║  EJEMPLOS:                                                       ║
║     python3 replace_bg.py "imgs/11-tracendental functions_..."  ║
║     python3 replace_bg.py "imgs/8-Polynomial functions_..."     ║
║                                                                  ║
║  NOTA: Usa comillas si la carpeta tiene espacios en el nombre.   ║
╚══════════════════════════════════════════════════════════════════╝
"""

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(AYUDA)
        sys.exit(1)

    folder = sys.argv[1]

    if not os.path.isdir(folder):
        print(f"Error: '{folder}' no es una carpeta válida.")
        sys.exit(1)

    process_folder(folder)
