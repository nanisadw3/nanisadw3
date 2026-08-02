from PIL import Image

RUTA_IMAGEN = "20241222_145921 (1).jpg"
SALIDA = "portrait.txt"

# Dimensiones exactas que caben en las 52 líneas de Y=80 a Y=472
ANCHO = 78
ALTO = 52

ASCII_CHARS = " .:-=+*#%@"

def generar_ascii_definitivo(ruta):
    try:
        img = Image.open(ruta).convert("L")
        ancho_orig, alto_orig = img.size
        
        # Recorte encuadrando tu rostro (eliminando techo y sobrantes)
        izq = int(ancho_orig * 0.14)
        sup = int(alto_orig * 0.16)
        der = int(ancho_orig * 0.86)
        inf = int(alto_orig * 0.77)
        
        img_recortada = img.crop((izq, sup, der, inf))
        img_final = img_recortada.resize((ANCHO, ALTO))
        pixeles = img_final.getdata()
        
        caracteres = [ASCII_CHARS[pixel * len(ASCII_CHARS) // 256] for pixel in pixeles]
        lineas = ["".join(caracteres[i:i + ANCHO]) for i in range(0, len(caracteres), ANCHO)]
        
        with open(SALIDA, "w", encoding="utf-8") as f:
            f.write("\n".join(lineas))
            
        print(f"✔ ¡Listo! Rostro guardado en tamaño exacto ({ANCHO}x{ALTO}).")
        
    except FileNotFoundError:
        print(f"Error: No se encontró '{RUTA_IMAGEN}'.")

if __name__ == "__main__":
    generar_ascii_definitivo(RUTA_IMAGEN)
