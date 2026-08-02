from PIL import Image

# 1. Configuración de entrada y salida
RUTA_IMAGEN = "20241222_145921 (1).jpg"  # Nombre de tu archivo de imagen
SALIDA = "portrait.txt"

# 2. Dimensiones exactas para cubrir TODA la pantalla del SVG (90x52)
ANCHO = 90
ALTO = 52

# 3. Rampa de caracteres (de sombra a luz para fondo oscuro)
# Si al verlo en tu perfil sientes que parece un negativo, invierte esta cadena: "@%#*+=-:. "
ASCII_CHARS = " .:-=+*#%@"

def generar_ascii(ruta):
    try:
        # Abrir imagen y convertir a blanco y negro (escala de grises)
        img = Image.open(ruta).convert("L")
        
        # Redimensionar exactamente a la rejilla completa de la terminal (90x52)
        img = img.resize((ANCHO, ALTO))
        pixeles = img.getdata()
        
        # Mapear cada píxel (0 a 255) a un carácter ASCII
        caracteres = [ASCII_CHARS[pixel * len(ASCII_CHARS) // 256] for pixel in pixeles]
        
        # Formatear el texto en filas y columnas
        lineas = ["".join(caracteres[i:i + ANCHO]) for i in range(0, len(caracteres), ANCHO)]
        
        # Guardar en portrait.txt
        with open(SALIDA, "w", encoding="utf-8") as f:
            f.write("\n".join(lineas))
            
        print(f"¡Éxito! Tu rostro en tamaño completo (90x52) se guardó en '{SALIDA}'.")
        
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{RUTA_IMAGEN}' en esta carpeta.")

if __name__ == "__main__":
    generar_ascii(RUTA_IMAGEN)
