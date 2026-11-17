#!/usr/bin/env python3
"""Gera os motivos de fundo (SVG 1080×1350, cor = currentColor) de «As Nossas Secções».
Uso: python src/motivos.py   ->  series/nossas_seccoes/motivos/{folhas,topografia,blueprint,montanha}.svg"""
import math
import random
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "series" / "nossas_seccoes" / "motivos"
W, H = 1080, 1350


def svg(body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice">{body}</svg>'


def folhas():
    """Jângal: folhas e fetos grandes a sair dos cantos."""
    r = random.Random(994)
    out = []
    spots = [(40, 80), (200, 40), (980, 120), (1060, 330), (30, 520), (1040, 760), (70, 940), (960, 1180), (120, 1290), (860, 1330), (560, 40), (1010, 560)]
    for (x, y) in spots:
        for k in range(r.randint(2, 3)):
            sz, rot = r.uniform(110, 230), r.uniform(0, 360)
            out.append(f'<g transform="translate({x + r.uniform(-50, 50):.0f},{y + r.uniform(-50, 50):.0f}) rotate({rot:.0f}) scale({sz / 100:.2f})">'
                       '<path d="M0,-100 C60,-55 60,55 0,100 C-60,55 -60,-55 0,-100Z" fill="currentColor"/>'
                       '<path d="M0,-92 L0,92 M0,-40 L30,-62 M0,-5 L36,-30 M0,30 L30,10 M0,-40 L-30,-62 M0,-5 L-36,-30 M0,30 L-30,10" '
                       'stroke="#000" stroke-opacity=".35" stroke-width="3" fill="none"/></g>')
    return svg("".join(out))


def topografia():
    """Exploradores: curvas de nível, como num mapa."""
    out = []
    for (cx, cy, n, ph) in ((880, 330, 11, 0.4), (170, 1080, 12, 2.1), (620, 1380, 6, 1.0)):
        for k in range(1, n + 1):
            r = 55 + k * 52
            pts = []
            for i in range(0, 121):
                t = i / 120 * 2 * math.pi
                rr = r * (1 + 0.10 * math.sin(3 * t + ph + k * 0.15) + 0.06 * math.sin(5 * t + ph * 2) + 0.03 * math.sin(7 * t + k))
                pts.append(f"{cx + rr * math.cos(t) * 1.15:.1f},{cy + rr * math.sin(t):.1f}")
            out.append(f'<polygon points="{" ".join(pts)}" fill="none" stroke="currentColor" stroke-width="3"/>')
    return svg("".join(out))


def blueprint():
    """Pioneiros: papel de projeto, com quadrícula, cotas e amarras."""
    out = []
    for x in range(0, W + 1, 54):
        major = x % 270 == 0
        out.append(f'<path d="M{x},0 V{H}" stroke="currentColor" stroke-width="{3 if major else 1.2}" opacity="{1 if major else .6}"/>')
    for y in range(0, H + 1, 54):
        major = y % 270 == 0
        out.append(f'<path d="M0,{y} H{W}" stroke="currentColor" stroke-width="{3 if major else 1.2}" opacity="{1 if major else .6}"/>')
    # esboço: dois paus cruzados com amarra, cotas e círculo de compasso
    out.append('<g stroke="currentColor" stroke-width="9" fill="none" stroke-linecap="round">'
               '<path d="M690,160 L1000,420"/><path d="M700,430 L990,150"/>'
               '<path d="M800,255 l38,34 M790,300 l38,-34 M812,275 l30,0" stroke-width="5"/></g>')
    out.append('<g stroke="currentColor" stroke-width="4" fill="none"><path d="M680,500 H1010 M680,486 v28 M1010,486 v28"/>'
               '<circle cx="190" cy="1110" r="150" stroke-dasharray="14 12"/><path d="M190,1110 L320,1190" /><circle cx="190" cy="1110" r="7" fill="currentColor"/></g>')
    return svg("".join(out))


def montanha():
    """Caminheiros: cumes e trilho."""
    r = random.Random(7)
    out = []
    for layer, (base, amp, op) in enumerate(((1010, 230, .55), (1120, 200, .75), (1230, 170, 1.0))):
        pts = [(0, H), (0, base)]
        x = 0
        while x < W:
            x += r.randint(90, 190)
            pts.append((min(x, W), base - r.randint(40, amp)))
            x += r.randint(40, 120)
            pts.append((min(x, W), base - r.randint(0, 50)))
        pts += [(W, H)]
        out.append(f'<polygon points="{" ".join(f"{a},{b}" for a, b in pts)}" fill="currentColor" opacity="{op}"/>')
    out.append('<path d="M120,1300 C320,1200 260,1100 470,1060 S760,1090 930,960" stroke="#fff" stroke-opacity=".6" stroke-width="6" '
               'stroke-dasharray="2 22" stroke-linecap="round" fill="none"/>')
    for (x, y) in ((880, 140), (140, 190)):                         # sol / lua
        out.append(f'<circle cx="{x}" cy="{y}" r="70" fill="currentColor"/>')
    return svg("".join(out))


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for nome, fn in (("folhas", folhas), ("topografia", topografia), ("blueprint", blueprint), ("montanha", montanha)):
        (OUT / f"{nome}.svg").write_text(fn(), encoding="utf-8")
        print(OUT / f"{nome}.svg")
