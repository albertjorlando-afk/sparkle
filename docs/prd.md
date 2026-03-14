# PRD

## Product

Sparkle is a solo research tool for building inspectable claims with provenance.

## Problem

Current notes workflows make it easy to collect fragments and hard to answer:

- what supports a claim
- what weakens a claim
- what alternative paths were explored
- why a path was abandoned or harvested
- how a final output traces back to evidence

## Product goal

Help a solo researcher build a claim graph where evidence, objections, questions, decisions, and syntheses remain reusable and traceable.

## User

A solo researcher, builder, or writer exploring an idea with branching lines of inquiry.

## Core principles

- Claims are the center of the workflow.
- Provenance is a first-class feature, not an afterthought.
- Abandoned work is preserved as context, not discarded as noise.
- The graph supports thinking; exported narratives support communication.

## MVP requirements

### Functional

- Create typed nodes: `claim`, `evidence`, `question`, `objection`, `inference`, `decision`, `synthesis`.
- Store nodes with stable content-derived IDs.
- Add typed edges between nodes.
- View a node together with inbound and outbound links.
- Trace ancestry or lineage from a chosen node.
- Mark node status with values like `active`, `stalled`, `promising`, `abandoned`, `harvested`.
- Export a selected subgraph into a markdown narrative.
- Bootstrap a starter graph from the original concept conversation.

### Non-functional

- Local-first.
- Human-readable storage.
- Small enough to inspect manually.
- No heavy dependencies.

## Success criteria for MVP

- A new user can initialize the store and add a claim in under a minute.
- A user can attach supporting and opposing nodes without editing raw JSON.
- A user can inspect where a synthesis came from.
- A user can export a research path into markdown.

## Out of scope for MVP

- graphical interface
- team collaboration
- real-time sync
- web app
- automated paper ingestion
- ranking, search, or recommendation systems
