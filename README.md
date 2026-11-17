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

## Série «As Nossas Secções» (`series/nossas_seccoes/`), 4 publicações com design próprio
Cada secção tem um design diferente, com fontes e linguagem visual próprias. Em comum (a âncora do 994): a etiqueta
«As Nossas Secções · I/II/III/IV» em cima à esquerda e o logótipo em baixo à direita.

| Parte | Conceito | Fontes |
|---|---|---|
| `1_lobitos.json` | Livro de histórias em papel recortado (folhas da Selva, sol com a idade, autocolantes) | Baloo 2 + Nunito |
| `2_exploradores.json` | Mapa de expedição (curvas de nível, coordenadas, trilho, carimbo, etiquetadora) | Saira Stencil One + Special Elite |
| `3_pioneiros.json` | Planta técnica de um Empreendimento (blueprint, cotas, legenda técnica, organigrama) | Space Grotesk + Space Mono |
| `4_caminheiros.json` | Revista editorial (capa com duotone vermelho, citação, serifa) | Fraunces + Inter |

- 4 slides por publicação: capa (nome, idade, lema) · o que fazem · como se organizam · lema e contactos.
- Cada parte indica o seu `"modelo"` e `"estilo"` (em `modelos/`), por isso os designs são independentes.
- Fontes dos factos: 994caxinas.com (bandos, patrulhas, equipas, tribos, lemas) e escutismo.pt (organização e atividades de cada secção).
- **Fotos:** `series/nossas_seccoes/fotos/<secção>/capa.jpg`, `atividade.jpg`, `final.jpg`. As atuais são provisórias;
  basta substituí-las com o mesmo nome (o enquadramento ajusta-se com `"foto_pos"` no JSON). Fora do git (há crianças).

## Fontes
- Palavras: **Chewy** · Descrições: **Roboto Condensed** (ambas livres, em `assets/fonts/`).
- Título da série («Dicionário Escutista», capa, «Faltou alguma?»): **Handelson Four**. Não é distribuível aqui, por isso, por agora,
  usa-se a Londrina Solid como substituta. Para usar a original, copia o ficheiro (`.otf`/`.ttf`/`.woff2`) para `assets/fonts/`
  com «Handelson» no nome (ex.: `HandelsonFour.otf`) — é detetado automaticamente. Confirma que a licença permite o uso.
- `"foto_pos": "50% 72%"` num slide ajusta o enquadramento da foto (horizontal vertical).

## Notas
- O logótipo (`assets/logo-994.png`, 172×242 px) vai sem fundo; `"altura"` e `"fundo_claro"` (disco claro opcional) em `serie.json`.
  Um PNG maior ou SVG melhora a nitidez.

## Série «Rótulo 994» (`series/rotulo_994/`)
Foto a ecrã inteiro, só com vinheta no topo e no fundo, e um **rótulo de garantia** («ALTO TEOR EM / MONTAR TENDAS…») que se posiciona
por slide com `"x"` e `"y"` (percentagem, centro do rótulo; por omissão 50 / 68). Campos do slide: `foto`, `foto_pos`, `texto`
(`|` separa linhas), `etiqueta_topo`, `cor` (faixa de baixo), `rot` (inclinação) e `legenda`.
`python src/gerar.py series/rotulo_994/partes/parte_01.json` · Fotos em `series/rotulo_994/fotos/` (fora do git).
