from PIL import Image

RUTA_IMAGEN = "20241222_145921 (1).jpg"
SALIDA = "portrait.txt"

# 92 columnas x 53 filas llena el recuadro con simetría perfecta
ANCHO = 92
ALTO = 53

ASCII_CHARS = " .:-=+*#%@"

def generar_ascii_centrado_definitivo():
        img = Image.open(RUTA_IMAGEN).convert("L")
        ancho_orig, alto_orig = img.size
        # Relación de aspecto aproximada en el SVG (414px de ancho / 400px de alto)
        target_aspect = 1.035
        current_aspect = ancho_orig / alto_orig
        
        if current_aspect > target_aspect:
            # Imagen más ancha: rellenar arriba y abajo
            nuevo_alto = int(ancho_orig / target_aspect)
            img_canvas = Image.new("L", (ancho_orig, nuevo_alto), 0)
            offset_y = (nuevo_alto - alto_orig) // 2
            img_canvas.paste(img, (0, offset_y))
        else:
            # Imagen más alta: rellenar a los lados (izquierda y derecha) para no recortar
            nuevo_ancho = int(alto_orig * target_aspect)
            img_canvas = Image.new("L", (nuevo_ancho, alto_orig), 0)
            offset_x = (nuevo_ancho - ancho_orig) // 2
            img_canvas.paste(img, (offset_x, 0))
            
        img_final = img_canvas.resize((ANCHO, ALTO))
        
        pixeles = list(img_final.getdata())
        caracteres = [ASCII_CHARS[pixel * len(ASCII_CHARS) // 256] for pixel in pixeles]
        lineas = ["".join(caracteres[i:i + ANCHO]) for i in range(0, len(caracteres), ANCHO)]
        
        with open(SALIDA, "w", encoding="utf-8") as f:
            f.write("\n".join(lineas))
        print(f"✔ ¡Listo! Retrato centrado, proporcionado y simétrico ({ANCHO}x{ALTO}) en '{SALIDA}'.")

if __name__ == "__main__":
    generar_ascii_centrado_definitivo()
