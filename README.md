# Knowledge Fullmap Pages

Big, interactive "what I know vs. what I don't" maps. Each is a single
self-contained HTML file: a radial graph (domain → subdomain → topic) with
prerequisite/related links, search, an outline view, and per-topic familiarity
marking saved in your browser.

- **AI / ML Knowledge Map** — https://italosalgado14.github.io/ai-knowledge-fullmap/
- **Software Engineering Knowledge Map** — https://italosalgado14.github.io/ai-knowledge-fullmap/software-engineering-map.html
- **Full-Stack Developer Map** — https://italosalgado14.github.io/ai-knowledge-fullmap/fullstack-developer-map.html

The three maps form a family and cross-link from their headers (⇄):

- **Software Engineering** is the **abstract, tool-agnostic foundation** — the
  durable concepts (languages, DSA, systems, networks, data, architecture,
  practice) that sit *beneath* every specialization.
- **AI / ML** and **Full-Stack Developer** are **focused specializations** on
  top of it. The Full-Stack map is a *hybrid* view: concept nodes as the
  backbone, with the concrete tools you'd actually use (React, Node, PostgreSQL,
  Docker, …) named in the descriptions.

Familiarity progress is stored per map (separate `localStorage` keys —
`aimap-`, `swemap-`, `fsmap-`), so marking one never affects the others.

## Architecture

All three pages share one renderer: `ai-knowledge-map.html` is both the live
AI/ML map **and** the template. Each generated map is a clone of it with only
the embedded data, page title, subline, help text, `localStorage` key, and the
two header cross-links swapped — so the maps look and behave identically but
keep independent state.

Each map is generated from data so the knowledge model can grow without touching
the renderer:

```
build/                    # Software Engineering map (16 domains)
  skeleton_def.py         #   domains × subdomains taxonomy -> skeleton.json
  skeleton.json
  domains/*.json          #   per-domain topics + intra-domain edges
  merge_cross.py          #   cross-domain "bridge" edges -> cross_edges.json
  cross_edges.json
  assemble.py             #   merges everything -> software-engineering-map.html

build-fullstack/          # Full-Stack Developer map (14 domains)
  skeleton_def.py         #   domains × subdomains taxonomy -> skeleton.json
  skeleton.json
  domains/*.json          #   per-domain topics + intra-domain edges
  cross_edges.json        #   cross-domain "bridge" edges
  assemble.py             #   merges everything -> fullstack-developer-map.html
```

## Regenerating

Software Engineering map:

```sh
python3 build/skeleton_def.py   # only if you change the taxonomy
python3 build/merge_cross.py    # only if you change cross-domain edges
python3 build/assemble.py       # writes software-engineering-map.html
```

Full-Stack Developer map:

```sh
python3 build-fullstack/skeleton_def.py   # only if you change the taxonomy
python3 build-fullstack/assemble.py       # writes fullstack-developer-map.html
```

`assemble.py` is idempotent and validates the graph as it builds: it drops
self-loops, edges with missing endpoints, and bad edge types, and dedupes
`related` edges (undirected) and `prereq` edges (directed). Editing a
`domains/*.json` file and re-running `assemble.py` is all it takes to grow a map.
