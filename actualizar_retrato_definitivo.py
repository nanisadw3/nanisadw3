# actualizar_retrato_definitivo.py
from PIL import Image
import re
from pathlib import Path

# --- CONFIGURACIÓN ---
RUTA_IMAGEN_ORIGINAL = "Gemini_Generated_Image_3mdvgr3mdvgr3mdv.png"
ARCHIVOS_SVG = ["dark.svg", "light.svg"]

# Dimensiones mayores para llenar el marco del SVG
NUEVO_ANCHO_ASCII = 160
NUEVA_ALTO_ASCII = 88

ASCII_CHARS = " .:-=+*#%@"

# Coordenadas y estilos precisos para el SVG
# y_start controla la altura de inicio, x_base el borde izquierdo
SVG_CONFIG = {
    'y_start': 130, # Ajusta esto para subir/bajar el bloque completo
    'y_step': 16,   # Distancia entre líneas
    'x_base': 80,  # Coordenada X base para el bloque
    'text_id': 'visual_map_ascii' # ID que usaremos para buscar en el SVG
}

def generar_y_centrar_ascii():
    try:
        # 1. Procesamiento estándar de imagen para enfocar el rostro
        img = Image.open(RUTA_IMAGEN_ORIGINAL).convert("L")
        ancho_orig, alto_orig = img.size
        # Un recorte más equilibrado
        izq = int(ancho_orig * 0.1)
        der = int(ancho_orig * 0.95)
        nuevo_ancho_crop = der - izq
        
        # Proporción física (1.10) para evitar estiramiento
        ratio_fisico_svg = 1.10
        alto_ideal = int(nuevo_ancho_crop / ratio_fisico_svg)
        margen_y = max(0, (alto_orig - alto_ideal) // 2)
        sup = int(margen_y * 0.8)
        inf = min(alto_orig, sup + alto_ideal)
        
        img_recortada = img.crop((izq, sup, der, inf))
        img_final = img_recortada.resize((NUEVO_ANCHO_ASCII, NUEVA_ALTO_ASCII))

        # 2. Generar líneas de caracteres en crudo
        pixeles = list(img_final.getdata())
        caracteres = [ASCII_CHARS[pixel * len(ASCII_CHARS) // 256] for pixel in pixeles]
        lineas_crudas = ["".join(caracteres[i:i + NUEVO_ANCHO_ASCII]) for i in range(0, len(caracteres), NUEVO_ANCHO_ASCII)]

        # 3. Calcular padding para centrado perfecto dentro del bloque de texto
        # Encontramos la columna de inicio y fin real del contenido (no espacios)
        primer_columna = NUEVO_ANCHO_ASCII
        ultima_columna = 0
        for linea in lineas_crudas:
            linea_limpia = linea.rstrip()
            if not linea_limpia: continue # Saltar líneas vacías
            trimmed_l = linea.lstrip()
            inicio = NUEVO_ANCHO_ASCII - len(trimmed_l)
            primer_columna = min(primer_columna, inicio)
            ultima_columna = max(ultima_columna, len(linea_limpia))

        ancho_contenido = ultima_columna - primer_columna
        total_padding = NUEVO_ANCHO_ASCII - ancho_contenido
        padding_izq = total_padding // 2
        
        # Regenerar líneas con padding explícito
        lineas_centradas = []
        for linea in lineas_crudas:
            if not linea.rstrip(): # Manejar líneas vacías
                lineas_centradas.append(" " * NUEVO_ANCHO_ASCII)
                continue
            # Tomar el contenido real de la línea cruda y añadirle padding simétrico
            contenido_recortado = linea[primer_columna:ultima_columna]
            lineas_centradas.append(" " * padding_izq + contenido_recortado + " " * (total_padding - padding_izq))

        # 4. Generar el bloque tspan para SVG
        tspan_completo = ""
        for i, linea in enumerate(lineas_centradas):
            # Escapar caracteres XML
            linea_escapada = (linea.replace('&', '&amp;')
                                   .replace('<', '&lt;')
                                   .replace('>', '&gt;')
                                   .replace('"', '&quot;')
                                   .replace("'", '&apos;'))
            
            y_coord = SVG_CONFIG['y_start'] + i * SVG_CONFIG['y_step']
            tspan_completo += f'<tspan x="{SVG_CONFIG["x_base"]}" y="{y_coord}">{linea_escapada}</tspan>\n'

        return tspan_completo

    except FileNotFoundError:
        print(f"Error: No se encontró '{RUTA_IMAGEN_ORIGINAL}'.")
        return None

def actualizar_archivos_svg(contenido_ascii_tspan):
    if not contenido_ascii_tspan: return

    for archivo in ARCHIVOS_SVG:
        ruta = Path(archivo)
        if not ruta.exists():
            print(f"⚠ No se encontró {archivo}")
            continue
        
        print(f"⌛ Actualizando {archivo}...")
        contenido_svg = ruta.read_text(encoding="utf-8")
        
        # Buscamos la etiqueta <text ... class="ascii"> por su ID o clase y reemplazamos todo
        # Es más robusto buscar y reemplazar el bloque completo.
        patron = r'(<text[^>]*class="ascii"[^>]*>)(.*?)(</text>)'
        
        # Si no tiene ID, lo añadimos para un centrado más fácil
        def replace_with_positioning(match):
            abrir_tag = match.group(1)
            # Asegurar que tenga el ID correcto para futuras referencias si es necesario
            if 'id="' not in abrir_tag:
                abrir_tag = abrir_tag.replace('class="ascii"', f'id="{SVG_CONFIG["text_id"]}" class="ascii"')
            # Reemplazar coordenadas x/y si existen para posicionar el bloque completo
            abrir_tag = re.sub(r'x="[^"]*"', f'x="{SVG_CONFIG["x_base"]}"', abrir_tag)
            # El y inicial no es tan importante para el bloque <text> si usamos <tspan> con y absolutos,
            # pero lo ajustamos por limpieza.
            abrir_tag = re.sub(r'y="[^"]*"', f'y="{SVG_CONFIG["y_start"]}"', abrir_tag)

            return f'{abrir_tag}\n{contenido_ascii_tspan}{match.group(3)}'

        nuevo_contenido_svg = re.sub(
            patron,
            replace_with_positioning,
            contenido_svg,
            flags=re.DOTALL
        )
        
        ruta.write_text(nuevo_contenido_svg, encoding="utf-8")
        print(f"✔ ¡Arte ASCII centrado y proporcionado actualizado en: {archivo}")

if __name__ == "__main__":
    tspan_content = generar_y_centrar_ascii()
    actualizar_archivos_svg(tspan_content)
