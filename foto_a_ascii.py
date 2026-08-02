from PIL import Image

RUTA_IMAGEN = "20241222_145921 (1).jpg"
SALIDA = "portrait.txt"

# Dimensiones EXACTAS para llenar todo el recuadro VISUAL.MAP de izquierda a derecha y de arriba a abajo
ANCHO = 90
ALTO = 52

ASCII_CHARS = " .:-=+*#%@"

def generar_ascii_completo(ruta):
    try:
        img = Image.open(ruta).convert("L")
        ancho_orig, alto_orig = img.size
        
        # Recorte natural de retrato: incluye cabello arriba, hombros/sudadera abajo y centra el rostro
        izq = int(ancho_orig * 0.05)
        sup = int(alto_orig * 0.08)
        der = int(ancho_orig * 0.95)
        inf = int(alto_orig * 0.72)
        
        img_recortada = img.crop((izq, sup, der, inf))
        img_final = img_recortada.resize((ANCHO, ALTO))
        
        pixeles = list(img_final.getdata())
        
        caracteres = [ASCII_CHARS[pixel * len(ASCII_CHARS) // 256] for pixel in pixeles]
        lineas = ["".join(caracteres[i:i + ANCHO]) for i in range(0, len(caracteres), ANCHO)]
        
        with open(SALIDA, "w", encoding="utf-8") as f:
            f.write("\n".join(lineas))
            
        print(f"✔ ¡Listo! Retrato proporcionado y a pantalla completa ({ANCHO}x{ALTO}) guardado en '{SALIDA}'.")
        
    except FileNotFoundError:
        print(f"Error: No se encontró '{RUTA_IMAGEN}'.")

if __name__ == "__main__":
    generar_ascii_completo(RUTA_IMAGEN)
