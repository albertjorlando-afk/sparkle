# Sparkle

Sparkle is an early solo research tool built around a claim graph on top of a content-addressed store.

The product idea came from a conversation about using Merkle-DAG-style structure for research: preserve provenance, branch inquiry without losing work, revisit abandoned paths, and export selected lines of thought into a usable artifact.

This repository contains:

- an archived copy of the original concept conversation
- a Python MVP CLI for creating and exploring a claim graph
- a short PRD for the MVP
- a roadmap for what comes next

## Why this exists

Typical notes tools are good at capture and weak at structured inquiry. Sparkle aims to make research paths inspectable:

- claims can point to evidence, questions, objections, decisions, and syntheses
- every node is content-addressed for stable provenance
- branches can be explored, stalled, abandoned, or harvested without deletion
- selected subgraphs can be exported into a linear narrative

Conceptually, Sparkle is a claim graph.

Operationally, Sparkle behaves like a branching inquiry workspace.

Technically, this MVP uses a Merkle-style content hash for immutable research nodes.

## MVP scope

The MVP is a local CLI that supports:

- creating research nodes with typed metadata
- storing nodes by content hash
- linking nodes with typed edges
- inspecting node lineage and neighborhood
- tracking branch-like status on nodes
- exporting a selected subgraph into a simple markdown narrative
- bootstrapping a sample graph from the archived conversation

This is intentionally small. It is a foundation for proving the model, not the full product.

## Project structure

- [`archive/chatgpt-merkle-dag-research.md`](/Users/aorlando/dev/ideas/sparkle/archive/chatgpt-merkle-dag-research.md): archived product-origin conversation
- [`docs/prd.md`](/Users/aorlando/dev/ideas/sparkle/docs/prd.md): compact product requirements document
- [`docs/roadmap.md`](/Users/aorlando/dev/ideas/sparkle/docs/roadmap.md): what the MVP covers and what is next
- [`src/sparkle/cli.py`](/Users/aorlando/dev/ideas/sparkle/src/sparkle/cli.py): command-line entrypoint
- [`src/sparkle/graph.py`](/Users/aorlando/dev/ideas/sparkle/src/sparkle/graph.py): graph store and export logic
- [`src/sparkle/models.py`](/Users/aorlando/dev/ideas/sparkle/src/sparkle/models.py): data model and hashing
- [`src/sparkle/bootstrap.py`](/Users/aorlando/dev/ideas/sparkle/src/sparkle/bootstrap.py): seeds a starter graph from the archived conversation

## Quick start

Use Python 3.11+.

```bash
python3 -m src.sparkle.cli init
python3 -m src.sparkle.cli bootstrap
python3 -m src.sparkle.cli list-nodes
python3 -m src.sparkle.cli show <node_id_prefix>
python3 -m src.sparkle.cli export --root <node_id_prefix>
```

By default, the CLI stores data in `.sparkle/graph.json`.

## Example workflow

1. Initialize the local store.
2. Bootstrap the example graph, or start with your own claim.
3. Add evidence, objections, questions, and syntheses as separate nodes.
4. Link them with typed relations like `supports`, `contradicts`, `answers`, or `derived_from`.
5. Export a subgraph into markdown when you want a memo-like output.

## Example commands

Create a claim:

```bash
python3 -m src.sparkle.cli add-node \
  --type claim \
  --title "Merkle DAG structure can improve research provenance" \
  --content "A claim-graph research tool can preserve distinct inquiry paths and make final outputs traceable."
```

Create evidence:

```bash
python3 -m src.sparkle.cli add-node \
  --type evidence \
  --title "Origin conversation" \
  --content "The original concept conversation argues for provenance, branching without loss, and selective extraction." \
  --citations archive/chatgpt-merkle-dag-research.md
```

Link the evidence to the claim:

```bash
python3 -m src.sparkle.cli add-edge \
  --from <evidence_id_prefix> \
  --to <claim_id_prefix> \
  --relation supports
```

Export a narrative:

```bash
python3 -m src.sparkle.cli export \
  --root <claim_id_prefix> \
  --output exports/merkle-dag-claim.md
```

## Design notes

This MVP keeps two ideas separate:

- immutable node content and links
- editable working interpretation through metadata like status and confidence

That separation matters because the tool is meant to preserve provenance without forcing every draft action to become permanent reasoning history.

## Current limitations

- no UI yet
- no multi-user collaboration
- no automatic source ingestion
- no merge conflict handling between competing syntheses
- no search or ranking beyond simple graph traversal

Those are deliberate omissions for the first cut.
