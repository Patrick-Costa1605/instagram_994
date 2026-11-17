"""Carrossel panorâmico: um trilho contínuo (estrada + pegadas) que atravessa todos os slides.
As pegadas começam pequeninas e vão crescendo ao longo das idades."""
import math


def _ss(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def _mix(a, b, k):
    return tuple(round(x + (y - x) * k) for x, y in zip(a, b))


def _rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def trilho(n, W, tons, y_base=705, passo=76):
    """Devolve a estrada (path SVG), as pegadas e a altura da estrada em cada x.

    tons = cores (hex) dos pés de cada slide, do 1.º (capa) ao último, para a pegada ir mudando de cor."""
    total = n * W

    def y(x):
        if x < W * 1.05:
            return 1010 * (1 - _ss(x / (W * 1.05))) + y_base * _ss(x / (W * 1.05))
        return y_base + 62 * math.sin((x - W * 1.05) / 1150 * 2 * math.pi)

    pts = [(x, y(x)) for x in range(-60, total + 80, 8)]
    d = "M" + " L".join(f"{px:.0f},{py:.1f}" for px, py in pts)
    centros = [W * (i + 0.5) for i in range(n)]
    cols = [_rgb(t) for t in tons]

    def cor(x):
        if x <= centros[0]:
            return cols[0]
        if x >= centros[-1]:
            return cols[-1]
        i = int(x // W) if x // W < n - 1 else n - 2
        i = max(0, min(n - 2, int((x - centros[0]) // W)))
        return _mix(cols[i], cols[i + 1], (x - centros[i]) / W)

    pegadas, acc, nxt, k = [], 0.0, 40.0, 0
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        seg = math.hypot(x1 - x0, y1 - y0)
        while acc + seg >= nxt:
            t = (nxt - acc) / seg
            px, py = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
            ang = math.atan2(y1 - y0, x1 - x0)
            side = 1 if k % 2 == 0 else -1
            s = 0.50 + 0.95 * (px / total)
            off = 20 * s
            px += -math.sin(ang) * off * side
            py += math.cos(ang) * off * side
            r, g, b = cor(px)
            pegadas.append({"x": round(px, 1), "y": round(py, 1), "rot": round(math.degrees(ang) + 90, 1),
                            "s": round(s, 3), "lado": side, "cor": f"rgb({r},{g},{b})"})
            nxt += passo * (0.65 + 0.35 * s)
            k += 1
        acc += seg
    return {"d": d, "pegadas": pegadas, "y": y}
