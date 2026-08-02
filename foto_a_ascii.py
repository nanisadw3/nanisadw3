from PIL import Image

RUTA_IMAGEN = "20241222_145921 (1).jpg"
SALIDA = "portrait.txt"

# Dimensiones para llenar el 100% del recuadro VISUAL.MAP
ANCHO = 104
ALTO = 52

ASCII_CHARS = " .:-=+*#%@"

def generar_ascii_sin_aplastar():
    try:
        img = Image.open(RUTA_IMAGEN).convert("L")
        ancho_orig, alto_orig = img.size
        
        # 1. Corrección de Aspect Ratio (Evita que la cara se aplaste horizontalmente)
        # En fuentes monoespaciadas, un carácter es más alto que ancho (~0.55 de relación)
        relacion_objetivo = (ANCHO * 0.52) / ALTO
        relacion_original = ancho_orig / alto_orig
        
        if relacion_original < relacion_objetivo:
            # La foto es muy vertical: recortamos arriba y abajo manteniendo el centro intacto
            nuevo_alto = int(ancho_orig / relacion_objetivo)
            margen = (alto_orig - nuevo_alto) // 2
            # Recortamos un poco más de arriba para no perder la sudadera y centrar tu mirada
            sup = int(margen * 1.1)
            inf = alto_orig - int(margen * 0.9)
            img = img.crop((0, sup, ancho_orig, inf))
        
        # 2. Redimensionar a la pantalla completa del monitor
        img_final = img.resize((ANCHO, ALTO))
        
        pixeles = list(img_final.getdata())
        caracteres = [ASCII_CHARS[pixel * len(ASCII_CHARS) // 256] for pixel in pixeles]
        lineas = ["".join(caracteres[i:i + ANCHO]) for i in range(0, len(caracteres), ANCHO)]
        
        with open(SALIDA, "w", encoding="utf-8") as f:
            f.write("\n".join(lineas))
            
        print(f"✔ ¡Listo! Retrato con proporciones reales y sin aplastar ({ANCHO}x{ALTO}) guardado en '{SALIDA}'.")
        
    except FileNotFoundError:
        print(f"Error: No se encontró '{RUTA_IMAGEN}'.")

if __name__ == "__main__":
    generar_ascii_sin_aplastar()
