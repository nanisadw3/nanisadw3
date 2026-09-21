"""Genera assets/frases.svg: tarjeta animada en dos renglones con frases de desarrollo e IA."""
from html import escape
from pathlib import Path

FRASES = [
    (
        "La IA no reemplaza al buen arquitecto;",
        "potencia a quien domina la robustez del backend."
    ),
    (
        "Un prompt genera ideas en segundos, pero la arquitectura",
        "y el código limpio las convierten en soluciones reales."
    ),
    (
        "Entrena tu lógica con disciplina técnica:",
        "cada bug superado es una época más de aprendizaje."
    ),
    (
        "Agentes autónomos y modelos de pesos abiertos:",
        "el futuro del software con soberanía y privacidad."
    ),
    (
        "Automatiza con inteligencia artificial lo repetitivo,",
        "y enfoca tu talento en diseñar sistemas de alto impacto."
    ),
    (
        "Construir IA local exige paciencia y rigor:",
        "un commit sólido vale más que cien líneas improvisadas."
    ),
    (
        "La seguridad y la ética no son un parche final;",
        "se programan desde la arquitectura y cada endpoint."
    ),
    (
        "La constancia técnica siempre le gana a la casualidad;",
        "la disciplina es el algoritmo que construye el éxito."
    ),
]
AUTOR = "— Iñaki Sobera Sotomayor"
ANCHO, ALTO = 540, 136
SEGUNDOS_POR_FRASE = 5.5
FUNDIDO = 0.08  # fracción del turno usada para aparecer y desaparecer


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


def texto(i, n, renglones, duracion):
    pts = puntos(i, n)
    tiempos = ";".join(str(t) for t, _ in pts)
    valores = ";".join(str(v) for _, v in pts)
    r1, r2 = renglones
    return (
        f'  <g opacity="0">\n'
        f'    <text x="{ANCHO // 2}" y="52" text-anchor="middle" font-size="13.5" fill="#c9d1d9">{escape(r1)}</text>\n'
        f'    <text x="{ANCHO // 2}" y="74" text-anchor="middle" font-size="13.5" fill="#c9d1d9">{escape(r2)}</text>\n'
        f'    <animate attributeName="opacity" dur="{duracion}s" repeatCount="indefinite" '
        f'keyTimes="{tiempos}" values="{valores}"/>\n'
        f'  </g>'
    )


def main():
    n = len(FRASES)
    duracion = round(n * SEGUNDOS_POR_FRASE, 2)
    frases = "\n".join(texto(i, n, f, duracion) for i, f in enumerate(FRASES))
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{ANCHO}" height="{ALTO}" viewBox="0 0 {ANCHO} {ALTO}" role="img" aria-label="Frases motivacionales de desarrollo e Inteligencia Artificial">
  <style>text {{ font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif; }}</style>
  <rect x="0.5" y="0.5" width="{ANCHO - 1}" height="{ALTO - 1}" rx="12" fill="#0d1117" stroke="#30363d"/>
  <text x="20" y="52" font-size="44" fill="#58a6ff" opacity="0.45" font-family="Georgia, serif">“</text>
{frases}
  <text x="{ANCHO // 2}" y="108" text-anchor="middle" font-size="12.5" font-style="italic" fill="#58a6ff">{escape(AUTOR)}</text>
</svg>
"""
    salida = Path(__file__).parent / "assets" / "frases.svg"
    salida.write_text(svg, encoding="utf-8")
    print(f"{salida} ({n} frases en dos renglones, ciclo de {duracion}s)")


if __name__ == "__main__":
    main()
