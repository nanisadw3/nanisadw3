from PIL import Image

# 1. Configuración de archivo
RUTA_IMAGEN = "20241222_145921 (1).jpg"
SALIDA = "portrait.txt"

# 2. Medida EXACTA para que no se salga del recuadro VISUAL.MAP
ANCHO = 78
ALTO = 48

# 3. Rampa de caracteres para buen contraste en fondo oscuro
ASCII_CHARS = " .:-=+*#%@"

def generar_ascii_perfecto(ruta):
    try:
        img = Image.open(ruta).convert("L")
        ancho_orig, alto_orig = img.size
        
        # 4. RECORTE CENTRADO EN EL ROSTRO (Sin techo del auto ni bordes sobrantes)
        izq = int(ancho_orig * 0.15)
        sup = int(alto_orig * 0.18)
        der = int(ancho_orig * 0.85)
        inf = int(alto_orig * 0.75)
        
        img_recortada = img.crop((izq, sup, der, inf))
        
        # 5. Redimensionar al tamaño exacto de la caja (78x48)
        img_final = img_recortada.resize((ANCHO, ALTO))
        pixeles = img_final.getdata()
        
        caracteres = [ASCII_CHARS[pixel * len(ASCII_CHARS) // 256] for pixel in pixeles]
        lineas = ["".join(caracteres[i:i + ANCHO]) for i in range(0, len(caracteres), ANCHO)]
        
        with open(SALIDA, "w", encoding="utf-8") as f:
            f.write("\n".join(lineas))
            
        print(f"✔ ¡Listo! Rostro ajustado exactamente al recuadro (78x48) en '{SALIDA}'.")
        
    except FileNotFoundError:
        print(f"Error: No se encontró '{RUTA_IMAGEN}'.")

if __name__ == "__main__":
    generar_ascii_perfecto(RUTA_IMAGEN)
