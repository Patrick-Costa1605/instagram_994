#!/usr/bin/env python3
"""Gerador de publicações para o Instagram do 994-Caxinas.

Cada *série* (pasta em series/) tem o seu modelo HTML/CSS e as suas «partes» (JSON).
O Chromium (Playwright) desenha cada slide e exporta PNG 1080×1350.

Uso:
    python src/gerar.py series/dicionario_escutista/partes/parte_01.json
    python src/gerar.py series/dicionario_escutista/partes/parte_01.json --slide 3     # só o slide 3
Saída: output/<serie>/<parte>/01.png … + folha.png (pré-visualização) + legenda.txt
"""
import argparse
import html
import json
import re
import sys
from pathlib import Path

from jinja2 import Environment

ROOT = Path(__file__).resolve().parent.parent
COR_TXT = re.compile(r"\[([^\]]+)\]\((amarelo|verde|azul|vermelho)(,sub)?\)")


def markup(texto: str) -> str:
    """Escapa o HTML e aplica [palavra](cor) = texto colorido, [palavra](cor,sub) = sublinhado colorido."""
    t = html.escape(texto)
    t = COR_TXT.sub(lambda m: f'<span class="{"s" if m.group(3) else "c"}-{m.group(2)}">{m.group(1)}</span>', t)
    return t.replace("\n", "<br>")


def launch(p):
    try:
        return p.chromium.launch()
    except Exception:                       # ambientes com o Chromium noutro sítio
        for cand in sorted(Path("/opt/pw-browsers").glob("chromium-*/chrome-linux*/chrome")):
            return p.chromium.launch(executable_path=str(cand))
        raise


def render_html(serie_dir: Path, serie: dict, parte: dict, idx: int, tmp: Path) -> Path:
    s = parte["slides"][idx]
    fmt = serie["formato"]
    fonts = (ROOT / "assets" / "fonts").as_uri()
    env = Environment(autoescape=False)
    css = env.from_string((serie_dir / serie["estilo"]).read_text(encoding="utf-8")).render(
        fonts=fonts, w=fmt["largura"], h=fmt["altura"])
    foto = None
    if s.get("foto"):
        fp = serie_dir / "fotos" / s["foto"]
        if fp.exists():
            foto = fp.as_uri()
        else:
            print(f"  ! slide {idx + 1}: foto «{s['foto']}» não existe em {serie_dir / 'fotos'} — a usar fundo padrão",
                  file=sys.stderr)
    logo_cfg = serie.get("logo")
    logo = (serie_dir / logo_cfg["ficheiro"]).resolve().as_uri() if logo_cfg else None
    page = env.from_string((serie_dir / serie["modelo"]).read_text(encoding="utf-8")).render(
        css=css, s=s, foto=foto, cores=serie["cores"], cabecalho=serie.get("cabecalho", []),
        rodape=serie.get("rodape"), logo=logo, logo_h=(logo_cfg or {}).get("altura", 120),
        logo_fundo=(logo_cfg or {}).get("fundo_claro", False), texto=markup(s.get("texto", "")))
    out = tmp / f"slide_{idx + 1:02d}.html"
    out.write_text(page, encoding="utf-8")
    return out


def folha(pngs, destino: Path, cols=4, thumb=360):
    from PIL import Image
    ims = [Image.open(p).convert("RGB") for p in pngs]
    h = int(thumb * ims[0].height / ims[0].width)
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * thumb + (cols + 1) * 16, rows * h + (rows + 1) * 16), (30, 30, 30))
    for i, im in enumerate(ims):
        sheet.paste(im.resize((thumb, h), Image.LANCZOS), (16 + (i % cols) * (thumb + 16), 16 + (i // cols) * (h + 16)))
    sheet.save(destino)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("parte", help="JSON da parte (ex.: series/dicionario_escutista/partes/parte_01.json)")
    ap.add_argument("--slide", type=int, nargs="+", help="só estes slides (1, 2, 3…)")
    a = ap.parse_args()

    parte_path = Path(a.parte).resolve()
    serie_dir = parte_path.parent.parent
    serie = json.loads((serie_dir / "serie.json").read_text(encoding="utf-8"))
    parte = json.loads(parte_path.read_text(encoding="utf-8"))
    out_dir = ROOT / "output" / serie_dir.name / parte_path.stem
    tmp = out_dir / ".tmp"
    tmp.mkdir(parents=True, exist_ok=True)
    fmt = serie["formato"]
    todos = list(range(len(parte["slides"])))
    idxs = [i - 1 for i in a.slide] if a.slide else todos

    from playwright.sync_api import sync_playwright
    pngs = []
    with sync_playwright() as p:
        browser = launch(p)
        page = browser.new_page(viewport={"width": fmt["largura"], "height": fmt["altura"]}, device_scale_factor=1)
        for i in idxs:
            h = render_html(serie_dir, serie, parte, i, tmp)
            page.goto(h.as_uri())
            page.wait_for_selector("body[data-pronto='1']")
            png = out_dir / f"{i + 1:02d}.png"
            page.screenshot(path=str(png), clip={"x": 0, "y": 0, "width": fmt["largura"], "height": fmt["altura"]})
            pngs.append(png)
            print(f"  {png.relative_to(ROOT)}")
        browser.close()
    for f in tmp.glob("*"):
        f.unlink()
    tmp.rmdir()

    existentes = [out_dir / f"{i + 1:02d}.png" for i in todos if (out_dir / f"{i + 1:02d}.png").exists()]
    if existentes:
        folha(existentes, out_dir / "folha.png")
    legenda = (parte.get("legenda", "").strip() + "\n\n" + serie.get("hashtags", "")).strip()
    (out_dir / "legenda.txt").write_text(legenda + "\n", encoding="utf-8")
    print(f"Pronto: {out_dir.relative_to(ROOT)}/ ({len(pngs)} slide(s), folha.png, legenda.txt)")


if __name__ == "__main__":
    main()
