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
        w_orig, h_orig = img.size
        
        # 1. Recorte inicial para centrar la cara y remover el cielo vacío arriba
        # Desplazamos a la derecha (izquierda = 24%) y un poco hacia abajo (arriba = 12%)
        izq = int(w_orig * 0.24)
        der = w_orig
        sup = int(h_orig * 0.12)
        inf = h_orig
        img_cropped = img.crop((izq, sup, der, inf))
        
        w_cropped, h_cropped = img_cropped.size
        
        # 2. Relación de aspecto objetivo en el SVG (414px / 400px = 1.035)
        target_aspect = 1.035
        current_aspect = w_cropped / h_cropped
        
        if current_aspect > target_aspect:
            # Rellenar arriba y abajo
            nuevo_alto = int(w_cropped / target_aspect)
            img_canvas = Image.new("L", (w_cropped, nuevo_alto), 40)
            offset_y = (nuevo_alto - h_cropped) // 2
            img_canvas.paste(img_cropped, (0, offset_y))
        else:
            # Rellenar a los lados (izquierda y derecha) para no recortar el alto
            nuevo_ancho = int(h_cropped * target_aspect)
            img_canvas = Image.new("L", (nuevo_ancho, h_cropped), 40)
            offset_x = (nuevo_ancho - w_cropped) // 2
            img_canvas.paste(img_cropped, (offset_x, 0))
            
        # 3. Aplicar corrección Gamma para resaltar ropa oscura y fondo
        import numpy as np
        arr = np.array(img_canvas) / 255.0
        arr = np.power(arr, 0.50) * 255.0  # gamma = 0.50 hace los oscuros más visibles
        img_canvas = Image.fromarray(arr.astype(np.uint8))
        
        # 4. Redimensionar al buffer objetivo
        img_final = img_canvas.resize((ANCHO, ALTO))
        
        # Usamos Pillow getdata (es segura y simple para este caso)
        pixeles = list(img_final.getdata())
        caracteres = [ASCII_CHARS[pixel * len(ASCII_CHARS) // 256] for pixel in pixeles]
        lineas = ["".join(caracteres[i:i + ANCHO]) for i in range(0, len(caracteres), ANCHO)]
        
        with open(SALIDA, "w", encoding="utf-8") as f:
            f.write("\n".join(lineas))
        print(f"✔ ¡Listo! Retrato sin recortes, centrado y con detalles visibles en '{SALIDA}'.")
    except Exception as e:
        print(f"Error al generar ASCII: {e}")

if __name__ == "__main__":
    generar_ascii_centrado_definitivo()
