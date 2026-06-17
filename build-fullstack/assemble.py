"""Full-Stack Developer Map — assembler.

Merges the taxonomy skeleton (domains + subdomains) with the per-domain
topic/edge files in build-fullstack/domains/*.json and the cross-domain bridge
edges in build-fullstack/cross_edges.json, then injects the resulting graph into
a clone of the AI/ML knowledge-map renderer to produce
fullstack-developer-map.html.

The renderer (HTML/CSS/JS) is reused verbatim from ai-knowledge-map.html — only
the embedded data, the page title, the subline, the help text, the localStorage
key and the two header cross-links are swapped, so all three maps look and behave
identically but keep separate progress.

Usage:  python3 build-fullstack/assemble.py
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DOMAINS_DIR = os.path.join(HERE, "domains")
TEMPLATE = os.path.join(ROOT, "ai-knowledge-map.html")
OUTPUT = os.path.join(ROOT, "fullstack-developer-map.html")
CROSS_EDGES = os.path.join(HERE, "cross_edges.json")

PAGE_TITLE = "The Full-Stack Developer Map"
FAM_KEY_NEW = "fsmap-familiarity-v1"
SUBLINE_NEW = "the working developer's whole stack"
HELP_PARAGRAPH = (
    "<p>This is a focused, practical map of the <b>full-stack web developer</b> "
    "role — from how the web works, through HTML/CSS/JS and frontend frameworks, "
    "the backend, APIs, auth &amp; security, databases, testing, DevOps &amp; "
    "deployment, architecture and performance, down to the CS foundations and "
    "collaboration skills you lean on daily. It is a <b>hybrid</b> view: durable "
    "concepts as the backbone, with the concrete tools you'd actually reach for "
    "(React, Node, PostgreSQL, Docker, …) named throughout. The goal is to see "
    "the <b>whole stack at once</b> and mark <b>what you know vs. what you "
    "don't.</b> For the tool-agnostic theory underneath, see the sibling "
    "<b>Software Engineering</b> map; for the ML side, the <b>AI / ML</b> map.</p>"
)

# Anchors that exist verbatim in ai-knowledge-map.html.
OLD_TITLE = "The AI / ML Knowledge Map"
OLD_FAM_KEY = "const FAM_KEY = 'aimap-familiarity-v1';"
NEW_FAM_KEY = "const FAM_KEY = 'fsmap-familiarity-v1';"
OLD_HELP_PARAGRAPH = (
    "<p>This is a big-picture atlas of artificial intelligence — from the "
    "mathematics and statistics underneath, through classical ML, deep learning, "
    "vision, NLP, reinforcement learning, generative models, the systems that "
    "ship them, and the responsible-AI layer around them. The goal is to let you "
    "see the <b>whole territory at once</b> and mark <b>what you know vs. what "
    "you don't.</b></p>"
)
DATA_OPEN = '<script id="aimap-data" type="application/json">'
DATA_CLOSE = "</script>"

# On the AI template, xmap1 -> SWE map and xmap2 -> Full-Stack map. On the
# generated Full-Stack page we leave the Software-Engineering link (xmap1) in
# place and flip the self-link (xmap2) to point at the AI map.
OLD_XLINK_HREF = 'href="fullstack-developer-map.html"'
NEW_XLINK_HREF = 'href="ai-knowledge-map.html"'
OLD_XLINK_TEXT = ">⇄ Full-Stack Developer</a>"
NEW_XLINK_TEXT = ">⇄ AI / ML Knowledge</a>"
OLD_SUBLINE = ">map your terra incognita</span>"
NEW_SUBLINE = ">" + SUBLINE_NEW + "</span>"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_graph():
    skel = load_json(os.path.join(HERE, "skeleton.json"))
    domains = skel["domains"]
    color_of = {d["key"]: d["color"] for d in domains}
    dom_order = [d["key"] for d in domains]

    # subdomain label lookup, and order, per domain
    sub_label = {}
    subs_by_dom = {k: [] for k in dom_order}
    for s in skel["subdomains"]:
        sub_label[(s["domain"], s["key"])] = s["label"]
        subs_by_dom[s["domain"]].append(s["key"])

    nodes = []
    topic_ids = set()
    topic_domain = {}

    # 1) domain nodes
    for d in domains:
        nodes.append({
            "id": "dom:" + d["key"], "label": d["title"], "kind": "domain",
            "domain": d["key"], "subdomain": None, "parent": None,
            "importance": 3, "color": d["color"], "desc": d.get("scope", ""),
        })
    # 2) subdomain nodes
    for k in dom_order:
        for subk in subs_by_dom[k]:
            nodes.append({
                "id": "sub:%s:%s" % (k, subk),
                "label": sub_label[(k, subk)], "kind": "subdomain",
                "domain": k, "subdomain": subk, "parent": "dom:" + k,
                "importance": 2, "color": color_of[k], "desc": "",
            })
    # 3) topic nodes + intra-domain edges
    intra_edges = []
    for k in dom_order:
        dom = load_json(os.path.join(DOMAINS_DIR, "%s.json" % k))
        valid_subs = set(subs_by_dom[k])
        for t in dom["topics"]:
            if t["subdomain"] not in valid_subs:
                raise SystemExit("%s: topic %s references unknown subdomain %r"
                                 % (k, t["id"], t["subdomain"]))
            if t["id"] in topic_ids:
                raise SystemExit("duplicate topic id: %s" % t["id"])
            topic_ids.add(t["id"])
            topic_domain[t["id"]] = k
            nodes.append({
                "id": t["id"], "label": t["label"], "kind": "topic",
                "domain": k, "subdomain": t["subdomain"],
                "parent": "sub:%s:%s" % (k, t["subdomain"]),
                "importance": t.get("importance", 2), "color": color_of[k],
                "desc": t.get("desc", ""),
            })
        for e in dom["edges"]:
            intra_edges.append((e["source"], e["target"], e["type"]))

    # 4) cross-domain bridge edges (optional)
    cross_raw = []
    if os.path.exists(CROSS_EDGES):
        cross_raw = load_json(CROSS_EDGES)

    # 5) merge + validate + dedupe edges
    edges, dropped, dups = [], [], 0
    seen = set()

    def add_edge(s, t, ty, where):
        nonlocal dups
        if s == t:
            dropped.append((s, t, ty, where, "self-loop")); return
        if s not in topic_ids or t not in topic_ids:
            dropped.append((s, t, ty, where, "missing-endpoint")); return
        if ty not in ("related", "prereq"):
            dropped.append((s, t, ty, where, "bad-type")); return
        # related is undirected -> canonicalise so a-b == b-a; prereq is directed
        key = (ty, tuple(sorted((s, t)))) if ty == "related" else (ty, s, t)
        if key in seen:
            dups += 1; return
        seen.add(key)
        edges.append({"source": s, "target": t, "type": ty})

    for s, t, ty in intra_edges:
        add_edge(s, t, ty, "intra")
    cross_kept_before = len(edges)
    for e in cross_raw:
        add_edge(e["source"], e["target"], e.get("type", "related"), "cross")
    cross_kept = len(edges) - cross_kept_before

    n_dom = sum(1 for n in nodes if n["kind"] == "domain")
    n_sub = sum(1 for n in nodes if n["kind"] == "subdomain")
    n_top = sum(1 for n in nodes if n["kind"] == "topic")
    cross_total = sum(1 for e in edges
                      if topic_domain[e["source"]] != topic_domain[e["target"]])

    data = {
        "meta": {"domains": n_dom, "subdomains": n_sub,
                 "topics": n_top, "edges": len(edges)},
        "domains": [{"key": d["key"], "title": d["title"],
                     "color": d["color"], "scope": d.get("scope", "")}
                    for d in domains],
        "nodes": nodes,
        "edges": edges,
    }
    stats = {"dropped": dropped, "dups": dups, "cross_in": len(cross_raw),
             "cross_kept": cross_kept, "cross_total": cross_total}
    return data, stats


def inject(template_text, data):
    json_text = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    # Safe to embed inside <script>: only </script> could terminate early.
    json_text = json_text.replace("</", "<\\/")

    # --- swap the data block ---
    i0 = template_text.index(DATA_OPEN) + len(DATA_OPEN)
    i1 = template_text.index(DATA_CLOSE, i0)
    out = template_text[:i0] + "\n" + json_text + "\n" + template_text[i1:]

    # --- swap title (appears in <title> and <h1>) ---
    n_title = out.count(OLD_TITLE)
    out = out.replace(OLD_TITLE, PAGE_TITLE)

    # --- swap localStorage key so progress is independent of the other maps ---
    if OLD_FAM_KEY not in out:
        raise SystemExit("FAM_KEY anchor not found in template")
    out = out.replace(OLD_FAM_KEY, NEW_FAM_KEY)

    # --- swap the help intro paragraph ---
    if OLD_HELP_PARAGRAPH not in out:
        raise SystemExit("help paragraph anchor not found in template")
    out = out.replace(OLD_HELP_PARAGRAPH, HELP_PARAGRAPH)

    # --- flip the self cross-link (xmap2) to point at the AI map ---
    if OLD_XLINK_HREF not in out or OLD_XLINK_TEXT not in out:
        raise SystemExit("header cross-link anchor not found in template")
    out = out.replace(OLD_XLINK_HREF, NEW_XLINK_HREF)
    out = out.replace(OLD_XLINK_TEXT, NEW_XLINK_TEXT)

    # --- swap the header subline ---
    if OLD_SUBLINE not in out:
        raise SystemExit("subline anchor not found in template")
    out = out.replace(OLD_SUBLINE, NEW_SUBLINE)

    return out, n_title


def main():
    data, stats = build_graph()
    with open(TEMPLATE, "r", encoding="utf-8") as f:
        template_text = f.read()
    out, n_title = inject(template_text, data)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(out)

    m = data["meta"]
    print("Assembled %s" % os.path.relpath(OUTPUT, ROOT))
    print("  domains=%d subdomains=%d topics=%d edges=%d"
          % (m["domains"], m["subdomains"], m["topics"], m["edges"]))
    print("  cross-domain edges: %d total (%d supplied, %d kept after validate/dedupe)"
          % (stats["cross_total"], stats["cross_in"], stats["cross_kept"]))
    print("  deduped: %d  dropped: %d  title-replacements: %d"
          % (stats["dups"], len(stats["dropped"]), n_title))
    if stats["dropped"]:
        print("  --- dropped edges ---")
        for s, t, ty, where, why in stats["dropped"][:30]:
            print("    [%s/%s] %s -> %s (%s)" % (where, why, s, t, ty))
        if len(stats["dropped"]) > 30:
            print("    ... and %d more" % (len(stats["dropped"]) - 30))


if __name__ == "__main__":
    main()
