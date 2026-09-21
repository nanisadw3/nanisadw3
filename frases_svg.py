"""Genera assets/frases.svg: tarjeta animada que rota entre frases de desarrollo."""
from html import escape
from pathlib import Path

FRASES = [
    "El código que hoy te cuesta será mañana tu superpoder.",
    "Un bug es solo una lección con prisa.",
    "Escribe para quien lo leerá en seis meses: probablemente tú.",
    "Commit pequeño, avance constante.",
    "Automatiza lo repetitivo y dedica tu mente a lo creativo.",
    "La seguridad se diseña desde la primera línea, no al final.",
    "Cada error de compilación te acerca a que funcione.",
    "La constancia le gana al talento cuando el talento no compila.",
]
AUTOR = "— Iñaki Sobera Sotomayor"
ANCHO, ALTO = 640, 118
SEGUNDOS_POR_FRASE = 4.5
FUNDIDO = 0.10  # fracción del turno usada para aparecer y desaparecer


def puntos(i, n):
    turno = 1 / n
    ini, fin = i * turno, (i + 1) * turno
    f = FUNDIDO * turno
    pts = [(0.0, 0)]
    if ini > 0:
        pts.append((ini, 0))
    pts += [(ini + f, 1), (fin - f, 1), (fin, 0)]
    if fin < 1:
        pts.append((1.0, 0))
    return [(round(min(t, 1.0), 5), v) for t, v in pts]


def texto(i, n, frase, duracion):
    pts = puntos(i, n)
    tiempos = ";".join(str(t) for t, _ in pts)
    valores = ";".join(str(v) for _, v in pts)
    return (
        f'  <text x="{ANCHO // 2}" y="58" text-anchor="middle" font-size="17" '
        f'fill="#c9d1d9" opacity="0">{escape(frase)}\n'
        f'    <animate attributeName="opacity" dur="{duracion}s" repeatCount="indefinite" '
        f'keyTimes="{tiempos}" values="{valores}"/>\n  </text>'
    )


def main():
    n = len(FRASES)
    duracion = round(n * SEGUNDOS_POR_FRASE, 2)
    frases = "\n".join(texto(i, n, f, duracion) for i, f in enumerate(FRASES))
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{ANCHO}" height="{ALTO}" viewBox="0 0 {ANCHO} {ALTO}" role="img" aria-label="Frases motivacionales de desarrollo">
  <style>text {{ font-family: 'Segoe UI', Helvetica, Arial, sans-serif; }}</style>
  <rect x="0.5" y="0.5" width="{ANCHO - 1}" height="{ALTO - 1}" rx="12" fill="#0d1117" stroke="#30363d"/>
  <text x="22" y="52" font-size="52" fill="#58a6ff" opacity="0.55" font-family="Georgia, serif">“</text>
{frases}
  <text x="{ANCHO // 2}" y="94" text-anchor="middle" font-size="14" font-style="italic" fill="#58a6ff">{escape(AUTOR)}</text>
</svg>
"""
    salida = Path(__file__).parent / "assets" / "frases.svg"
    salida.write_text(svg, encoding="utf-8")
    print(f"{salida} ({n} frases, ciclo de {duracion}s)")


if __name__ == "__main__":
    main()
