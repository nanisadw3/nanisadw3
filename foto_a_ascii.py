from PIL import Image

RUTA_IMAGEN = "20241222_145921 (1).jpg"
SALIDA = "portrait.txt"

# 98 columnas x 54 filas llena el recuadro con simetría perfecta
ANCHO = 98
ALTO = 54

ASCII_CHARS = " .:-=+*#%@"

def generar_ascii_centrado_definitivo():
    try:
        img = Image.open(RUTA_IMAGEN).convert("L")
        ancho_orig, alto_orig = img.size
        
        # 1. Recorte horizontal para centrar tu rostro (eliminamos el vacío del coche a la izquierda)
        izq = int(ancho_orig * 0.08)
        der = int(ancho_orig * 0.98)
        nuevo_ancho = der - izq
        
        # 2. Proporción física real (1.10) para evitar que la cara se vea aplastada o ancha
        ratio_fisico_svg = 1.10
        alto_ideal = int(nuevo_ancho / ratio_fisico_svg)
        
        margen_y = max(0, (alto_orig - alto_ideal) // 2)
        sup = int(margen_y * 0.8)
        inf = min(alto_orig, sup + alto_ideal)
        
        img_recortada = img.crop((izq, sup, der, inf))
        img_final = img_recortada.resize((ANCHO, ALTO))
        
        pixeles = list(img_final.getdata())
        caracteres = [ASCII_CHARS[pixel * len(ASCII_CHARS) // 256] for pixel in pixeles]
        lineas = ["".join(caracteres[i:i + ANCHO]) for i in range(0, len(caracteres), ANCHO)]
        
        with open(SALIDA, "w", encoding="utf-8") as f:
            f.write("\n".join(lineas))
            
        print(f"✔ ¡Listo! Retrato centrado, proporcionado y simétrico ({ANCHO}x{ALTO}) en '{SALIDA}'.")
        
    except FileNotFoundError:
        print(f"Error: No se encontró '{RUTA_IMAGEN}'.")

if __name__ == "__main__":
    generar_ascii_centrado_definitivo()
