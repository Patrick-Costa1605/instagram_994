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
COR_TXT = re.compile(r"\[([^\]]+)\]\((amarelo|verde|azul|vermelho|seccao)(,sub)?\)")


def markup(texto: str) -> str:
    """Escapa o HTML e aplica [palavra](cor) = texto colorido, [palavra](cor,sub) = sublinhado colorido."""
    t = html.escape(texto)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)          # **negrito**
    t = COR_TXT.sub(lambda m: f'<span class="{"s" if m.group(3) else "c"}-{m.group(2)}">{m.group(1)}</span>', t)
    return t.replace("\n", "<br>")


# ---------------------------------------------------------------- cor por parte (opcional)
def _rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _lum(rgb):
    def f(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (f(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _contraste(a, b):
    la, lb = sorted((_lum(a), _lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def cores_da_parte(serie: dict, parte: dict):
    """Devolve (cores, pontos, veu) para esta parte.

    Sem `cor_seccao`/`cor_banda`/`cores` no JSON da parte, as cores da série ficam exatamente como estão
    (retrocompatível com o Dicionário Escutista). Com elas:
      cor_seccao  = amarelo | verde | azul | vermelho  -> faixa (--banda) e destaque (--acento)
      cor_banda   = "#RRGGBB"                          -> faixa personalizada
      --texto-banda é escolhido automaticamente (escuro ou creme) pelo melhor contraste.
      veu_tinto   = 0..1 (opcional) intensidade da cor da secção no véu das fotos; sobrepõe o valor da série.
    """
    cores = dict(serie["cores"])
    cores.update(parte.get("cores", {}))
    nome = parte.get("cor_seccao")
    if nome:
        if nome not in cores:
            raise SystemExit(f"cor_seccao «{nome}» desconhecida. Usa: amarelo, verde, azul ou vermelho.")
        cores["banda"] = cores.get("banda_" + nome, cores[nome])
        cores["acento"] = cores.get("acento_" + nome, cores[nome])
    if parte.get("cor_banda"):
        cores["banda"] = parte["cor_banda"]
        cores.setdefault("acento", parte["cor_banda"])
    cores.setdefault("acento", cores["banda"])
    banda, escuro, creme = _rgb(cores["banda"]), _rgb(cores.get("texto_escuro", "#1b1b1b")), _rgb(cores["creme"])
    cores["texto_banda"] = cores.get("texto_escuro", "#1b1b1b") if _contraste(banda, escuro) > _contraste(banda, creme) else cores["creme"]

    # pontos de navegação (uma bolinha por secção, a atual destacada)
    pontos = []
    for sec in serie.get("seccoes", []):
        pontos.append({"nome": sec["nome"], "cor": cores.get("banda_" + sec["id"], cores[sec["id"]]),
                       "ativo": sec["id"] == nome})
    # véu da foto: verde-escuro por defeito; tingido com a cor da secção se `veu_tinto` > 0 na série
    base = (6, 38, 34)
    t = float(parte.get("veu_tinto", serie.get("veu_tinto", 0.0))) if (nome or parte.get("cor_banda")) else 0.0
    alvo = tuple(c * 0.35 for c in banda)
    veu = tuple(round(b + (a - b) * t) for b, a in zip(base, alvo))
    return cores, pontos, veu


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
    # fonte da série (ex.: Handelson Four): se existir um ficheiro assets/fonts/*andelson*, é usado; senão há fallback
    hf = next(iter(sorted((ROOT / "assets" / "fonts").glob("*andelson*"))), None)
    cores, pontos, veu = cores_da_parte(serie, parte)
    css = env.from_string((serie_dir / serie["estilo"]).read_text(encoding="utf-8")).render(
        fonts=fonts, w=fmt["largura"], h=fmt["altura"], handelson=hf.as_uri() if hf else None,
        cores=cores, veu=",".join(map(str, veu)))
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
        css=css, s=s, foto=foto, foto_pos=s.get("foto_pos", "50% 50%"), cores=cores, pontos=pontos, parte=parte, cabecalho=serie.get("cabecalho", []),
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
