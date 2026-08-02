import re
from pathlib import Path

# 1. Leer las líneas generadas de tu retrato
tspan_content = Path("portrait_tspan.txt").read_text(encoding="utf-8")

# 2. Reemplazar el bloque ASCII en dark.svg y light.svg
for svg_file in ["dark.svg", "light.svg"]:
    path = Path(svg_file)
    if not path.exists():
        print(f"⚠ No se encontró {svg_file}")
        continue
        
    content = path.read_text(encoding="utf-8")
    
    # Busca la etiqueta <text ... class="ascii"> y reemplaza todo su contenido hasta </text>
    new_content = re.sub(
        r'(<text[^>]*class="ascii"[^>]*>)(.*?)(</text>)',
        r'\1\n' + tspan_content + r'\n\3',
        content,
        flags=re.DOTALL
    )
    
    path.write_text(new_content, encoding="utf-8")
    print(f"✔ Arte ASCII actualizado correctamente en: {svg_file}")

