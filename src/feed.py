"""Feed em puzzle: as capas das publicações encaixam na grelha do perfil (3 colunas) e parecem uma imagem só.

- campo de cor: cada capa tem uma cor no seu centro e as cores vão-se misturando suavemente de uma capa
  para as vizinhas (na horizontal e na vertical);
- dentro de cada carrossel, a cor sai da capa e vai-se juntando à cor própria da publicação.
"""
import numpy as np


def _ss(x):
    x = np.clip(x, 0, 1)
    return x * x * (3 - 2 * x)


def capa(cores, ncols, col, row, W=1080, H=1350):
    """Fundo (H×W×3) da capa na posição (col,row) da grelha. `cores` = lista de RGB por ordem de leitura."""
    n = len(cores)
    nrows = (n + ncols - 1) // ncols
    grid = np.zeros((nrows, ncols, 3), np.float32)
    for k in range(nrows * ncols):
        grid[k // ncols, k % ncols] = cores[min(k, n - 1)]
    u = np.clip((col * W + np.arange(W) + 0.5) / W - 0.5, 0, ncols - 1)
    v = np.clip((row * H + np.arange(H) + 0.5) / H - 0.5, 0, nrows - 1)
    i0 = np.minimum(np.floor(u).astype(int), max(ncols - 2, 0)); i1 = np.minimum(i0 + 1, ncols - 1)
    j0 = np.minimum(np.floor(v).astype(int), max(nrows - 2, 0)); j1 = np.minimum(j0 + 1, nrows - 1)
    fu = _ss(u - i0)[None, :, None].astype(np.float32)
    fv = _ss(v - j0)[:, None, None].astype(np.float32)
    c00, c10 = grid[j0[:, None], i0[None, :]], grid[j0[:, None], i1[None, :]]
    c01, c11 = grid[j1[:, None], i0[None, :]], grid[j1[:, None], i1[None, :]]
    top = c00 * (1 - fu) + c10 * fu
    bot = c01 * (1 - fu) + c11 * fu
    return top * (1 - fv) + bot * fv


def publicacao(cover, own_stops, n, W=1080, mistura=700.0):
    """Fundo (H×n·W×3): capa vinda do feed + resto a ir da cor da borda da capa para o perfil de cores próprio.

    own_stops = [(x, (r,g,b)), ...] (interpolado linearmente)."""
    H = cover.shape[0]
    total = n * W
    out = np.empty((H, total, 3), np.float32)
    out[:, :W] = cover
    xs = np.arange(W, total)
    xp = [p[0] for p in own_stops]
    base = np.stack([np.interp(xs, xp, [p[1][c] for p in own_stops]) for c in range(3)], axis=1).astype(np.float32)
    t = _ss((xs - W) / mistura)[None, :, None].astype(np.float32)
    out[:, W:] = cover[:, -1:, :] * (1 - t) + base[None, :, :] * t
    return out
