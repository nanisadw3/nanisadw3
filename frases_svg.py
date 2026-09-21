"""Genera assets/frases.svg: tarjeta animada que rota entre frases de desarrollo e IA."""
from html import escape
from pathlib import Path

FRASES = [
    "La IA no reemplaza al buen ingeniero; potencia la visión de quien domina la arquitectura y el código a fondo.",
    "Entrena tu lógica como a una red neuronal: cada error de compilación es solo una época más de aprendizaje.",
    "Automatiza con inteligencia lo repetitivo y enfoca tu creatividad en resolver problemas de alto impacto.",
    "La verdadera IA nace de bases de datos limpias, algoritmos seguros y sistemas diseñados con propósito.",
    "Diseña pensando en escalabilidad y seguridad: la IA acelera el camino, pero tu criterio define el destino.",
    "Un fallo en producción no es el final; es el mejor dataset para entrenar una solución mucho más robusta.",
    "El prompt perfecto inspira ideas, pero la arquitectura sólida y el código limpio las hacen realidad.",
    "La constancia le gana al talento, y la disciplina supera a cualquier algoritmo sin una dirección clara.",
]
AUTOR = "— Iñaki Sobera Sotomayor"
ANCHO, ALTO = 680, 122
SEGUNDOS_POR_FRASE = 5.0
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


def texto(i, n, frase, duracion):
    pts = puntos(i, n)
    tiempos = ";".join(str(t) for t, _ in pts)
    valores = ";".join(str(v) for _, v in pts)
    return (
        f'  <text x="{ANCHO // 2}" y="60" text-anchor="middle" font-size="14" '
        f'fill="#c9d1d9" opacity="0">{escape(frase)}\n'
        f'    <animate attributeName="opacity" dur="{duracion}s" repeatCount="indefinite" '
        f'keyTimes="{tiempos}" values="{valores}"/>\n  </text>'
    )


def main():
    n = len(FRASES)
    duracion = round(n * SEGUNDOS_POR_FRASE, 2)
    frases = "\n".join(texto(i, n, f, duracion) for i, f in enumerate(FRASES))
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{ANCHO}" height="{ALTO}" viewBox="0 0 {ANCHO} {ALTO}" role="img" aria-label="Frases motivacionales de desarrollo e Inteligencia Artificial">
  <style>text {{ font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif; }}</style>
  <rect x="0.5" y="0.5" width="{ANCHO - 1}" height="{ALTO - 1}" rx="12" fill="#0d1117" stroke="#30363d"/>
  <text x="24" y="52" font-size="48" fill="#58a6ff" opacity="0.5" font-family="Georgia, serif">“</text>
{frases}
  <text x="{ANCHO // 2}" y="98" text-anchor="middle" font-size="13.5" font-style="italic" fill="#58a6ff">{escape(AUTOR)}</text>
</svg>
"""
    salida = Path(__file__).parent / "assets" / "frases.svg"
    salida.write_text(svg, encoding="utf-8")
    print(f"{salida} ({n} frases, ciclo de {duracion}s)")


if __name__ == "__main__":
    main()
