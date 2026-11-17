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

## Fontes
- Palavras: **Chewy** · Descrições: **Roboto Condensed** (ambas livres, em `assets/fonts/`).
- Título da série («Dicionário Escutista», capa, «Faltou alguma?»): **Handelson Four**. Não é distribuível aqui, por isso, por agora,
  usa-se a Londrina Solid como substituta. Para usar a original, copia o ficheiro (`.otf`/`.ttf`/`.woff2`) para `assets/fonts/`
  com «Handelson» no nome (ex.: `HandelsonFour.otf`) — é detetado automaticamente. Confirma que a licença permite o uso.
- `"foto_pos": "50% 72%"` num slide ajusta o enquadramento da foto (horizontal vertical).

## Notas
- O logótipo (`assets/logo-994.png`, 172×242 px) vai sem fundo; `"altura"` e `"fundo_claro"` (disco claro opcional) em `serie.json`.
  Um PNG maior ou SVG melhora a nitidez.
