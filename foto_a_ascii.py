from PIL import Image

RUTA_IMAGEN = "20241222_145921 (1).jpg"
SALIDA = "portrait.txt"

# 104 columnas x 52 filas cubre el 100% del ancho y alto de VISUAL.MAP
ANCHO = 104
ALTO = 52

ASCII_CHARS = " .:-=+*#%@"

def generar_ascii_alejado():
    try:
        img = Image.open(RUTA_IMAGEN).convert("L")
        
        # SIN RECORTE (.crop) para mantener la distancia original (alejado, con hombros y sudadera)
        img_final = img.resize((ANCHO, ALTO))
        
        pixeles = list(img_final.getdata())
        caracteres = [ASCII_CHARS[pixel * len(ASCII_CHARS) // 256] for pixel in pixeles]
        lineas = ["".join(caracteres[i:i + ANCHO]) for i in range(0, len(caracteres), ANCHO)]
        
        with open(SALIDA, "w", encoding="utf-8") as f:
            f.write("\n".join(lineas))
            
        print(f"✔ ¡Listo! Retrato alejado y a pantalla completa ({ANCHO}x{ALTO}) guardado en '{SALIDA}'.")
        
    except FileNotFoundError:
        print(f"Error: No se encontró '{RUTA_IMAGEN}'.")

if __name__ == "__main__":
    generar_ascii_alejado()
