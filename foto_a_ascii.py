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
        
        # 1. Recorte cuadrado (aspecto 1.035) enfocado en cara y hombros
        # Desplazamos a la derecha para centrar la cara y abajo para centrar los hombros
        w_new = w_orig - int(w_orig * 0.15)
        h_new = int(w_new / 1.035)
        
        izq = int(w_orig * 0.15)
        der = w_orig
        sup = int(h_orig * 0.20)
        inf = sup + h_new
        
        img_cropped = img.crop((izq, sup, der, inf))
        
        # 2. Aplicar corrección Gamma para resaltar ropa oscura y fondo
        import numpy as np
        arr = np.array(img_cropped) / 255.0
        arr = np.power(arr, 0.50) * 255.0  # gamma = 0.50 hace los oscuros más visibles
        img_canvas = Image.fromarray(arr.astype(np.uint8))
        
        # 3. Redimensionar al buffer objetivo (92x53) sin rellenar, llenando toda la caja
        img_final = img_canvas.resize((ANCHO, ALTO))
        
        # Usamos Pillow getdata
        pixeles = list(img_final.getdata())
        caracteres = [ASCII_CHARS[pixel * len(ASCII_CHARS) // 256] for pixel in pixeles]
        lineas = ["".join(caracteres[i:i + ANCHO]) for i in range(0, len(caracteres), ANCHO)]
        
        with open(SALIDA, "w", encoding="utf-8") as f:
            f.write("\n".join(lineas))
        print(f"✔ ¡Listo! Retrato cuadrado de {ANCHO}x{ALTO} generado llenando toda la caja.")
    except Exception as e:
        print(f"Error al generar ASCII: {e}")

if __name__ == "__main__":
    generar_ascii_centrado_definitivo()
