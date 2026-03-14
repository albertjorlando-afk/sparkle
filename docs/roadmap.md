# Roadmap

## Completed

- Local Python CLI for a claim-graph research store
- Content-addressed node IDs using deterministic hashing
- Typed nodes and typed edges
- Structured branch templates for support, objection, reframing, and application flows
- Node status and confidence metadata
- Input validation for node type, status, and confidence range (0.0-1.0)
- CLI argument validation via argparse choices
- Claim-card style node inspection
- Local ASCII tree rendering
- Provenance-focused why view
- Filtered node listing by status, type, tag, query, and limit
- Home dashboard for graph summary and next actions
- Lineage inspection
- Markdown export for a selected subgraph
- Bootstrap flow seeded from the original concept conversation
- Defensive error handling for corrupt stores and missing node references
- Optimized single-read traversal for tree and provenance rendering
- `python -m sparkle` entrypoint
- Automated tests for the current CLI workflows
- Repository docs that anchor the concept, scope, and next steps

## Next

### Phase 1: Research ergonomics

- Editable working views layered over immutable node content
- More structured export formats for memo, outline, and literature-review modes
- Ergonomic alias commands for the most common research moves

### Phase 2: Trust and provenance

- Rich citations with excerpt storage and source metadata
- Stronger lineage views for "why do I believe this?" and "what would change my mind?"
- Branch evaluation fields like evidence coverage, unresolved objections, and abandonment reason
- Merge and supersede workflows for converging syntheses

## Later

### Phase 3: Interface

- TUI or web UI for claim-card navigation
- Graph visualization with path highlighting
- Branch triage dashboard for active, stalled, abandoned, and harvested work
- Guided claim review for weak support and unresolved objections

### Phase 4: Collaboration

- Shared repositories or sync
- Multi-author provenance and attribution
- Review and comment workflows on claims and syntheses
- Conflict-aware merge support for research branches
