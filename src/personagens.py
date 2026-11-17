#!/usr/bin/env python3
"""Desenha as 4 personagens de «As Nossas Secções» (a mesma criança a crescer) em SVG.
Uso: python src/personagens.py  ->  series/nossas_seccoes/personagens/{lobitos,exploradores,pioneiros,caminheiros}.svg"""
import math
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "series" / "nossas_seccoes" / "personagens"
INK, SHIRT, SHORTS, SHOE, CREAM = "#3B2A22", "#EBD9B0", "#4F6C9E", "#7A4B2A", "#FFF7E8"

# estágio: cor do lenço, tom de pele, cabelo
SEC = {
    "lobitos":      dict(stage=0, scarf="#F2C230", skin="#FFD9B8", hair="#7A5230"),
    "exploradores": dict(stage=1, scarf="#1E9E4A", skin="#F3C7A0", hair="#3A2A20"),
    "pioneiros":    dict(stage=2, scarf="#2F5FD0", skin="#E3AE86", hair="#2B1E18"),
    "caminheiros":  dict(stage=3, scarf="#D93A2B", skin="#D49A72", hair="#241915"),
}


def shade(hexc, k):
    r, g, b = (int(hexc[i:i + 2], 16) for i in (1, 3, 5))
    f = lambda c: max(0, min(255, round(c * k if k < 1 else c + (255 - c) * (k - 1))))
    return "#%02X%02X%02X" % (f(r), f(g), f(b))


