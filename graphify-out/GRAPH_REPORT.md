# Graph Report - instagram_994  (2026-11-17)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 40 nodes · 60 edges · 7 communities (2 shown, 5 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 3 edges (avg confidence: 0.85)
- Token cost: 34,534 input · 105 output

## Graph Freshness
- Built from commit: `27c6d3d8`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Panorama Slide Rendering
- Color Contrast Utilities
- Rope Geometry Math
- Rope Drawing and Knots
- Rope SVG Output
- Text Markup Parsing

## God Nodes (most connected - your core abstractions)
1. `corda_svg()` - 8 edges
2. `render_html()` - 7 edges
3. `render_panorama()` - 7 edges
4. `cores_da_parte()` - 6 edges
5. `main()` - 5 edges
6. `_pts()` - 4 edges
7. `_no()` - 4 edges
8. `_rope()` - 4 edges
9. `folha()` - 3 edges
10. `_contraste()` - 3 edges

## Surprising Connections (you probably didn't know these)
- `render_panorama()` --calls--> `corda_svg()`  [EXTRACTED]
  src/gerar.py → src/corda.py

## Import Cycles
- None detected.

## Communities (7 total, 5 thin omitted)

### Community 0 - "Panorama Slide Rendering"
Cohesion: 0.27
Nodes (6): folha(), launch(), main(), render_html(), render_panorama(), foto_fn()

### Community 2 - "Color Contrast Utilities"
Cohesion: 0.29
Nodes (4): _contraste(), cores_da_parte(), _lum(), _rgb()

## Knowledge Gaps
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `corda_svg()` connect `Rope SVG Output` to `Panorama Slide Rendering`, `Post Generator CLI`, `Rope Geometry Math`, `Rope Drawing and Knots`?**
  _High betweenness centrality (0.336) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `render_panorama()` (e.g. with `ag()` and `foto_fn()`) actually correct?**
  _`render_panorama()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Why does `render_panorama()` connect `Panorama Slide Rendering` to `Post Generator CLI`, `Rope SVG Output`?**
  _High betweenness centrality (0.156) - this node is a cross-community bridge._
- **Why does `cores_da_parte()` connect `Color Contrast Utilities` to `Panorama Slide Rendering`, `Post Generator CLI`?**
  _High betweenness centrality (0.106) - this node is a cross-community bridge._