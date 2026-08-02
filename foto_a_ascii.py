from PIL import Image

RUTA_IMAGEN = "20241222_145921 (1).jpg"
SALIDA = "portrait.txt"

# 92 columnas x 53 filas llena el recuadro con simetría perfecta
ANCHO = 92
ALTO = 53

ASCII_CHARS = " .:-=+*#%@"

def generar_ascii_centrado_definitivo():
    try:
        img = Image.open(RUTA_IMAGEN).convert("L")
        ancho_orig, alto_orig = img.size
        
        # Relación de aspecto aproximada en el SVG (414px de ancho / 400px de alto)
        target_aspect = 1.035
        current_aspect = ancho_orig / alto_orig
        
        if current_aspect > target_aspect:
            # Recorte horizontal minimal para centrar la imagen
            nuevo_ancho = int(alto_orig * target_aspect)
            izq = (ancho_orig - nuevo_ancho) // 2
            der = izq + nuevo_ancho
            sup = 0
            inf = alto_orig
        else:
            # Recorte vertical minimal para centrar la imagen
            nuevo_alto = int(ancho_orig / target_aspect)
            sup = (alto_orig - nuevo_alto) // 2
            inf = sup + nuevo_alto
            izq = 0
            der = ancho_orig
            
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