def kid(name):
    d = SEC[name]; s = d["stage"]; skin, hair, scarf = d["skin"], d["hair"], d["scarf"]
    R = [98, 92, 86, 80][s]; torso = [104, 128, 150, 172][s]; leg = [58, 82, 104, 126][s]; tw = [126, 136, 146, 156][s]
    arm = [60, 70, 82, 94][s]
    yl = -leg; tb = yl + 12; tt = tb - torso; hy = tt - R * 0.97
    o = []
    add = o.append
    # ------------- atrás: mochilas
    if s in (1, 3):
        bw = tw + (34 if s == 1 else 52)
        col = shade(scarf, 0.72)
        add(f'<rect x="{-bw/2}" y="{tt-10-(34 if s==3 else 0)}" width="{bw}" height="{torso+(34 if s==3 else 8)}" rx="34" fill="{col}"/>')
        if s == 3:
            add(f'<rect x="{-bw/2+6}" y="{tt-58}" width="{bw-12}" height="40" rx="20" fill="{shade(scarf,1.25)}"/>')
    # ------------- pernas, sapatos, calções
    for sx in (-1, 1):
        add(f'<line x1="{sx*tw*0.22}" y1="{yl}" x2="{sx*tw*0.25}" y2="-14" stroke="{skin}" stroke-width="{26+s*3}" stroke-linecap="round"/>')
        add(f'<ellipse cx="{sx*(tw*0.25+7)}" cy="-9" rx="{30+s*2}" ry="15" fill="{SHOE}"/>')
        add(f'<ellipse cx="{sx*(tw*0.25+7)}" cy="-3" rx="{30+s*2}" ry="6" fill="{shade(SHOE,.7)}"/>')
    add(f'<rect x="{-tw/2+3}" y="{yl-8}" width="{tw-6}" height="{leg*0.5}" rx="18" fill="{SHORTS}"/>')
    add(f'<line x1="0" y1="{yl+6}" x2="0" y2="{yl+leg*0.46}" stroke="{shade(SHORTS,.75)}" stroke-width="4" stroke-linecap="round"/>')
    # ------------- camisa
    add(f'<rect x="{-tw/2}" y="{tt}" width="{tw}" height="{torso}" rx="36" fill="{SHIRT}"/>')
    add(f'<rect x="{tw/2-26}" y="{tt+6}" width="22" height="{torso-12}" rx="11" fill="#000" opacity=".05"/>')
    add(f'<rect x="{-tw/2+10}" y="{tb-30}" width="{tw-20}" height="12" rx="6" fill="{shade(SHORTS,.8)}" opacity=".9"/>')
    # ------------- lenço (volume: gola + 2 pontas + argola)
    for sx, ln, rot in ((-1, torso * 0.78, 8), (1, torso * 0.66, -8)):
        add(f'<g transform="translate({sx*10},{tt+8}) rotate({rot*sx*-1})"><path d="M {-38} 0 L 38 0 L {sx*-4} {ln} Z" fill="{scarf}" stroke="{scarf}" stroke-width="10" stroke-linejoin="round"/>'
            f'<path d="M {-38} 0 L 38 0 L {sx*-4} {ln} Z" fill="none" stroke="{CREAM}" stroke-width="4" stroke-linejoin="round" transform="translate(0,0) scale(.8)" opacity=".85"/></g>')
    add(f'<path d="M {-tw*0.42} {tt-6} Q 0 {tt+34} {tw*0.42} {tt-6}" fill="none" stroke="{shade(scarf,.85)}" stroke-width="30" stroke-linecap="round"/>')
    add(f'<path d="M {-tw*0.40} {tt-10} Q 0 {tt+24} {tw*0.40} {tt-10}" fill="none" stroke="{shade(scarf,1.25)}" stroke-width="10" stroke-linecap="round" opacity=".7"/>')
    add(f'<circle cx="0" cy="{tt+24}" r="11" fill="#9A6A3A"/><circle cx="-3" cy="{tt+21}" r="3.5" fill="#fff" opacity=".7"/>')
    # ------------- braços (esq. em baixo; dir. a acenar)
    shx = tw / 2 - 8
    ly = tt + 30
    lend = (-tw / 2 - 20, ly + arm)
    rend = (tw / 2 + arm * 0.62, ly - arm * 0.78)
    for (sx, end) in ((-1, lend), (1, rend)):
        add(f'<line x1="{sx*shx}" y1="{ly}" x2="{end[0]}" y2="{end[1]}" stroke="{skin}" stroke-width="{26+s*2}" stroke-linecap="round"/>')
        mx, my = sx * shx + (end[0] - sx * shx) * 0.42, ly + (end[1] - ly) * 0.42
        add(f'<line x1="{sx*shx}" y1="{ly}" x2="{mx}" y2="{my}" stroke="{SHIRT}" stroke-width="{40+s*2}" stroke-linecap="round"/>')
    # ------------- paus / adereços nas mãos
    if s >= 2:
        sx_, top = lend[0] - 4, tt - 150 - (40 if s == 3 else 0)
        add(f'<line x1="{sx_}" y1="-6" x2="{sx_}" y2="{top}" stroke="#A9743F" stroke-width="13" stroke-linecap="round"/>')
        if s == 2:
            add(f'<line x1="{sx_-34}" y1="{top+26}" x2="{sx_+34}" y2="{top+26}" stroke="#A9743F" stroke-width="11" stroke-linecap="round"/>'
                f'<path d="M {sx_-9} {top+14} l 18 24 M {sx_+9} {top+14} l -18 24" stroke="#F8F1DE" stroke-width="4" stroke-linecap="round"/>')
        add(f'<line x1="{sx_+3}" y1="{top+30}" x2="{sx_+3}" y2="{top+200}" stroke="#fff" stroke-opacity=".18" stroke-width="3"/>')
    hr = [15, 17, 19, 21][s]
    add(f'<circle cx="{lend[0]}" cy="{lend[1]}" r="{hr}" fill="{skin}"/>')
    add(f'<circle cx="{rend[0]}" cy="{rend[1]}" r="{hr}" fill="{skin}"/>')
    # ------------- cabeça
    add(f'<g transform="translate(0,{hy})">')
    if s == 0:                                                    # capuz de lobo
        hood, fur = "#A8805A", "#E8CFA6"
        add(f'<polygon points="{-0.88*R},{-0.62*R} {-0.74*R},{-1.62*R} {-0.18*R},{-1.0*R}" fill="{hood}" stroke="{hood}" stroke-width="14" stroke-linejoin="round"/>'
            f'<polygon points="{0.88*R},{-0.62*R} {0.74*R},{-1.62*R} {0.18*R},{-1.0*R}" fill="{hood}" stroke="{hood}" stroke-width="14" stroke-linejoin="round"/>'
            f'<polygon points="{-0.78*R},{-0.76*R} {-0.70*R},{-1.34*R} {-0.34*R},{-0.98*R}" fill="#F0A9A8"/>'
            f'<polygon points="{0.78*R},{-0.76*R} {0.70*R},{-1.34*R} {0.34*R},{-0.98*R}" fill="#F0A9A8"/>')
        add(f'<circle r="{R*1.16}" fill="{hood}"/>')
    for sx in (-1, 1):
        add(f'<circle cx="{sx*R*0.97}" cy="{R*0.08}" r="{R*0.2}" fill="{shade(skin,.92)}"/>')
    add(f'<circle r="{R}" fill="{skin}"/>')
    if s == 0:
        add(f'<path d="M {-R*0.96:.1f} {-R*0.12:.1f} A {R*0.96:.1f} {R*0.96:.1f} 0 0 1 {R*0.96:.1f} {-R*0.12:.1f}" fill="none" stroke="{fur}" stroke-width="{R*0.30:.1f}" stroke-linecap="round"/>')
    else:                                                         # cabelo
        add(f'<path d="M {-R} {-0.1*R} A {R} {R} 0 0 1 {R} {-0.1*R} Q {0.55*R} {-0.58*R} {0.1*R} {-0.5*R} Q {-0.4*R} {-0.62*R} {-R} {-0.1*R} Z" fill="{hair}"/>')
    # rosto
    for sx in (-1, 1):
        add(f'<ellipse cx="{sx*R*0.58}" cy="{R*0.30}" rx="{R*0.17}" ry="{R*0.11}" fill="#F28B82" opacity=".55"/>')
        add(f'<ellipse cx="{sx*R*0.36}" cy="{R*0.02}" rx="{R*0.085}" ry="{R*0.115}" fill="{INK}"/>')
        add(f'<circle cx="{sx*R*0.36+R*0.03}" cy="{-R*0.03}" r="{R*0.033}" fill="#fff"/>')
        add(f'<path d="M {sx*R*0.36-R*0.12} {-R*0.20} Q {sx*R*0.36} {-R*0.30} {sx*R*0.36+R*0.12} {-R*0.20}" fill="none" stroke="{INK}" stroke-width="{R*0.035}" stroke-linecap="round" opacity=".7"/>')
    if s in (0, 1):                                               # sorriso aberto
        add(f'<path d="M {-R*0.2} {R*0.30} Q 0 {R*0.62} {R*0.2} {R*0.30} Z" fill="{INK}"/>'
            f'<path d="M {-R*0.1} {R*0.48} Q 0 {R*0.40} {R*0.1} {R*0.48} Q 0 {R*0.55} {-R*0.1} {R*0.48} Z" fill="#F28B82"/>')
    else:
        add(f'<path d="M {-R*0.2} {R*0.30} Q 0 {R*0.5} {R*0.2} {R*0.30}" fill="none" stroke="{INK}" stroke-width="{R*0.045}" stroke-linecap="round"/>')
    add(f'<ellipse cx="0" cy="{R*0.16}" rx="{R*0.04}" ry="{R*0.03}" fill="{shade(skin,.8)}"/>')
    # chapéus
    if s == 1:
        kh = "#C9A262"
        add(f'<ellipse cx="0" cy="{-0.60*R}" rx="{1.45*R}" ry="{0.26*R}" fill="{shade(kh,.92)}"/>'
            f'<path d="M {-0.78*R} {-0.64*R} C {-0.84*R} {-1.4*R} {0.84*R} {-1.4*R} {0.78*R} {-0.64*R} Z" fill="{kh}"/>'
            f'<path d="M {-0.79*R} {-0.74*R} Q 0 {-0.58*R} {0.79*R} {-0.74*R} L {0.77*R} {-0.9*R} Q 0 {-0.74*R} {-0.77*R} {-0.9*R} Z" fill="{scarf}"/>'
            f'<ellipse cx="0" cy="{-0.60*R}" rx="{1.45*R}" ry="{0.26*R}" fill="none" stroke="{shade(kh,.8)}" stroke-width="3"/>')
    if s == 2:
        nv = "#2D4C8C"
        add(f'<path d="M {-1.0*R} {-0.34*R} C {-1.02*R} {-1.25*R} {1.02*R} {-1.25*R} {1.0*R} {-0.34*R} Z" fill="{nv}"/>'
            f'<ellipse cx="0" cy="{-0.34*R}" rx="{1.08*R}" ry="{0.2*R}" fill="{shade(nv,.85)}"/>'
            f'<circle cx="0" cy="{-1.02*R}" r="{0.07*R}" fill="{shade(nv,.8)}"/>'
            f'<path d="M {-0.5*R} {-0.8*R} Q 0 {-1.0*R} {0.5*R} {-0.8*R}" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width="{0.05*R}" stroke-linecap="round"/>')
    if s == 3:
        nv = "#2B3F66"
        add(f'<g transform="rotate(-9)"><ellipse cx="{0.08*R}" cy="{-0.78*R}" rx="{1.18*R}" ry="{0.50*R}" fill="{nv}"/>'
            f'<ellipse cx="{0.08*R}" cy="{-0.62*R}" rx="{1.12*R}" ry="{0.24*R}" fill="{shade(nv,.8)}"/>'
            f'<circle cx="{0.1*R}" cy="{-1.28*R}" r="{0.07*R}" fill="{nv}"/></g>')
    add('</g>')
    top = hy - 1.9 * R
    h = -top + 24
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-230 {top:.0f} 460 {h:.0f}">{"".join(o)}</svg>'


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for n in SEC:
        (OUT / f"{n}.svg").write_text(kid(n), encoding="utf-8")
        print(OUT / f"{n}.svg")
