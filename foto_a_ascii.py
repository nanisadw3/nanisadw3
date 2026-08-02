from PIL import Image

RUTA_IMAGEN = "20241222_145921 (1).jpg"
SALIDA = "portrait.txt"

# 96 columnas x 52 filas llena el recuadro completo sin dejar huecos
ANCHO = 96
ALTO = 52

ASCII_CHARS = " .:-=+*#%@"

def generar_ascii_centrado(ruta):
    try:
        img = Image.open(ruta).convert("L")
        ancho_orig, alto_orig = img.size
        
        # Recorte suave superior/inferior SOLO para igualar la proporción cuadrada
        # Mantiene la distancia original (hombros, sudadera y rostro centrados) sin zoom a la cara
        margen_v = int(alto_orig * 0.08)
        izq = 0
        sup = margen_v
        der = ancho_orig
        inf = alto_orig - margen_v
        
        img_recortada = img.crop((izq, sup, der, inf))
        img_final = img_recortada.resize((ANCHO, ALTO))
        
        pixeles = list(img_final.getdata())
        
        caracteres = [ASCII_CHARS[pixel * len(ASCII_CHARS) // 256] for pixel in pixeles]
        lineas = ["".join(caracteres[i:i + ANCHO]) for i in range(0, len(caracteres), ANCHO)]
        
        with open(SALIDA, "w", encoding="utf-8") as f:
            f.write("\n".join(lineas))
            
        print(f"✔ ¡Listo! Retrato alejado, centrado y a pantalla completa ({ANCHO}x{ALTO}) en '{SALIDA}'.")
        
    except FileNotFoundError:
        print(f"Error: No se encontró '{RUTA_IMAGEN}'.")

if __name__ == "__main__":
    generar_ascii_centrado(RUTA_IMAGEN)
