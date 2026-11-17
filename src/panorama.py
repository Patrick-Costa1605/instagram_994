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


def trilho(n, W, tons, y_base=705, passo=76, smin=0.50, smax=1.45, y_ini=1010, amp=62, hump=0):
    """Devolve a estrada (path SVG), as pegadas e a altura da estrada em cada x.

    tons = cores (hex) dos pés de cada slide, do 1.º (capa) ao último, para a pegada ir mudando de cor."""
    total = n * W

    def y(x):
        if hump and 0 <= x <= W:
            return y_base + hump * math.sin(math.pi * x / W)
        if x < W * 1.05:
            return y_ini * (1 - _ss(x / (W * 1.05))) + y_base * _ss(x / (W * 1.05))
        return y_base + amp * math.sin((x - W * 1.05) / 1150 * 2 * math.pi)

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
            s = smin + (smax - smin) * (px / total)
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


# ------------------------------------------------------------------ motivos de fundo (o imaginário de cada secção)
def motivo(nome, total, H=1350, seed=994):
    """SVG (cor = currentColor) com o imaginário da secção: selva, terra, navegacao, homem_novo."""
    import random
    r = random.Random(seed)
    o = []
    if nome == "selva":                                   # Lobitos: folhas da Selva
        n = int(total / 240)
        for i in range(n):
            x = (i + r.random()) * total / n
            y = r.choice((r.uniform(10, 190), r.uniform(1110, 1340)))
            sz, rot = r.uniform(70, 150), r.uniform(0, 360)
            o.append(f'<g transform="translate({x:.0f},{y:.0f}) rotate({rot:.0f}) scale({sz/100:.2f})"><path d="M0,-100 C60,-55 60,55 0,100 C-60,55 -60,-55 0,-100Z" fill="currentColor"/>'
                     '<path d="M0,-92 L0,92 M0,-40 L30,-62 M0,-5 L36,-30 M0,30 L30,10 M0,-40 L-30,-62 M0,-5 L-36,-30 M0,30 L-30,10" stroke="#fff" stroke-opacity=".5" stroke-width="3" fill="none"/></g>')
    elif nome == "terra":                                 # Exploradores: dunas e sol da Terra Prometida
        for k, (base, amp, op) in enumerate(((1130, 70, .5), (1190, 60, .75), (1255, 50, 1.0))):
            pts = [(-20, H + 10)] + [(x, base + amp * math.sin(x / (520 - 60 * k) * 2 * math.pi + k * 1.7)) for x in range(-20, int(total) + 60, 40)] + [(total + 20, H + 10)]
            o.append(f'<polygon points="{" ".join(f"{a:.0f},{b:.0f}" for a, b in pts)}" fill="currentColor" opacity="{op}"/>')
        for cx in (total * 0.18, total * 0.62, total * 0.93):
            o.append(f'<circle cx="{cx:.0f}" cy="215" r="{r.randint(70, 105)}" fill="currentColor" opacity=".75"/>')
    elif nome == "navegacao":                             # Pioneiros: ondas, velas e bússola
        for k in range(3):
            pts = [(x, 1150 + 52 * k + 20 * math.sin(x / (210 + 40 * k) * 2 * math.pi + k)) for x in range(-20, int(total) + 60, 30)]
            o.append(f'<polyline points="{" ".join(f"{a:.0f},{b:.0f}" for a, b in pts)}" fill="none" stroke="currentColor" stroke-width="7" stroke-linecap="round" opacity="{.9 - .2 * k}"/>')
        for cx in (total * 0.12, total * 0.47, total * 0.81):
            o.append(f'<g transform="translate({cx:.0f},1130)"><path d="M-70,0 L70,0 L45,38 L-45,38Z" fill="currentColor"/><path d="M0,-150 L0,-6 L-60,-6Z" fill="currentColor"/><path d="M8,-130 L8,-6 L58,-6Z" fill="currentColor" opacity=".7"/></g>')
        o.append(f'<g transform="translate({total*0.73:.0f},170)" stroke="currentColor" fill="none" stroke-width="6"><circle r="90"/><circle r="70" stroke-width="3"/><path d="M0,-90 L18,0 L0,90 L-18,0Z" fill="currentColor" stroke="none"/><path d="M-90,0 L0,-14 L90,0 L0,14Z" fill="currentColor" opacity=".5" stroke="none"/></g>')
    else:                                                 # Caminheiros: montanhas e nascer do sol (Homem Novo)
        for k, (base, amp, op) in enumerate(((1020, 260, .55), (1130, 210, .8), (1240, 160, 1.0))):
            pts, x = [(-20, H + 10), (-20, base)], -20
            while x < total + 40:
                x += r.randint(110, 230)
                pts.append((x, base - r.randint(30, amp)))
                x += r.randint(40, 130)
                pts.append((x, base - r.randint(0, 50)))
            pts.append((total + 40, H + 10))
            o.append(f'<polygon points="{" ".join(f"{a:.0f},{b:.0f}" for a, b in pts)}" fill="currentColor" opacity="{op}"/>')
        for cx in (total * 0.2, total * 0.66):
            o.append(f'<circle cx="{cx:.0f}" cy="190" r="95" fill="currentColor" opacity=".7"/>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {total:.0f} {H}" width="{total:.0f}" height="{H}">{"".join(o)}</svg>'
