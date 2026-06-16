# Knowledge Fullmap Pages

Big, interactive "what I know vs. what I don't" maps. Each is a single
self-contained HTML file: a radial graph (domain → subdomain → topic) with
prerequisite/related links, search, an outline view, and per-topic familiarity
marking saved in your browser.

- **AI / ML Knowledge Map** — https://italosalgado14.github.io/ai-knowledge-fullmap/
- **Software Engineering Knowledge Map** — https://italosalgado14.github.io/ai-knowledge-fullmap/software-engineering-map.html

The two maps cross-link from their headers (⇄). Familiarity progress is stored
per map (separate `localStorage` keys), so marking one never affects the other.

## Building the Software Engineering map

The SWE map is generated from data so the knowledge model can grow without
touching the renderer:

```
build/
  skeleton_def.py      # 16 domains × 8 subdomains taxonomy -> skeleton.json
  skeleton.json
  domains/*.json        # per-domain topics + intra-domain edges
  merge_cross.py        # cross-domain "bridge" edges -> cross_edges.json
  cross_edges.json
  assemble.py           # merges everything into software-engineering-map.html
```

Regenerate with:

```sh
python3 build/skeleton_def.py   # only if you change the taxonomy
python3 build/merge_cross.py    # only if you change cross-domain edges
python3 build/assemble.py       # writes software-engineering-map.html
```

`assemble.py` clones `ai-knowledge-map.html` (the renderer) and swaps in the new
data, title, help text and storage key — so both maps stay visually identical.
