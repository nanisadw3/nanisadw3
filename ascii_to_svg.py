from pathlib import Path
from html import escape

INPUT = "portrait.txt"
OUTPUT = "portrait_tspan.txt"

# START_X = 26 alinea el texto exactamente en el borde izquierdo de VISUAL.MAP
START_X = 26
START_Y = 80.00
LINE_HEIGHT = 7.40

lines = Path(INPUT).read_text(
    encoding="utf-8",
    errors="ignore"
).splitlines()

lines = [l.rstrip() for l in lines]

y = START_Y
svg = []
for line in lines:
    svg.append(
        f'<tspan x="{START_X}" y="{y:.2f}">{escape(line)}</tspan>'
    )
    y += LINE_HEIGHT

Path(OUTPUT).write_text(
    "\n".join(svg),
    encoding="utf-8"
)

print(f"✔ Generadas {len(svg)} líneas alineadas en el borde exacto (X={START_X}).")
