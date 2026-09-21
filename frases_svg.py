"""Genera assets/frases.svg: tarjeta animada en dos renglones con frases de desarrollo e IA."""
from html import escape
from pathlib import Path

FRASES = [
    (
        "La IA no reemplaza al buen arquitecto; multiplica la visión de quien domina",
        "la ingeniería de software, los modelos de pesos abiertos y la robustez del backend."
    ),
    (
        "Un prompt puede generar una idea en segundos, pero solo una arquitectura sólida,",
        "pipelines RAG precisos y código limpio la convierten en una solución de impacto."
    ),
    (
        "Entrena tu criterio técnico con la misma disciplina que un modelo neuronal:",
        "cada error en consola y cada bug en producción es solo una época más de aprendizaje."
    ),
    (
        "La verdadera innovación con agentes autónomos nace de bases de datos confiables,",
        "protocolos estándar como MCP y sistemas diseñados para respetar la privacidad."
    ),
    (
        "Automatiza con inteligencia artificial todo aquello que sea repetitivo,",
        "y dedica tu ingenio a resolver los desafíos más complejos de la computación."
    ),
    (
        "Construir software y agentes locales de pesos abiertos exige paciencia y rigor:",
        "un commit consciente y bien probado siempre supera a cien líneas improvisadas."
    ),
    (
        "La seguridad y la ética no se añaden como un parche al final del despliegue;",
        "se forjan desde el diseño del sistema, la primera consulta y cada endpoint."
    ),
    (
        "La constancia técnica siempre superará a la casualidad, y la disciplina diaria",
        "es el algoritmo definitivo para construir tecnología que trascienda."
    ),
]
AUTOR = "— Iñaki Sobera Sotomayor"
ANCHO, ALTO = 720, 142
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
        f'    <text x="{ANCHO // 2}" y="54" text-anchor="middle" font-size="14" fill="#c9d1d9">{escape(r1)}</text>\n'
        f'    <text x="{ANCHO // 2}" y="78" text-anchor="middle" font-size="14" fill="#c9d1d9">{escape(r2)}</text>\n'
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
  <text x="26" y="56" font-size="50" fill="#58a6ff" opacity="0.45" font-family="Georgia, serif">“</text>
{frases}
  <text x="{ANCHO // 2}" y="114" text-anchor="middle" font-size="13" font-style="italic" fill="#58a6ff">{escape(AUTOR)}</text>
</svg>
"""
    salida = Path(__file__).parent / "assets" / "frases.svg"
    salida.write_text(svg, encoding="utf-8")
    print(f"{salida} ({n} frases en dos renglones, ciclo de {duracion}s)")


if __name__ == "__main__":
    main()
