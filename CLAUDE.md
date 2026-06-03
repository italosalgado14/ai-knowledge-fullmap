# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project state

Greenfield. The repository currently contains only `Instructions.md` — no code, build system, tests, dependencies, or VCS history exist yet. Any commands, tooling, or architecture are decisions to be made, not discovered. Update this file once a stack is chosen.

## What this project is

The deliverable (see `Instructions.md`) is a **single, very large visual diagram** mapping the entire landscape of AI knowledge and the relationships between topics. The intended audience is one expert user (background in software, computer vision, and mathematics) who wants a "what I know vs. what I don't know" map — so breadth and the connections between subfields matter more than depth on any one node.

Required topic coverage, per the instructions:
- Statistical view: causal inference, Bayesian statistics
- Foundational knowledge, classical ML, deep learning, and applied/practical vision
- Supporting mathematics (algebra and whatever else the structure requires)
- Software engineering knowledge
- Optimization knowledge

## Working constraints from the instructions

- **Do not skimp on size.** The user explicitly wants a large, comprehensive diagram with many nodes — err toward more topics and more detail, not a tidy summary.
- **Show relationships, not just a list.** The value is in how subfields connect, prerequisite chains, and overlaps — model the edges deliberately.
- **Presentation format is open.** An HTML page is the suggested default, but choosing a better-suited approach (e.g. an interactive graph) is encouraged. Favor something self-contained and easy to open in a browser.
- Support the "known vs. unknown" goal — the visualization should make it natural to mark or distinguish familiarity per topic.

## Guidance for picking an approach

Because nothing is committed yet, prefer a low-friction, dependency-light deliverable the user can open directly (a single HTML file, ideally self-contained). If an interactive graph library is needed for the scale, keep the data (the topic/edge model) separated from the rendering so the knowledge map can grow without rewrites.
