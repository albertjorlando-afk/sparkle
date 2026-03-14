# Sparkle

Claim-graph research MVP with content-addressed provenance. Pure Python 3.11+, zero external dependencies.

## Project structure

- `src/sparkle/` — core package (models, graph store, CLI, templates, bootstrap)
- `tests/test_cli.py` — integration tests via unittest
- `docs/` — PRD and roadmap
- `.sparkle/graph.json` — local graph data (not committed)

## Key conventions

- **Immutable data model**: Node and Edge are frozen dataclasses with SHA256 content-addressed IDs
- **No external dependencies**: stdlib only (dataclasses, json, pathlib, hashlib, argparse, collections)
- **Validation at boundaries**: confidence must be [0.0, 1.0], node types and statuses validated via argparse choices
- **Single JSON store**: all reads/writes go through `GraphStore._read()` / `._write()`
- **Error handling**: `ValueError` for user-facing errors, caught in `cli.main()` and printed to stderr with exit code 2

## Running

```bash
python3 -m sparkle <command>          # via __main__.py
python3 -m src.sparkle.cli <command>  # direct module
```

## Testing

```bash
python3 -m unittest discover -s tests -v
```

All tests must pass before committing. Tests use temp directories — no side effects.

## Docs

Three docs must stay in sync with code changes:
- `README.md` — features, class diagram, sequence diagram, state diagram, CLI examples
- `docs/prd.md` — MVP status, requirements, next focus
- `docs/roadmap.md` — completed items and phased next steps

Use `/doc-sync` after any feature or structural change to keep them aligned.
