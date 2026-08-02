from PIL import Image

RUTA_IMAGEN = "20241222_145921 (1).jpg"
SALIDA = "portrait.txt"

# 90x56 mantiene tu rostro delgado, natural, alejado y proporcionado
ANCHO = 90
ALTO = 56

ASCII_CHARS = " .:-=+*#%@"

def generar_ascii_definitivo():
    try:
        img = Image.open(RUTA_IMAGEN).convert("L")
        img_final = img.resize((ANCHO, ALTO))
        
        pixeles = list(img_final.getdata())
        caracteres = [ASCII_CHARS[pixel * len(ASCII_CHARS) // 256] for pixel in pixeles]
        lineas = ["".join(caracteres[i:i + ANCHO]) for i in range(0, len(caracteres), ANCHO)]
        
        with open(SALIDA, "w", encoding="utf-8") as f:
            f.write("\n".join(lineas))
            
        print(f"✔ ¡Listo! Retrato natural y proporcionado ({ANCHO}x{ALTO}) guardado en '{SALIDA}'.")
        
    except FileNotFoundError:
        print(f"Error: No se encontró '{RUTA_IMAGEN}'.")

if __name__ == "__main__":
    generar_ascii_definitivo()
