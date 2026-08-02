from PIL import Image

RUTA_IMAGEN = "20241222_145921 (1).jpg"
SALIDA = "portrait.txt"

# 104 columnas de ancho x 56 filas de alto da la proporción justa para una cara delgada en SVG
ANCHO = 104
ALTO = 56

ASCII_CHARS = " .:-=+*#%@"

def generar_ascii_proporcionado():
    try:
        img = Image.open(RUTA_IMAGEN).convert("L")
        ancho_orig, alto_orig = img.size
        
        # Factor de corrección 0.45: adelgaza horizontalmente para compensar la letra delgada del SVG
        relacion_objetivo = (ANCHO * 0.45) / ALTO
        relacion_original = ancho_orig / alto_orig
        
        if relacion_original < relacion_objetivo:
            nuevo_alto = int(ancho_orig / relacion_objetivo)
            margen = (alto_orig - nuevo_alto) // 2
            # Recortamos un poco de arriba/abajo pero conservando hombros, pecho y rostro centrado
            sup = int(margen * 0.9)
            inf = alto_orig - int(margen * 1.1)
            img = img.crop((0, sup, ancho_orig, inf))
            
        img_final = img.resize((ANCHO, ALTO))
        
        pixeles = list(img_final.getdata())
        caracteres = [ASCII_CHARS[pixel * len(ASCII_CHARS) // 256] for pixel in pixeles]
        lineas = ["".join(caracteres[i:i + ANCHO]) for i in range(0, len(caracteres), ANCHO)]
        
        with open(SALIDA, "w", encoding="utf-8") as f:
            f.write("\n".join(lineas))
            
        print(f"✔ ¡Listo! Retrato proporcionado, delgado y a pantalla completa ({ANCHO}x{ALTO}).")
        
    except FileNotFoundError:
        print(f"Error: No se encontró '{RUTA_IMAGEN}'.")

if __name__ == "__main__":
    generar_ascii_proporcionado()
