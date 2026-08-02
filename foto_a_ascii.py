from PIL import Image

RUTA_IMAGEN = "20241222_145921 (1).jpg"
SALIDA = "portrait.txt"

# 92 columnas x 52 filas llena exactamente el 100% del recuadro VISUAL.MAP
ANCHO = 92
ALTO = 52

ASCII_CHARS = " .:-=+*#%@"

def generar_ascii_definitivo():
    try:
        img = Image.open(RUTA_IMAGEN).convert("L")
        ancho_orig, alto_orig = img.size
        
        # 1. Corrección matemática para 0% de deformación (adiós cara aplastada)
        # En SVG, 92 caracteres de ancho por 52 líneas equivale a una proporción física de ~0.92
        ratio_fisico_svg = 0.92
        alto_meta = int(ancho_orig / ratio_fisico_svg)
        
        if alto_orig > alto_meta:
            # Recortamos únicamente el techo sobrante del auto para conservar tu rostro
            # delgado, hombros y sudadera sin estirar horizontalmente
            margen = (alto_orig - alto_meta) // 2
            img = img.crop((0, int(margen * 0.8), ancho_orig, alto_orig - int(margen * 1.2)))
        
        # 2. Redimensionar a la rejilla exacta de 92x52
        img_final = img.resize((ANCHO, ALTO))
        
        pixeles = list(img_final.getdata())
        caracteres = [ASCII_CHARS[pixel * len(ASCII_CHARS) // 256] for pixel in pixeles]
        lineas = ["".join(caracteres[i:i + ANCHO]) for i in range(0, len(caracteres), ANCHO)]
        
        with open(SALIDA, "w", encoding="utf-8") as f:
            f.write("\n".join(lineas))
            
        print(f"✔ ¡Listo! Retrato natural sin aplastar ({ANCHO}x{ALTO}) en '{SALIDA}'.")
        
    except FileNotFoundError:
        print(f"Error: No se encontró '{RUTA_IMAGEN}'.")

if __name__ == "__main__":
    generar_ascii_definitivo()
