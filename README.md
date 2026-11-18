# Instagram 994 · Publicações

Gerador de publicações (imagens 1080×1350, formato padrão de post) para o Agrupamento de Escuteiros 994 – Caxinas.
Cada **série** (Dicionário Escutista, …) tem o seu modelo visual; cada **parte** é um ficheiro JSON com o conteúdo.
O Chromium desenha os slides a partir de HTML/CSS, por isso o design é fácil de editar.

## Instalar
```bash
pip install -r requirements.txt
playwright install chromium
```

## Gerar
```bash
python src/gerar.py series/dicionario_escutista/partes/parte_01.json
python src/gerar.py series/dicionario_escutista/partes/parte_01.json --slide 3   # só um slide (mais rápido para afinar)
```
Resultado em `output/dicionario_escutista/parte_01/`: `01.png … 08.png`, `folha.png` (vista geral para rever) e `legenda.txt`.

## Fotos
Coloca as fotos em `series/<serie>/fotos/` com os nomes indicados no JSON (`"foto": "lenco.jpg"`).
Se faltar uma foto, o slide usa um fundo verde padrão e o gerador avisa. As fotos **não vão para o git** de propósito: o repositório é público e há crianças nas imagens (ver `.gitignore`).

## Criar a Parte 2 do Dicionário
1. Copia `series/dicionario_escutista/partes/parte_01.json` para `parte_02.json`.
2. Muda os termos. Tipos de slide: `capa`, `termo` (`termo` = 1 ou 2 linhas; a última leva a faixa verde) e `cta`.
3. No `texto`: `\n` = nova linha; `[Lobitos](amarelo)` = palavra colorida; `[Bando](amarelo,sub)` = sublinhado colorido
   (cores: `amarelo`, `verde`, `azul`, `vermelho`).
4. `python src/gerar.py series/dicionario_escutista/partes/parte_02.json`

## Criar uma série nova
Copia a pasta `series/dicionario_escutista/` para `series/<nova_serie>/` e edita:
- `serie.json` — nome, cabeçalho, rodapé, cores, logótipo, hashtags;
- `estilo.css` e `modelo.html.j2` — o aspeto (cada slide é uma página HTML 1080×1350);
- `partes/` — os conteúdos.

## Série «As Nossas Secções» (`series/nossas_seccoes/`), 4 publicações
As quatro publicações usam o mesmo sistema visual «Caderneta de campo 994»: papel creme,
verde estrutural, tipografia condensada, fotografia tratada de forma consistente e uma cor
de acento. A identidade de cada secção vem do conteúdo, dos grupos e da cor de destaque,
não de um modelo gráfico isolado.

- 4 slides por publicação: capa (nome, idade, lema) · o que fazem · como se organizam · lema e contactos.
- As partes usam `modelos/unificado.html.j2` e `modelos/unificado.css`.
- Capa e slide final usam exactamente o mesmo modelo editorial em todas as secções: fotografia ampla,
  cartão creme à esquerda, emblema da secção no cartão e logo do agrupamento no canto inferior direito.
  Muda apenas a cor, a fotografia e o texto.
- As unidades e patronos seguem a página oficial do agrupamento em `994caxinas.com/agrupamento`.
- **Fotos:** cada parte declara a sua pasta em `"pasta_fotos"`:
  `series/nossas_seccoes/fotos/lobitos/`, `exploradores/`, `pioneiros/` ou `caminheiros/`.
  A capa e o slide final usam `"foto"`; `"foto_fundo"` é opcional nos slides 2 e 3 e recebe
  automaticamente um véu da cor da secção, com baixa nitidez. `"foto_pos"` e `"foto_fundo_pos"`
  ajustam o enquadramento. Fora do git (há crianças).

## Fontes
- Palavras: **Chewy** · Descrições: **Roboto Condensed** (ambas livres, em `assets/fonts/`).
- Título da série («Dicionário Escutista», capa, «Faltou alguma?»): **Handelson Four**. Não é distribuível aqui, por isso, por agora,
  usa-se a Londrina Solid como substituta. Para usar a original, copia o ficheiro (`.otf`/`.ttf`/`.woff2`) para `assets/fonts/`
  com «Handelson» no nome (ex.: `HandelsonFour.otf`) — é detetado automaticamente. Confirma que a licença permite o uso.
- `"foto_pos": "50% 72%"` num slide ajusta o enquadramento da foto (horizontal vertical).
- `"foto_zoom": 115` amplia a foto 15% antes do corte. Use `foto_zoom: 100` para manter o
  tamanho normal. `"foto_pos"` controla a parte da imagem que permanece visível:
  `50% 50%` centra, `50% 30%` mantém mais a parte superior e `70% 50%` mantém mais o lado direito.

## Notas
- O logótipo (`assets/logo-994.png`, 172×242 px) vai sem fundo; `"altura"` e `"fundo_claro"` (disco claro opcional) em `serie.json`.
  Um PNG maior ou SVG melhora a nitidez.

## Série «Rótulo 994» (`series/rotulo_994/`)
Foto a ecrã inteiro, só com vinheta no topo e no fundo, e um **rótulo de garantia** («ALTO TEOR EM / MONTAR TENDAS…») que se posiciona
por slide com `"x"` e `"y"` (percentagem, centro do rótulo; por omissão 50 / 68). Campos do slide: `foto`, `foto_pos`, `texto`
(`|` separa linhas), `etiqueta_topo`, `cor` (faixa de baixo), `rot` (inclinação) e `legenda`.
`python src/gerar.py series/rotulo_994/partes/parte_01.json` · Fotos em `series/rotulo_994/fotos/` (fora do git).
