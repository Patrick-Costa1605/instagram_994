"""O cordel: uma corda que atravessa todos os slides (e, no feed, as capas vizinhas) com um nó direito em cada emenda.

Estilo «plano»: corda de manila com contorno escuro e a torção marcada por riscos, como numa ilustração de manual de nós.
Cada peça de corda entra num nó pelo fio de cima e sai pelo de baixo (dois cabos com as pontas soltas), por isso a corda
sobe e desce 28 px em cada emenda, como numa corda atada a sério."""
import math
import random

OUT_COL, BASE_COL, TICK_COL = "#4B361D", "#D8B67C", "#B08B54"
RW = 25                      # espessura da corda
HALF = 150                   # meia-largura do nó (inclui as pontas)


def _pts(x0, y0, x1, y1, sag, seed, step=18):
    r = random.Random(seed)
    n = max(2, int(abs(x1 - x0) / step))
    out = []
    for i in range(n + 1):
        t = i / n
        x = x0 + (x1 - x0) * t
        ss = t * t * (3 - 2 * t)
        y = y0 + (y1 - y0) * ss + sag * math.sin(math.pi * t) + (r.random() - .5) * 1.6 * (1 if abs(x1 - x0) > 300 else 0)
        out.append((x, y))
    return out


def _path(pts):
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)


def _rope(d, extra="", cap="butt"):
    """A corda desenhada em 4 camadas (sombra, contorno, base, torção)."""
    return (f'<path d="{d}" fill="none" stroke="{OUT_COL}" stroke-width="{RW + 7}" stroke-linecap="{cap}" stroke-linejoin="round" {extra}/>'
            f'<path d="{d}" fill="none" stroke="{BASE_COL}" stroke-width="{RW}" stroke-linecap="{cap}" stroke-linejoin="round" {extra}/>'
            f'<path d="{d}" fill="none" stroke="url(#tw)" stroke-width="{RW}" stroke-linecap="butt" stroke-linejoin="round" {extra}/>'
            f'<path d="{d}" fill="none" stroke="#fff" stroke-opacity=".38" stroke-width="3" stroke-linecap="round" transform="translate(0,-7)" {extra}/>')


def _no(cx, cy, uid, rot=0.0):
    """Nó direito: duas «línguas» enlaçadas (A com as pontas à esquerda, B com as pontas à direita).
    Origem no centro. O fio de cima da esquerda e o de baixo da direita continuam como corda; os outros dois são as pontas."""
    # A: pico deslocado para a esquerda; fio de cima longo (corda), fio de baixo curto (ponta)
    a = ("M -150,-14 L -128,-14 C -84,-14 -66,-47 -24,-47 C 42,-47 84,-24 84,0 C 84,24 42,47 -24,47 C -66,47 -84,14 -128,14 L -190,14")
    # B: espelho de A, com o pico deslocado para a direita
    b = ("M 150,14 L 128,14 C 84,14 66,47 24,47 C -42,47 -84,24 -84,0 C -84,-24 -42,-47 24,-47 C 66,-47 84,-14 128,-14 L 190,-14")
    return (f'<g transform="translate({cx:.1f},{cy:.1f}) rotate({rot})">'
            f'<defs><clipPath id="cb{uid}"><rect x="-40" y="6" width="80" height="62"/></clipPath></defs>'
            + _rope(b) + _rope(a)
            + f'<g clip-path="url(#cb{uid})">' + _rope(b) + '</g>'
            # pontas soltas: corte limpo, com a «cara» da corda
            + f'<path d="M -190,{14 - RW/2 - 3} L -190,{14 + RW/2 + 3}" stroke="{OUT_COL}" stroke-width="3.5"/>'
            + f'<path d="M 190,{-14 - RW/2 - 3} L 190,{-14 + RW/2 + 3}" stroke="{OUT_COL}" stroke-width="3.5"/></g>')


def corda_svg(n, W, H, y0, sag=20, seed=994):
    """SVG de n·W × H com o cordel a atravessar os n slides.

    Há um nó em x = 0, W, 2W … n·W (também nas bordas!). Assim, quando as capas de publicações seguidas ficam lado a lado no feed,
    a metade de nó que sai da direita de uma encaixa na metade que entra pela esquerda da seguinte (mesma geometria, mesma altura).
    Os nós têm todos a mesma posição e inclinação (0°) para as emendas coincidirem ao pixel."""
    total = n * W
    xs = [k * W for k in range(0, n + 1)]
    parts = []
    marcos = [-HALF - 400] + xs + [total + HALF + 400]
    for i in range(len(marcos) - 1):
        xa = marcos[i] + (HALF if i > 0 else 0)
        xb = marcos[i + 1] - (HALF if i < len(marcos) - 2 else 0)
        ya = y0 + (14 if i > 0 else 0)
        yb = y0 - (14 if i < len(marcos) - 2 else 0)
        parts.append(_rope(_path(_pts(xa, ya, xb, yb, sag, seed + i))))
    for k, x in enumerate(xs):
        parts.append(_no(x, y0, k, rot=0))
    defs = ('<defs><pattern id="tw" width="15" height="60" patternUnits="userSpaceOnUse">'
            f'<path d="M-3,60 L18,0" stroke="{TICK_COL}" stroke-width="3.4"/></pattern></defs>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{total}" height="{H}" viewBox="0 0 {total} {H}" class="cordel">'
            f'{defs}{"".join(parts)}</svg>')
