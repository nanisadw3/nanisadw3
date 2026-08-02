import re
from pathlib import Path
from PIL import Image

# --- CONFIGURACIÓN DE RESOLUCIÓN Y GEOMETRÍA SVG ---
RUTA_IMAGEN = "Gemini_Generated_Image_3mdvgr3mdvgr3mdv.png"
ARCHIVOS_SVG = ["dark.svg", "light.svg"]

# Dimensiones calibradas para el bounding box del panel "VISUAL.MAP"
ANCHO = 62
ALTO = 34

# Coordenadas absolutas dentro del recuadro izquierdo del SVG
X_BASE = 55      # Margen izquierdo del panel VISUAL.MAP (aumenta para mover a la derecha)
Y_START = 120    # Margen superior del ASCII dentro del panel
Y_STEP = 11      # Salto de línea (line-height) proporcional al font-size

ASCII_CHARS = " .:-=+*#%@"


def generar_ascii_centrado():
    try:
        img = Image.open(RUTA_IMAGEN).convert("L")
        ancho_orig, alto_orig = img.size
        
        # 1. Recorte para aislar la región central (rostro)
        izq = int(ancho_orig * 0.10)
        der = int(ancho_orig * 0.90)
        nuevo_ancho = der - izq
        
        # 2. Compensación de relación de aspecto para caracteres de consola (proporción ~1.15)
        ratio_fisico = 1.15
        alto_ideal = int(nuevo_ancho / ratio_fisico)
        margen_y = max(0, (alto_orig - alto_ideal) // 2)
        sup = int(margen_y * 0.75)
        inf = min(alto_orig, sup + alto_ideal)
        
        # 3. Redimensionado al buffer objetivo
        img_final = img.crop((izq, sup, der, inf)).resize((ANCHO, ALTO))
        
        # 4. Mapeo de luminancia a caracteres ASCII
        pixeles = list(img_final.getdata())
        caracteres = [ASCII_CHARS[pixel * len(ASCII_CHARS) // 256] for pixel in pixeles]
        lineas = [
            "".join(caracteres[i : i + ANCHO])
            for i in range(0, len(caracteres), ANCHO)
        ]
        
        # 5. Construcción de nodos <tspan> para inyección en SVG
        nodos_tspan = []
        for index, linea in enumerate(lineas):
            linea_escapada = (
                linea.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
            )
            y_coord = Y_START + (index * Y_STEP)
            nodos_tspan.append(f'<tspan x="{X_BASE}" y="{y_coord}">{linea_escapada}</tspan>')
            
        return "\n".join(nodos_tspan)

    except FileNotFoundError:
        print(f"Error de I/O: No se encontró '{RUTA_IMAGEN}'.")
        return None


def inyectar_en_svg(tspan_content):
    if not tspan_content:
        return

    patron = re.compile(r'(<text[^>]*class="ascii"[^>]*>)(.*?)(</text>)', re.DOTALL)

    for svg_file in ARCHIVOS_SVG:
        ruta = Path(svg_file)
        if not ruta.exists():
            print(f"⚠ Advertencia: '{svg_file}' no existe en el directorio de trabajo.")
            continue
            
        contenido = ruta.read_text(encoding="utf-8")
        
        # Reemplaza el bloque de texto respetando los tags de apertura/cierre originales
        nuevo_contenido = patron.sub(
            rf'\1\n{tspan_content}\n\3',
            contenido
        )
        
        ruta.write_text(nuevo_contenido, encoding="utf-8")
        print(f"✔ DOM de '{svg_file}' actualizado (Resolución: {ANCHO}x{ALTO}, Offset X: {X_BASE}).")


if __name__ == "__main__":
    tspan_buffer = generar_ascii_centrado()
    inyectar_en_svg(tspan_buffer)
